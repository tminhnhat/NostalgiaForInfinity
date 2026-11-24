#!/usr/bin/env python3
"""Binance API Key IP Whitelist Auto-Updater & IP Change Alerter.

Monitors the live bot machine's public IPv4 address and:
1. Sub-Account mode (automatic update via Binance SAPI):
   When BINANCE_MASTER_API_KEY, BINANCE_MASTER_API_SECRET,
   BINANCE_SUBACCOUNT_EMAIL, and BINANCE_SUBACCOUNT_API_KEY (or
   FREQTRADE__EXCHANGE__KEY) are configured, automatically adds the new
   public IP to the sub-account API key whitelist via
   POST /sapi/v2/sub-account/subAccountApi/ipRestriction and optionally
   removes the previous dynamic IP via
   DELETE /sapi/v1/sub-account/subAccountApi/ipRestriction/ipList.
2. Master Account / Alert mode:
   Because Binance does not expose a public SAPI endpoint to modify the IP
   whitelist of a Master Account's own API key (requires 2FA/Passkey in
   Web/App), detects public IP changes, optionally checks whether the live
   API key is currently blocked by Binance (-2015), and sends an immediate
   Telegram alert with the new IP and a direct link to Binance API Management.

Zero third-party dependencies (Python 3 standard library only).
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib
import hmac
import html
import ipaddress
import json
import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path
import signal
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Callable

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

DEFAULT_IP_PROVIDERS: tuple[str, ...] = (
    "https://api.ipify.org",
    "https://ifconfig.me/ip",
    "https://icanhazip.com",
    "https://checkip.amazonaws.com",
)
DEFAULT_BINANCE_BASE_URL = "https://api.binance.com"
DEFAULT_STATE_FILE = "user_data/binance_ip_state.json"
BINANCE_API_MGMT_URL = "https://www.binance.com/en/my/settings/api-management"
DEFAULT_RECV_WINDOW = 10000
DEFAULT_CHECK_INTERVAL = 300
DEFAULT_RECONCILE_EVERY = 3600
DEFAULT_RETRY_DELAY = 30
DEFAULT_MAX_CONSECUTIVE_ERRORS = 3
MAX_HISTORY_ENTRIES = 50
CRON_MARKER = "# binance-ip-whitelist-updater"

logger = logging.getLogger("BinanceIPUpdater")


class BinanceAPIError(RuntimeError):
    """Raised when Binance API returns an HTTP or application-level error."""

    def __init__(self, status_code: int, code: int | None, msg: str, raw: str = ""):
        self.status_code = status_code
        self.code = code
        self.msg = msg
        self.raw = raw
        detail = f"HTTP {status_code}"
        if code is not None:
            detail += f" | Binance code {code}"
        if msg:
            detail += f": {msg}"
        super().__init__(detail)


@dataclass
class UpdaterConfig:
    """Runtime configuration resolved from CLI args, environment, and .env."""

    mode: str = "auto"  # auto | subaccount | alert
    bot_name: str = "LiveBot"
    binance_base_url: str = DEFAULT_BINANCE_BASE_URL
    recv_window: int = DEFAULT_RECV_WINDOW

    # Sub-Account auto-update credentials (Master API Key -> Sub-Account API Key)
    master_api_key: str = ""
    master_api_secret: str = ""
    subaccount_email: str = ""
    subaccount_api_key: str = ""
    keep_ips: list[str] = field(default_factory=list)
    remove_old_ip: bool = True

    # Live bot API key (used as fallback for subaccount_api_key and connectivity check)
    live_api_key: str = ""
    live_api_secret: str = ""

    # Telegram notifications
    telegram_token: str = ""
    telegram_chat_id: str = ""
    notify_telegram: bool = True

    # Execution & state
    state_file: Path = field(default_factory=lambda: Path(DEFAULT_STATE_FILE))
    log_file: str = ""
    ip_providers: tuple[str, ...] = DEFAULT_IP_PROVIDERS
    http_timeout: int = 15
    check_interval: int = DEFAULT_CHECK_INTERVAL
    reconcile_every: int = DEFAULT_RECONCILE_EVERY
    retry_delay: int = DEFAULT_RETRY_DELAY
    max_consecutive_errors: int = DEFAULT_MAX_CONSECUTIVE_ERRORS
    dry_run: bool = False
    force: bool = False

    def has_subaccount_credentials(self) -> bool:
        return bool(
            self.master_api_key
            and self.master_api_secret
            and self.subaccount_email
            and self.subaccount_api_key
        )

    def resolved_mode(self) -> str:
        if self.mode == "auto":
            return "subaccount" if self.has_subaccount_credentials() else "alert"
        return self.mode


def parse_env_file(env_path: Path) -> dict[str, str]:
    """Parse key=value pairs from a .env file without mutating os.environ."""
    values: dict[str, str] = {}
    if not env_path.exists():
        return values
    with open(env_path, "r", encoding="utf-8") as fh:
        for raw_line in fh:
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            if line.startswith("export "):
                line = line[len("export ") :].strip()
            key, val = line.split("=", 1)
            key = key.strip()
            val = val.strip()
            if len(val) >= 2 and val[0] == val[-1] and val[0] in ("'", '"'):
                val = val[1:-1]
            elif " #" in val:
                val = val.split(" #", 1)[0].strip()
            if key:
                values[key] = val
    return values


def _get_setting(
    env_file_vars: dict[str, str],
    *keys: str,
    default: str = "",
) -> str:
    """Return first non-empty value checking OS environment first, then .env."""
    for key in keys:
        val = os.environ.get(key)
        if val is not None and val.strip() != "":
            return val.strip()
    for key in keys:
        val = env_file_vars.get(key)
        if val is not None and val.strip() != "":
            return val.strip()
    return default


def _parse_bool(value: str, default: bool = True) -> bool:
    if not value:
        return default
    return value.strip().lower() in ("1", "true", "yes", "y", "on")


def _parse_ip_list(raw: str) -> list[str]:
    ips: list[str] = []
    for part in raw.split(","):
        candidate = part.strip()
        if not candidate:
            continue
        try:
            normalized = str(ipaddress.IPv4Address(candidate))
            if normalized not in ips:
                ips.append(normalized)
        except ipaddress.AddressValueError:
            logger.warning("Ignoring invalid IPv4 in BINANCE_KEEP_IPS: %s", candidate)
    return ips


def mask_api_key(api_key: str) -> str:
    """Mask an API key for safe logging/alerting."""
    if not api_key:
        return "(none)"
    if len(api_key) <= 10:
        return f"{api_key[:2]}***{api_key[-2:]}"
    return f"{api_key[:6]}...{api_key[-4:]}"


def load_config(args: argparse.Namespace) -> UpdaterConfig:
    """Build UpdaterConfig from CLI args, environment variables, and .env."""
    env_path = Path(args.env_file)
    env_vars = parse_env_file(env_path)

    live_key = _get_setting(
        env_vars,
        "BINANCE_LIVE_API_KEY",
        "FREQTRADE__EXCHANGE__KEY",
    )
    live_secret = _get_setting(
        env_vars,
        "BINANCE_LIVE_API_SECRET",
        "FREQTRADE__EXCHANGE__SECRET",
    )
    sub_key = _get_setting(
        env_vars,
        "BINANCE_SUBACCOUNT_API_KEY",
        "FREQTRADE__EXCHANGE__KEY",
    )

    state_file_str = args.state_file or _get_setting(
        env_vars,
        "BINANCE_IP_STATE_FILE",
        default=DEFAULT_STATE_FILE,
    )
    mode = args.mode or _get_setting(env_vars, "BINANCE_IP_MODE", default="auto").lower()
    if mode not in ("auto", "subaccount", "alert"):
        raise ValueError(f"Invalid mode '{mode}'. Expected: auto, subaccount, alert.")

    remove_old_env = _parse_bool(
        _get_setting(env_vars, "BINANCE_REMOVE_OLD_IP", default="true"),
        default=True,
    )
    remove_old_ip = False if args.keep_old_ip else remove_old_env

    keep_ips_raw = _get_setting(env_vars, "BINANCE_KEEP_IPS", default="")
    if args.keep_ips:
        keep_ips_raw = f"{keep_ips_raw},{args.keep_ips}" if keep_ips_raw else args.keep_ips

    providers_raw = _get_setting(env_vars, "BINANCE_IP_PROVIDERS", default="")
    if providers_raw:
        providers = tuple(p.strip() for p in providers_raw.split(",") if p.strip())
    else:
        providers = DEFAULT_IP_PROVIDERS

    check_interval = args.interval if args.interval is not None else int(
        _get_setting(
            env_vars,
            "BINANCE_IP_CHECK_INTERVAL",
            default=str(DEFAULT_CHECK_INTERVAL),
        )
    )
    reconcile_every = args.reconcile_every if args.reconcile_every is not None else int(
        _get_setting(
            env_vars,
            "BINANCE_IP_RECONCILE_EVERY",
            default=str(DEFAULT_RECONCILE_EVERY),
        )
    )
    retry_delay = args.retry_delay if args.retry_delay is not None else int(
        _get_setting(
            env_vars,
            "BINANCE_IP_RETRY_DELAY",
            default=str(DEFAULT_RETRY_DELAY),
        )
    )
    max_consecutive_errors = int(
        _get_setting(
            env_vars,
            "BINANCE_IP_MAX_CONSECUTIVE_ERRORS",
            default=str(DEFAULT_MAX_CONSECUTIVE_ERRORS),
        )
    )
    log_file = args.log_file or _get_setting(env_vars, "BINANCE_IP_LOG_FILE", default="")

    return UpdaterConfig(
        mode=mode,
        bot_name=_get_setting(
            env_vars,
            "BINANCE_BOT_NAME",
            "FREQTRADE__BOT_NAME",
            default="LiveBot",
        ),
        binance_base_url=_get_setting(
            env_vars,
            "BINANCE_API_BASE_URL",
            default=DEFAULT_BINANCE_BASE_URL,
        ).rstrip("/"),
        recv_window=int(
            _get_setting(
                env_vars,
                "BINANCE_RECV_WINDOW",
                default=str(DEFAULT_RECV_WINDOW),
            )
        ),
        master_api_key=_get_setting(env_vars, "BINANCE_MASTER_API_KEY"),
        master_api_secret=_get_setting(env_vars, "BINANCE_MASTER_API_SECRET"),
        subaccount_email=_get_setting(env_vars, "BINANCE_SUBACCOUNT_EMAIL"),
        subaccount_api_key=sub_key,
        keep_ips=_parse_ip_list(keep_ips_raw),
        remove_old_ip=remove_old_ip,
        live_api_key=live_key,
        live_api_secret=live_secret,
        telegram_token=_get_setting(
            env_vars,
            "TELEGRAM_BOT_TOKEN",
            "FREQTRADE__TELEGRAM__TOKEN",
        ),
        telegram_chat_id=_get_setting(
            env_vars,
            "TELEGRAM_CHAT_ID",
            "FREQTRADE__TELEGRAM__CHAT_ID",
        ),
        notify_telegram=not args.no_telegram,
        state_file=Path(state_file_str),
        log_file=log_file,
        ip_providers=providers,
        http_timeout=args.timeout,
        check_interval=max(10, check_interval),
        reconcile_every=max(0, reconcile_every),
        retry_delay=max(5, retry_delay),
        max_consecutive_errors=max(1, max_consecutive_errors),
        dry_run=args.dry_run,
        force=args.force,
    )


def get_public_ip(
    providers: tuple[str, ...] = DEFAULT_IP_PROVIDERS,
    timeout: int = 10,
) -> str:
    """Fetch current public IPv4 address using multi-provider fallback."""
    errors: list[str] = []
    for url in providers:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "BinanceIPWhitelistUpdater/1.0"},
            method="GET",
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw = resp.read().decode("utf-8", errors="replace").strip()
            ip_obj = ipaddress.IPv4Address(raw)
            return str(ip_obj)
        except Exception as exc:
            errors.append(f"{url}: {exc}")
            logger.debug("IP provider failed (%s): %s", url, exc)

    raise RuntimeError(
        "Failed to detect public IPv4 from all providers: " + " ; ".join(errors)
    )


def load_state(state_file: Path) -> dict[str, Any]:
    """Load persisted IP state from JSON file."""
    if not state_file.exists():
        return {}
    try:
        with open(state_file, "r", encoding="utf-8") as fh:
            data = json.load(fh)
            return data if isinstance(data, dict) else {}
    except Exception as exc:
        logger.warning("Could not read state file %s: %s", state_file, exc)
        return {}


def save_state(state_file: Path, state: dict[str, Any]) -> None:
    """Atomically write state JSON to disk."""
    state_file.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = state_file.with_suffix(state_file.suffix + ".tmp")
    with open(tmp_path, "w", encoding="utf-8") as fh:
        json.dump(state, fh, indent=2, ensure_ascii=False)
    os.replace(tmp_path, state_file)


def sign_binance_query(params: dict[str, Any], api_secret: str) -> str:
    """Build URL-encoded query string and append HMAC-SHA256 signature."""
    filtered = [(k, str(v)) for k, v in params.items() if v is not None]
    query_string = urllib.parse.urlencode(filtered)
    signature = hmac.new(
        api_secret.encode("utf-8"),
        query_string.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    return f"{query_string}&signature={signature}"


class BinanceClient:
    """Minimal signed REST client for Binance SAPI IP restriction endpoints."""

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        base_url: str = DEFAULT_BINANCE_BASE_URL,
        recv_window: int = DEFAULT_RECV_WINDOW,
        timeout: int = 15,
    ):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url.rstrip("/")
        self.recv_window = recv_window
        self.timeout = timeout
        self._time_offset_ms: int | None = None

    def _get_time_offset_ms(self) -> int:
        if self._time_offset_ms is not None:
            return self._time_offset_ms
        url = f"{self.base_url}/api/v3/time"
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "BinanceIPWhitelistUpdater/1.0"},
            method="GET",
        )
        try:
            with urllib.request.urlopen(req, timeout=min(self.timeout, 10)) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                server_time = int(data["serverTime"])
                local_time = int(time.time() * 1000)
                self._time_offset_ms = server_time - local_time
        except Exception as exc:
            logger.debug("Could not sync Binance server time (using local clock): %s", exc)
            self._time_offset_ms = 0
        return self._time_offset_ms

    def signed_request(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = dict(params or {})
        payload["recvWindow"] = self.recv_window
        payload["timestamp"] = int(time.time() * 1000) + self._get_time_offset_ms()

        signed_query = sign_binance_query(payload, self.api_secret)
        url = f"{self.base_url}{endpoint}"
        headers = {
            "X-MBX-APIKEY": self.api_key,
            "User-Agent": "BinanceIPWhitelistUpdater/1.0",
        }
        data: bytes | None = None
        if method.upper() == "POST":
            headers["Content-Type"] = "application/x-www-form-urlencoded"
            data = signed_query.encode("utf-8")
        else:
            url = f"{url}?{signed_query}"

        req = urllib.request.Request(url, data=data, headers=headers, method=method.upper())
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                body = resp.read().decode("utf-8")
                return json.loads(body) if body else {}
        except urllib.error.HTTPError as exc:
            raw_err = exc.read().decode("utf-8", errors="replace")
            code: int | None = None
            msg = raw_err
            try:
                parsed = json.loads(raw_err)
                code = parsed.get("code")
                msg = parsed.get("msg", raw_err)
            except Exception:
                pass
            raise BinanceAPIError(exc.code, code, msg, raw_err) from exc

    def get_subaccount_ip_restriction(
        self,
        email: str,
        subaccount_api_key: str,
    ) -> dict[str, Any]:
        """GET /sapi/v1/sub-account/subAccountApi/ipRestriction."""
        return self.signed_request(
            "GET",
            "/sapi/v1/sub-account/subAccountApi/ipRestriction",
            {
                "email": email,
                "subAccountApiKey": subaccount_api_key,
            },
        )

    def update_subaccount_ip_restriction(
        self,
        email: str,
        subaccount_api_key: str,
        ip_addresses: list[str],
        status: str = "2",
    ) -> dict[str, Any]:
        """POST /sapi/v2/sub-account/subAccountApi/ipRestriction.

        status="1" -> IP Unrestricted
        status="2" -> Restrict access to trusted IPs only
        """
        params: dict[str, Any] = {
            "email": email,
            "subAccountApiKey": subaccount_api_key,
            "status": status,
        }
        if ip_addresses:
            params["ipAddress"] = ",".join(ip_addresses)
        return self.signed_request(
            "POST",
            "/sapi/v2/sub-account/subAccountApi/ipRestriction",
            params,
        )

    def delete_subaccount_ip_list(
        self,
        email: str,
        subaccount_api_key: str,
        ip_addresses: list[str],
    ) -> dict[str, Any]:
        """DELETE /sapi/v1/sub-account/subAccountApi/ipRestriction/ipList."""
        return self.signed_request(
            "DELETE",
            "/sapi/v1/sub-account/subAccountApi/ipRestriction/ipList",
            {
                "email": email,
                "subAccountApiKey": subaccount_api_key,
                "ipAddress": ",".join(ip_addresses),
            },
        )

    def get_account_api_restrictions(self) -> dict[str, Any]:
        """GET /sapi/v1/account/apiRestrictions (read-only health/IP check)."""
        return self.signed_request("GET", "/sapi/v1/account/apiRestrictions", {})


def send_telegram_message(
    token: str,
    chat_id: str,
    message: str,
    timeout: int = 15,
) -> bool:
    """Send an HTML-formatted message to Telegram."""
    if not token or not chat_id:
        logger.debug("Telegram credentials not configured; skipping notification.")
        return False
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = urllib.parse.urlencode(
        {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "HTML",
            "disable_web_page_preview": "true",
        }
    ).encode("utf-8")
    req = urllib.request.Request(url, data=payload, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status == 200
    except Exception as exc:
        logger.error("Failed to send Telegram message: %s", exc)
        return False


def check_live_api_key_access(cfg: UpdaterConfig) -> str:
    """Check whether the live bot's own Binance API key is accepted from this IP."""
    if not cfg.live_api_key or not cfg.live_api_secret:
        return "not_configured"
    if cfg.live_api_key.startswith("Put_Your_") or cfg.live_api_secret.startswith("Put_Your_"):
        return "not_configured"
    client = BinanceClient(
        api_key=cfg.live_api_key,
        api_secret=cfg.live_api_secret,
        base_url=cfg.binance_base_url,
        recv_window=cfg.recv_window,
        timeout=cfg.http_timeout,
    )
    try:
        info = client.get_account_api_restrictions()
        ip_restrict = info.get("ipRestrict")
        return f"ok (ipRestrict={ip_restrict})"
    except BinanceAPIError as exc:
        if exc.code == -2015:
            return "blocked_ip (-2015 Invalid API-key, IP, or permissions)"
        return f"error ({exc})"
    except Exception as exc:
        return f"error ({exc})"


def _build_subaccount_update_plan(
    current_ip: str,
    old_ip: str | None,
    existing_ip_list: list[str],
    existing_status: str,
    keep_ips: list[str],
    remove_old_ip: bool,
) -> tuple[list[str], list[str]]:
    """Compute (ips_to_add, ips_to_delete) safely.

    Always adds missing required IPs first; never deletes current_ip or keep_ips.
    """
    required_ips: list[str] = [current_ip]
    for ip in keep_ips:
        if ip not in required_ips:
            required_ips.append(ip)

    ips_to_add = [ip for ip in required_ips if ip not in existing_ip_list]
    if existing_status != "2" and not ips_to_add:
        # Must still call POST with status=2 and current_ip to enable restriction
        ips_to_add = [current_ip]

    protected = set(required_ips)
    ips_to_delete: list[str] = []
    if remove_old_ip and old_ip and old_ip != current_ip:
        if old_ip in existing_ip_list and old_ip not in protected:
            ips_to_delete.append(old_ip)

    return ips_to_add, ips_to_delete


def run_once(cfg: UpdaterConfig, reconcile: bool = False) -> dict[str, Any]:
    """Execute one IP detection and Binance whitelist sync / alert cycle.

    When ``reconcile=True`` and the public IP has not changed:
    - In ``subaccount`` mode: re-verifies with Binance that ``current_ip`` is
      still whitelisted (re-adding it if missing).
    - In ``alert`` mode: checks live API key connectivity and sends a Telegram
      alert if Binance reports ``-2015`` (IP blocked).
    """
    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    resolved_mode = cfg.resolved_mode()
    state = load_state(cfg.state_file)
    old_ip: str | None = state.get("last_ip")

    current_ip = get_public_ip(providers=cfg.ip_providers, timeout=cfg.http_timeout)
    ip_changed = old_ip != current_ip

    logger.info(
        "Public IP=%s | Previous IP=%s | Changed=%s | Reconcile=%s | Mode=%s | DryRun=%s",
        current_ip,
        old_ip or "(first run)",
        ip_changed,
        reconcile,
        resolved_mode,
        cfg.dry_run,
    )

    if not ip_changed and not cfg.force and not reconcile:
        return {
            "status": "unchanged",
            "mode": resolved_mode,
            "current_ip": current_ip,
            "old_ip": old_ip,
        }

    # Periodic reconciliation in alert mode: only alert if live API key is actually blocked
    if not ip_changed and not cfg.force and reconcile and resolved_mode == "alert":
        api_check = check_live_api_key_access(cfg)
        if not api_check.startswith("blocked_ip"):
            logger.info("Periodic reconcile OK (IP=%s, live_api_check=%s)", current_ip, api_check)
            return {
                "status": "reconciled_ok",
                "mode": resolved_mode,
                "current_ip": current_ip,
                "old_ip": old_ip,
                "live_api_check": api_check,
            }
        logger.warning(
            "Periodic reconcile detected blocked IP on Binance (%s): %s",
            current_ip,
            api_check,
        )

    result: dict[str, Any] = {
        "status": "ok",
        "mode": resolved_mode,
        "current_ip": current_ip,
        "old_ip": old_ip,
        "updated_utc": now_utc,
    }

    if resolved_mode == "subaccount":
        if not cfg.has_subaccount_credentials():
            raise ValueError(
                "Sub-Account mode requires BINANCE_MASTER_API_KEY, "
                "BINANCE_MASTER_API_SECRET, BINANCE_SUBACCOUNT_EMAIL, and "
                "BINANCE_SUBACCOUNT_API_KEY (or FREQTRADE__EXCHANGE__KEY)."
            )

        client = BinanceClient(
            api_key=cfg.master_api_key,
            api_secret=cfg.master_api_secret,
            base_url=cfg.binance_base_url,
            recv_window=cfg.recv_window,
            timeout=cfg.http_timeout,
        )

        try:
            current_info = client.get_subaccount_ip_restriction(
                email=cfg.subaccount_email,
                subaccount_api_key=cfg.subaccount_api_key,
            )
            existing_ip_list = list(current_info.get("ipList") or [])
            existing_status = str(current_info.get("status") or "")
            if not existing_status and current_info.get("ipRestrict") is True:
                existing_status = "2"

            ips_to_add, ips_to_delete = _build_subaccount_update_plan(
                current_ip=current_ip,
                old_ip=old_ip,
                existing_ip_list=existing_ip_list,
                existing_status=existing_status,
                keep_ips=cfg.keep_ips,
                remove_old_ip=cfg.remove_old_ip,
            )
            result["existing_ip_list"] = existing_ip_list
            result["ips_to_add"] = ips_to_add
            result["ips_to_delete"] = ips_to_delete

            final_ip_list = list(existing_ip_list)
            if cfg.dry_run:
                logger.info(
                    "[DRY-RUN] Would add IPs=%s (status=2) and delete IPs=%s on sub-account %s (%s)",
                    ips_to_add,
                    ips_to_delete,
                    cfg.subaccount_email,
                    mask_api_key(cfg.subaccount_api_key),
                )
                result["status"] = "dry_run"
                return result

            if ips_to_add:
                logger.info("Adding IP(s) %s to Binance Sub-Account whitelist...", ips_to_add)
                add_resp = client.update_subaccount_ip_restriction(
                    email=cfg.subaccount_email,
                    subaccount_api_key=cfg.subaccount_api_key,
                    ip_addresses=ips_to_add,
                    status="2",
                )
                final_ip_list = list(add_resp.get("ipList") or final_ip_list)
                logger.info("Binance whitelist after ADD: %s", final_ip_list)

            if ips_to_delete:
                if current_ip in final_ip_list:
                    logger.info(
                        "Removing old IP(s) %s from Binance Sub-Account whitelist...",
                        ips_to_delete,
                    )
                    del_resp = client.delete_subaccount_ip_list(
                        email=cfg.subaccount_email,
                        subaccount_api_key=cfg.subaccount_api_key,
                        ip_addresses=ips_to_delete,
                    )
                    final_ip_list = list(del_resp.get("ipList") or final_ip_list)
                    logger.info("Binance whitelist after DELETE: %s", final_ip_list)
                else:
                    logger.warning(
                        "Skipping DELETE of %s because current_ip %s was not confirmed in ipList %s",
                        ips_to_delete,
                        current_ip,
                        final_ip_list,
                    )

            result["final_ip_list"] = final_ip_list
            result["status"] = "updated" if (ips_to_add or ips_to_delete) else "already_whitelisted"

            should_notify = cfg.notify_telegram and (
                bool(ips_to_add or ips_to_delete) or ip_changed or cfg.force
            )
            if should_notify:
                msg = (
                    f"<b>Binance IP Whitelist Auto-Updated</b>\n"
                    f"• <b>Bot:</b> <code>{html.escape(cfg.bot_name)}</code>\n"
                    f"• <b>Sub-Account:</b> <code>{html.escape(cfg.subaccount_email)}</code>\n"
                    f"• <b>API Key:</b> <code>{html.escape(mask_api_key(cfg.subaccount_api_key))}</code>\n"
                    f"• <b>Old IP:</b> <code>{html.escape(old_ip or 'N/A')}</code>\n"
                    f"• <b>New IP:</b> <code>{html.escape(current_ip)}</code>\n"
                    f"• <b>Active Whitelist:</b> <code>{html.escape(', '.join(final_ip_list) or current_ip)}</code>\n"
                    f"• <b>Time:</b> {now_utc}"
                )
                send_telegram_message(cfg.telegram_token, cfg.telegram_chat_id, msg, cfg.http_timeout)

        except Exception as exc:
            logger.error("Failed to auto-update Binance Sub-Account IP whitelist: %s", exc)
            if cfg.notify_telegram and not cfg.dry_run:
                err_msg = (
                    f"<b>Binance IP Whitelist Update FAILED</b>\n"
                    f"• <b>Bot:</b> <code>{html.escape(cfg.bot_name)}</code>\n"
                    f"• <b>Old IP:</b> <code>{html.escape(old_ip or 'N/A')}</code>\n"
                    f"• <b>New IP:</b> <code>{html.escape(current_ip)}</code>\n"
                    f"• <b>Error:</b> <code>{html.escape(str(exc))}</code>\n"
                    f"• <b>Manual Update:</b> {BINANCE_API_MGMT_URL}\n"
                    f"• <b>Time:</b> {now_utc}"
                )
                send_telegram_message(cfg.telegram_token, cfg.telegram_chat_id, err_msg, cfg.http_timeout)
            raise

    else:
        # Master Account / Alert mode
        api_check = check_live_api_key_access(cfg)
        result["live_api_check"] = api_check
        logger.warning(
            "Public IP changed (%s -> %s). Master Account API keys cannot be updated "
            "via Binance API; live API check=%s",
            old_ip or "N/A",
            current_ip,
            api_check,
        )

        if cfg.dry_run:
            logger.info("[DRY-RUN] Would send Telegram alert for new IP %s", current_ip)
            result["status"] = "dry_run"
            return result

        sent = False
        if cfg.notify_telegram:
            msg = (
                f"<b>Live Bot IP Changed — Update Binance Whitelist</b>\n"
                f"• <b>Bot:</b> <code>{html.escape(cfg.bot_name)}</code>\n"
                f"• <b>Old IP:</b> <code>{html.escape(old_ip or 'N/A')}</code>\n"
                f"• <b>New IP:</b> <code>{html.escape(current_ip)}</code>\n"
                f"• <b>API Key:</b> <code>{html.escape(mask_api_key(cfg.live_api_key))}</code>\n"
                f"• <b>Binance Check:</b> <code>{html.escape(api_check)}</code>\n"
                f"• <b>Action:</b> Copy IP mới và cập nhật tại:\n{BINANCE_API_MGMT_URL}\n"
                f"• <b>Time:</b> {now_utc}"
            )
            sent = send_telegram_message(
                cfg.telegram_token,
                cfg.telegram_chat_id,
                msg,
                cfg.http_timeout,
            )
        result["telegram_sent"] = sent
        result["status"] = "alerted" if sent else "detected_no_telegram"

    # Persist updated state
    history = list(state.get("history") or [])
    history.append(
        {
            "timestamp_utc": now_utc,
            "old_ip": old_ip,
            "new_ip": current_ip,
            "mode": resolved_mode,
            "status": result["status"],
        }
    )
    new_state = {
        "last_ip": current_ip,
        "last_updated_utc": now_utc,
        "last_mode": resolved_mode,
        "last_status": result["status"],
        "last_binance_ip_list": result.get("final_ip_list", state.get("last_binance_ip_list", [])),
        "history": history[-MAX_HISTORY_ENTRIES:],
    }
    save_state(cfg.state_file, new_state)
    return result


def print_status(cfg: UpdaterConfig) -> int:
    """Print current public IP, mode, saved state, and optional Binance whitelist."""
    current_ip = get_public_ip(providers=cfg.ip_providers, timeout=cfg.http_timeout)
    state = load_state(cfg.state_file)
    resolved_mode = cfg.resolved_mode()

    info: dict[str, Any] = {
        "bot_name": cfg.bot_name,
        "current_public_ip": current_ip,
        "saved_last_ip": state.get("last_ip"),
        "ip_changed": state.get("last_ip") != current_ip,
        "resolved_mode": resolved_mode,
        "state_file": str(cfg.state_file),
        "telegram_configured": bool(cfg.telegram_token and cfg.telegram_chat_id),
        "keep_ips": cfg.keep_ips,
        "remove_old_ip": cfg.remove_old_ip,
    }

    if resolved_mode == "subaccount" and cfg.has_subaccount_credentials():
        client = BinanceClient(
            api_key=cfg.master_api_key,
            api_secret=cfg.master_api_secret,
            base_url=cfg.binance_base_url,
            recv_window=cfg.recv_window,
            timeout=cfg.http_timeout,
        )
        try:
            restriction = client.get_subaccount_ip_restriction(
                email=cfg.subaccount_email,
                subaccount_api_key=cfg.subaccount_api_key,
            )
            info["binance_subaccount"] = {
                "email": cfg.subaccount_email,
                "api_key": mask_api_key(cfg.subaccount_api_key),
                "status": restriction.get("status"),
                "ipRestrict": restriction.get("ipRestrict"),
                "ipList": restriction.get("ipList", []),
            }
        except Exception as exc:
            info["binance_subaccount_error"] = str(exc)
    else:
        info["live_api_check"] = check_live_api_key_access(cfg)

    print(json.dumps(info, indent=2, ensure_ascii=False))
    return 0


def _interval_to_cron_schedule(interval_seconds: int) -> str:
    """Convert a polling interval in seconds to a standard 5-field cron schedule."""
    minutes = max(1, round(interval_seconds / 60))
    if minutes < 60:
        return f"*/{minutes} * * * *"
    hours = max(1, round(minutes / 60))
    if hours < 24:
        return f"0 */{hours} * * *"
    return "0 0 * * *"


def _build_cron_entry(
    script_path: Path,
    work_dir: Path,
    env_file: str,
    interval_seconds: int,
    log_file: str = "",
    python_executable: str = sys.executable,
) -> str:
    schedule = _interval_to_cron_schedule(interval_seconds)
    log_target = log_file or "user_data/logs/binance_ip_updater.log"
    cmd_parts = [
        f"cd {work_dir}",
        f"mkdir -p $(dirname {log_target})",
        (
            f"{python_executable} {script_path} --env-file {env_file} "
            f">> {log_target} 2>&1"
        ),
    ]
    return f"{schedule} {' && '.join(cmd_parts)} {CRON_MARKER}"


def _upsert_cron_entry(existing_crontab: str, new_entry: str) -> str:
    lines = [
        line
        for line in existing_crontab.splitlines()
        if CRON_MARKER not in line
    ]
    while lines and not lines[-1].strip():
        lines.pop()
    lines.append(new_entry)
    return "\n".join(lines) + "\n"


def _remove_cron_entry(existing_crontab: str) -> str:
    lines = [
        line
        for line in existing_crontab.splitlines()
        if CRON_MARKER not in line
    ]
    if not lines:
        return ""
    return "\n".join(lines).rstrip("\n") + "\n"


def install_cron_job(args: argparse.Namespace, cfg: UpdaterConfig) -> int:
    """Install or update a tagged crontab entry for periodic IP checks."""
    script_path = Path(__file__).resolve()
    work_dir = Path.cwd().resolve()
    entry = _build_cron_entry(
        script_path=script_path,
        work_dir=work_dir,
        env_file=args.env_file,
        interval_seconds=cfg.check_interval,
        log_file=cfg.log_file,
    )

    if cfg.dry_run:
        logger.info("[DRY-RUN] Would install crontab entry:\n%s", entry)
        return 0

    proc = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    existing = proc.stdout if proc.returncode == 0 else ""
    updated = _upsert_cron_entry(existing, entry)
    apply_proc = subprocess.run(
        ["crontab", "-"],
        input=updated,
        capture_output=True,
        text=True,
    )
    if apply_proc.returncode != 0:
        logger.error("Failed to install crontab entry: %s", apply_proc.stderr.strip())
        return 1
    logger.info("Installed crontab entry:\n%s", entry)
    return 0


def uninstall_cron_job(cfg: UpdaterConfig) -> int:
    """Remove the tagged crontab entry."""
    proc = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    if proc.returncode != 0:
        logger.info("No crontab found for current user.")
        return 0
    updated = _remove_cron_entry(proc.stdout)
    if updated == proc.stdout:
        logger.info("No Binance IP updater cron entry found.")
        return 0
    if cfg.dry_run:
        logger.info("[DRY-RUN] Would remove crontab entry tagged with %s", CRON_MARKER)
        return 0
    apply_proc = subprocess.run(
        ["crontab", "-"],
        input=updated,
        capture_output=True,
        text=True,
    )
    if apply_proc.returncode != 0:
        logger.error("Failed to update crontab: %s", apply_proc.stderr.strip())
        return 1
    logger.info("Removed crontab entry tagged with %s", CRON_MARKER)
    return 0


def render_systemd_unit(args: argparse.Namespace, cfg: UpdaterConfig) -> str:
    """Render a systemd service unit file for running --watch continuously."""
    script_path = Path(__file__).resolve()
    work_dir = Path.cwd().resolve()
    user = os.environ.get("USER") or "root"
    log_target = cfg.log_file or str(work_dir / "user_data/logs/binance_ip_updater.log")
    return (
        "[Unit]\n"
        f"Description=Binance IP Whitelist Periodic Updater ({cfg.bot_name})\n"
        "After=network-online.target\n"
        "Wants=network-online.target\n"
        "\n"
        "[Service]\n"
        "Type=simple\n"
        f"User={user}\n"
        f"WorkingDirectory={work_dir}\n"
        f"ExecStart={sys.executable} -u {script_path} "
        f"--env-file {args.env_file} --watch "
        f"--interval {cfg.check_interval} "
        f"--reconcile-every {cfg.reconcile_every} "
        f"--log-file {log_target}\n"
        "Restart=always\n"
        "RestartSec=15\n"
        "\n"
        "[Install]\n"
        "WantedBy=multi-user.target\n"
    )


def run_periodic_loop(
    cfg: UpdaterConfig,
    *,
    max_cycles: int = 0,
    sleep_fn: Callable[[float], None] = time.sleep,
    monotonic_fn: Callable[[], float] = time.monotonic,
    stop_check: Callable[[], bool] | None = None,
) -> int:
    """Run periodic IP check loop with reconciliation and error backoff."""
    stop_requested = False

    def _should_stop() -> bool:
        return stop_requested or (stop_check() if stop_check else False)

    if stop_check is None:
        def _handle_signal(signum: int, _frame: Any) -> None:
            nonlocal stop_requested
            logger.info("Received signal %s; shutting down periodic watcher...", signum)
            stop_requested = True

        signal.signal(signal.SIGINT, _handle_signal)
        signal.signal(signal.SIGTERM, _handle_signal)

    interval = max(10, cfg.check_interval)
    reconcile_every = max(0, cfg.reconcile_every)
    retry_delay = max(5, min(cfg.retry_delay, interval))

    logger.info(
        "Starting periodic IP watcher (mode=%s, interval=%ss, reconcile_every=%ss, "
        "retry_delay=%ss, state=%s)",
        cfg.resolved_mode(),
        interval,
        reconcile_every,
        retry_delay,
        cfg.state_file,
    )

    last_reconcile_ts = monotonic_fn()
    consecutive_errors = 0
    error_alert_sent = False
    cycles = 0

    while not _should_stop():
        cycles += 1
        now_mono = monotonic_fn()
        do_reconcile = reconcile_every > 0 and (now_mono - last_reconcile_ts) >= reconcile_every

        try:
            res = run_once(cfg, reconcile=do_reconcile)
            if do_reconcile:
                last_reconcile_ts = now_mono
            if res.get("status") not in ("unchanged", "reconciled_ok"):
                logger.info("Cycle #%d result: %s", cycles, json.dumps(res, ensure_ascii=False))

            if error_alert_sent and cfg.notify_telegram and not cfg.dry_run:
                send_telegram_message(
                    cfg.telegram_token,
                    cfg.telegram_chat_id,
                    (
                        f"<b>Binance IP Watcher Recovered</b>\n"
                        f"• <b>Bot:</b> <code>{html.escape(cfg.bot_name)}</code>\n"
                        f"• <b>Current IP:</b> <code>{html.escape(str(res.get('current_ip', 'N/A')))}</code>\n"
                        f"• <b>Status:</b> <code>{html.escape(str(res.get('status', 'ok')))}</code>"
                    ),
                    cfg.http_timeout,
                )
            consecutive_errors = 0
            error_alert_sent = False
            wait_seconds = interval
        except Exception as exc:
            consecutive_errors += 1
            wait_seconds = min(interval, retry_delay * (2 ** min(consecutive_errors - 1, 3)))
            logger.error(
                "Periodic check #%d failed (%d consecutive) — retrying in %ss: %s",
                cycles,
                consecutive_errors,
                wait_seconds,
                exc,
            )
            if (
                consecutive_errors >= cfg.max_consecutive_errors
                and not error_alert_sent
                and cfg.notify_telegram
                and not cfg.dry_run
            ):
                error_alert_sent = send_telegram_message(
                    cfg.telegram_token,
                    cfg.telegram_chat_id,
                    (
                        f"<b>Binance IP Watcher Consecutive Errors ({consecutive_errors})</b>\n"
                        f"• <b>Bot:</b> <code>{html.escape(cfg.bot_name)}</code>\n"
                        f"• <b>Last Error:</b> <code>{html.escape(str(exc))}</code>\n"
                        f"• <b>Next Retry:</b> {wait_seconds}s"
                    ),
                    cfg.http_timeout,
                )

        # After first iteration, turn off one-time --force flag
        cfg.force = False
        if max_cycles > 0 and cycles >= max_cycles:
            break

        slept = 0
        while slept < wait_seconds and not _should_stop():
            step = min(1, wait_seconds - slept)
            sleep_fn(step)
            slept += step

    return 0


def configure_logging(verbose: bool = False, log_file: str = "") -> None:
    """Configure console logging and optional rotating file handler."""
    level = logging.DEBUG if verbose else logging.INFO
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.handlers.clear()

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    root_logger.addHandler(stream_handler)

    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = RotatingFileHandler(
            log_path,
            maxBytes=5 * 1024 * 1024,
            backupCount=3,
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Auto-update Binance Sub-Account API IP whitelist or alert via Telegram on live bot IP change."
    )
    parser.add_argument(
        "--env-file",
        default=".env",
        help="Path to .env file (default: .env).",
    )
    parser.add_argument(
        "--state-file",
        default="",
        help=f"Path to JSON state file (default: {DEFAULT_STATE_FILE}).",
    )
    parser.add_argument(
        "--log-file",
        default="",
        help="Optional rotating log file path (or BINANCE_IP_LOG_FILE).",
    )
    parser.add_argument(
        "--mode",
        choices=("auto", "subaccount", "alert"),
        default="",
        help="Operation mode: auto (default), subaccount, or alert.",
    )
    parser.add_argument(
        "--keep-ips",
        default="",
        help="Comma-separated static IPv4 addresses to always keep in whitelist.",
    )
    parser.add_argument(
        "--keep-old-ip",
        action="store_true",
        help="Do not delete the previous dynamic IP after adding the new IP.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force Binance sync / Telegram alert even if public IP has not changed.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview actions without modifying Binance whitelist, state file, or sending Telegram.",
    )
    parser.add_argument(
        "--no-telegram",
        action="store_true",
        help="Disable Telegram notifications.",
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Print current public IP, mode, saved state, and Binance status as JSON.",
    )
    parser.add_argument(
        "--watch",
        "--daemon",
        dest="watch",
        action="store_true",
        help="Run continuously in periodic check mode every --interval seconds.",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=None,
        help=f"Periodic check interval in seconds (default: {DEFAULT_CHECK_INTERVAL} or BINANCE_IP_CHECK_INTERVAL).",
    )
    parser.add_argument(
        "--reconcile-every",
        type=int,
        default=None,
        help=(
            f"Re-verify Binance whitelist/access every N seconds in --watch mode even if "
            f"IP has not changed (default: {DEFAULT_RECONCILE_EVERY}, 0 to disable)."
        ),
    )
    parser.add_argument(
        "--retry-delay",
        type=int,
        default=None,
        help=f"Initial retry delay in seconds after a failed check in --watch mode (default: {DEFAULT_RETRY_DELAY}).",
    )
    parser.add_argument(
        "--install-cron",
        action="store_true",
        help="Install/update a crontab entry to run periodic IP checks automatically.",
    )
    parser.add_argument(
        "--uninstall-cron",
        action="store_true",
        help="Remove the crontab entry installed by --install-cron.",
    )
    parser.add_argument(
        "--print-systemd",
        action="store_true",
        help="Print a ready-to-use systemd service unit file for --watch mode.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=15,
        help="HTTP request timeout in seconds (default: 15).",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable DEBUG logging.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)

    configure_logging(verbose=args.verbose)

    try:
        cfg = load_config(args)
    except Exception as exc:
        logger.error("Configuration error: %s", exc)
        return 2

    if cfg.log_file:
        configure_logging(verbose=args.verbose, log_file=cfg.log_file)

    if args.print_systemd:
        print(render_systemd_unit(args, cfg))
        return 0

    if args.install_cron:
        return install_cron_job(args, cfg)

    if args.uninstall_cron:
        return uninstall_cron_job(cfg)

    if args.status:
        try:
            return print_status(cfg)
        except Exception as exc:
            logger.error("Status check failed: %s", exc)
            return 1

    if not args.watch:
        try:
            res = run_once(cfg)
            logger.info("Result: %s", json.dumps(res, ensure_ascii=False))
            return 0
        except Exception as exc:
            logger.error("Execution failed: %s", exc)
            return 1

    return run_periodic_loop(cfg)


if __name__ == "__main__":
    sys.exit(main())
