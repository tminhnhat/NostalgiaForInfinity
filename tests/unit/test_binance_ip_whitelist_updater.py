"""Unit tests for tools/binance_ip_whitelist_updater.py."""

from __future__ import annotations

import argparse
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import urllib.error

REPO_ROOT = Path(__file__).resolve().parents[2]
TOOLS_DIR = REPO_ROOT / "tools"
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

import binance_ip_whitelist_updater as updater  # noqa: E402


class _FakeHTTPResponse:
    def __init__(self, body: str, status: int = 200):
        self._body = body.encode("utf-8")
        self.status = status

    def read(self) -> bytes:
        return self._body

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class TestBinanceIPWhitelistUpdater(unittest.TestCase):
    def test_get_public_ip_fallback(self):
        calls: list[str] = []

        def fake_urlopen(req, timeout=10):
            calls.append(req.full_url)
            if "provider1" in req.full_url:
                raise urllib.error.URLError("timeout")
            if "provider2" in req.full_url:
                return _FakeHTTPResponse("not-an-ip")
            return _FakeHTTPResponse("203.0.113.42\n")

        with patch("urllib.request.urlopen", side_effect=fake_urlopen):
            ip = updater.get_public_ip(
                providers=(
                    "https://provider1.example",
                    "https://provider2.example",
                    "https://provider3.example",
                ),
                timeout=5,
            )

        self.assertEqual(ip, "203.0.113.42")
        self.assertEqual(len(calls), 3)

    def test_sign_binance_query(self):
        signed = updater.sign_binance_query(
            {"email": "sub@test.com", "timestamp": 1700000000000},
            "my_secret_key",
        )
        self.assertIn("email=sub%40test.com", signed)
        self.assertIn("timestamp=1700000000000", signed)
        self.assertIn("&signature=", signed)
        sig = signed.split("&signature=")[1]
        self.assertEqual(len(sig), 64)

    def test_subaccount_update_plan_preserves_keep_ips_and_current_ip(self):
        to_add, to_del = updater._build_subaccount_update_plan(
            current_ip="198.51.100.20",
            old_ip="198.51.100.10",
            existing_ip_list=["198.51.100.10", "203.0.113.5"],
            existing_status="2",
            keep_ips=["203.0.113.5", "203.0.113.9"],
            remove_old_ip=True,
        )
        self.assertEqual(to_add, ["198.51.100.20", "203.0.113.9"])
        self.assertEqual(to_del, ["198.51.100.10"])

        # Never delete old_ip if it is in keep_ips
        to_add2, to_del2 = updater._build_subaccount_update_plan(
            current_ip="198.51.100.20",
            old_ip="203.0.113.5",
            existing_ip_list=["203.0.113.5"],
            existing_status="2",
            keep_ips=["203.0.113.5"],
            remove_old_ip=True,
        )
        self.assertEqual(to_add2, ["198.51.100.20"])
        self.assertEqual(to_del2, [])

    def test_run_once_subaccount_auto_update_add_then_delete(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state_path = Path(tmpdir) / "state.json"
            updater.save_state(state_path, {"last_ip": "198.51.100.10"})

            cfg = updater.UpdaterConfig(
                mode="auto",
                bot_name="TestBot",
                master_api_key="master_key_123456",
                master_api_secret="master_secret_123456",
                subaccount_email="sub@example.com",
                subaccount_api_key="sub_key_1234567890",
                keep_ips=["203.0.113.5"],
                remove_old_ip=True,
                telegram_token="tg_token",
                telegram_chat_id="12345",
                state_file=state_path,
            )

            actions: list[tuple[str, str]] = []

            def fake_urlopen(req, timeout=15):
                url = req.full_url
                method = req.get_method()
                actions.append((method, url.split("?")[0]))
                if url == updater.DEFAULT_IP_PROVIDERS[0]:
                    return _FakeHTTPResponse("198.51.100.20")
                if url.endswith("/api/v3/time"):
                    return _FakeHTTPResponse(json.dumps({"serverTime": 1700000000000}))
                if "/sapi/v1/sub-account/subAccountApi/ipRestriction" in url and method == "GET":
                    return _FakeHTTPResponse(
                        json.dumps(
                            {
                                "status": "2",
                                "ipList": ["198.51.100.10", "203.0.113.5"],
                                "apiKey": cfg.subaccount_api_key,
                            }
                        )
                    )
                if "/sapi/v2/sub-account/subAccountApi/ipRestriction" in url and method == "POST":
                    body = req.data.decode("utf-8")
                    self.assertIn("status=2", body)
                    self.assertIn("ipAddress=198.51.100.20", body)
                    return _FakeHTTPResponse(
                        json.dumps(
                            {
                                "status": "2",
                                "ipList": ["198.51.100.10", "203.0.113.5", "198.51.100.20"],
                                "apiKey": cfg.subaccount_api_key,
                            }
                        )
                    )
                if "/sapi/v1/sub-account/subAccountApi/ipRestriction/ipList" in url and method == "DELETE":
                    self.assertIn("ipAddress=198.51.100.10", url)
                    return _FakeHTTPResponse(
                        json.dumps(
                            {
                                "status": "2",
                                "ipList": ["203.0.113.5", "198.51.100.20"],
                                "apiKey": cfg.subaccount_api_key,
                            }
                        )
                    )
                if "api.telegram.org" in url:
                    return _FakeHTTPResponse(json.dumps({"ok": True}))
                raise AssertionError(f"Unexpected request: {method} {url}")

            with patch("urllib.request.urlopen", side_effect=fake_urlopen):
                res = updater.run_once(cfg)

            self.assertEqual(res["status"], "updated")
            self.assertEqual(res["mode"], "subaccount")
            self.assertEqual(res["final_ip_list"], ["203.0.113.5", "198.51.100.20"])

            # Verify POST happened before DELETE
            post_idx = next(i for i, (m, _) in enumerate(actions) if m == "POST")
            del_idx = next(i for i, (m, _) in enumerate(actions) if m == "DELETE")
            self.assertLess(post_idx, del_idx)

            saved = updater.load_state(state_path)
            self.assertEqual(saved["last_ip"], "198.51.100.20")
            self.assertEqual(saved["last_binance_ip_list"], ["203.0.113.5", "198.51.100.20"])

    def test_run_once_master_alert_mode_on_ip_change(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state_path = Path(tmpdir) / "state.json"
            updater.save_state(state_path, {"last_ip": "198.51.100.10"})

            cfg = updater.UpdaterConfig(
                mode="auto",
                bot_name="MasterBot",
                live_api_key="live_key_1234567890",
                live_api_secret="live_secret_1234567890",
                telegram_token="tg_token",
                telegram_chat_id="12345",
                state_file=state_path,
            )

            sent_payloads: list[str] = []

            def fake_urlopen(req, timeout=15):
                url = req.full_url
                if url == updater.DEFAULT_IP_PROVIDERS[0]:
                    return _FakeHTTPResponse("198.51.100.99")
                if url.endswith("/api/v3/time"):
                    return _FakeHTTPResponse(json.dumps({"serverTime": 1700000000000}))
                if "/sapi/v1/account/apiRestrictions" in url:
                    err_body = json.dumps(
                        {"code": -2015, "msg": "Invalid API-key, IP, or permissions for action."}
                    ).encode("utf-8")
                    raise urllib.error.HTTPError(
                        url, 401, "Unauthorized", {}, io.BytesIO(err_body)
                    )
                if "api.telegram.org" in url:
                    sent_payloads.append(req.data.decode("utf-8"))
                    return _FakeHTTPResponse(json.dumps({"ok": True}))
                raise AssertionError(f"Unexpected request: {url}")

            with patch("urllib.request.urlopen", side_effect=fake_urlopen):
                res = updater.run_once(cfg)

            self.assertEqual(res["mode"], "alert")
            self.assertEqual(res["status"], "alerted")
            self.assertIn("blocked_ip", res["live_api_check"])
            self.assertEqual(len(sent_payloads), 1)
            self.assertIn("198.51.100.99", sent_payloads[0])

            saved = updater.load_state(state_path)
            self.assertEqual(saved["last_ip"], "198.51.100.99")

    def test_run_once_unchanged_skips_binance_and_telegram(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state_path = Path(tmpdir) / "state.json"
            updater.save_state(state_path, {"last_ip": "198.51.100.20"})
            cfg = updater.UpdaterConfig(state_file=state_path)

            with patch("urllib.request.urlopen", return_value=_FakeHTTPResponse("198.51.100.20")):
                res = updater.run_once(cfg)

            self.assertEqual(res["status"], "unchanged")

    def test_dry_run_does_not_mutate_state(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state_path = Path(tmpdir) / "state.json"
            updater.save_state(state_path, {"last_ip": "198.51.100.10"})
            cfg = updater.UpdaterConfig(
                mode="alert",
                state_file=state_path,
                dry_run=True,
                telegram_token="tg_token",
                telegram_chat_id="12345",
            )

            with patch("urllib.request.urlopen", return_value=_FakeHTTPResponse("198.51.100.25")):
                res = updater.run_once(cfg)

            self.assertEqual(res["status"], "dry_run")
            self.assertEqual(updater.load_state(state_path)["last_ip"], "198.51.100.10")

    def test_load_config_reads_env_file_with_fallbacks(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            env_path = Path(tmpdir) / ".env"
            env_path.write_text(
                "\n".join(
                    [
                        "FREQTRADE__BOT_NAME=NFI_Live",
                        "FREQTRADE__EXCHANGE__KEY=ft_api_key_9999",
                        "FREQTRADE__EXCHANGE__SECRET=ft_api_secret_9999",
                        "FREQTRADE__TELEGRAM__TOKEN=tg_tok_1",
                        "FREQTRADE__TELEGRAM__CHAT_ID=987654",
                        "BINANCE_MASTER_API_KEY=m_key_1",
                        "BINANCE_MASTER_API_SECRET=m_sec_1",
                        "BINANCE_SUBACCOUNT_EMAIL=bot@example.com",
                        "BINANCE_KEEP_IPS=1.1.1.1, invalid_ip, 8.8.8.8",
                    ]
                ),
                encoding="utf-8",
            )
            parser = updater.build_arg_parser()
            args = parser.parse_args(["--env-file", str(env_path)])
            with patch.dict(os.environ, {}, clear=True):
                cfg = updater.load_config(args)

            self.assertEqual(cfg.bot_name, "NFI_Live")
            self.assertEqual(cfg.subaccount_api_key, "ft_api_key_9999")
            self.assertEqual(cfg.telegram_token, "tg_tok_1")
            self.assertEqual(cfg.telegram_chat_id, "987654")
            self.assertEqual(cfg.resolved_mode(), "subaccount")
            self.assertEqual(cfg.keep_ips, ["1.1.1.1", "8.8.8.8"])

    def test_periodic_reconcile_readds_missing_ip_in_subaccount_mode(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state_path = Path(tmpdir) / "state.json"
            updater.save_state(state_path, {"last_ip": "198.51.100.20"})
            cfg = updater.UpdaterConfig(
                mode="subaccount",
                master_api_key="m_key",
                master_api_secret="m_secret",
                subaccount_email="sub@example.com",
                subaccount_api_key="sub_key",
                state_file=state_path,
                notify_telegram=False,
            )

            post_called = False

            def fake_urlopen(req, timeout=15):
                nonlocal post_called
                url = req.full_url
                method = req.get_method()
                if url == updater.DEFAULT_IP_PROVIDERS[0]:
                    return _FakeHTTPResponse("198.51.100.20")
                if url.endswith("/api/v3/time"):
                    return _FakeHTTPResponse(json.dumps({"serverTime": 1700000000000}))
                if "/sapi/v1/sub-account/subAccountApi/ipRestriction" in url and method == "GET":
                    # IP was removed externally on Binance
                    return _FakeHTTPResponse(json.dumps({"status": "2", "ipList": []}))
                if "/sapi/v2/sub-account/subAccountApi/ipRestriction" in url and method == "POST":
                    post_called = True
                    return _FakeHTTPResponse(json.dumps({"status": "2", "ipList": ["198.51.100.20"]}))
                raise AssertionError(f"Unexpected request: {method} {url}")

            with patch("urllib.request.urlopen", side_effect=fake_urlopen):
                res = updater.run_once(cfg, reconcile=True)

            self.assertTrue(post_called)
            self.assertEqual(res["status"], "updated")
            self.assertEqual(res["final_ip_list"], ["198.51.100.20"])

    def test_periodic_reconcile_alert_mode_only_alerts_when_blocked(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            state_path = Path(tmpdir) / "state.json"
            updater.save_state(state_path, {"last_ip": "198.51.100.20"})
            cfg = updater.UpdaterConfig(
                mode="alert",
                live_api_key="live_key_123456",
                live_api_secret="live_sec_123456",
                telegram_token="tg_tok",
                telegram_chat_id="123",
                state_file=state_path,
            )

            def fake_ok(req, timeout=15):
                url = req.full_url
                if url == updater.DEFAULT_IP_PROVIDERS[0]:
                    return _FakeHTTPResponse("198.51.100.20")
                if url.endswith("/api/v3/time"):
                    return _FakeHTTPResponse(json.dumps({"serverTime": 1700000000000}))
                if "/sapi/v1/account/apiRestrictions" in url:
                    return _FakeHTTPResponse(json.dumps({"ipRestrict": True}))
                raise AssertionError(f"Should not send Telegram when OK: {url}")

            with patch("urllib.request.urlopen", side_effect=fake_ok):
                res = updater.run_once(cfg, reconcile=True)
            self.assertEqual(res["status"], "reconciled_ok")

    def test_periodic_loop_backoff_alert_and_recovery(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            cfg = updater.UpdaterConfig(
                mode="alert",
                bot_name="WatchBot",
                state_file=Path(tmpdir) / "state.json",
                telegram_token="tg_tok",
                telegram_chat_id="123",
                check_interval=60,
                reconcile_every=0,
                retry_delay=10,
                max_consecutive_errors=2,
            )

            outcomes = [
                RuntimeError("net err 1"),
                RuntimeError("net err 2"),
                {"status": "unchanged", "current_ip": "203.0.113.10"},
            ]
            tg_messages: list[str] = []
            sleep_calls: list[float] = []

            def fake_run_once(_cfg, reconcile=False):
                item = outcomes.pop(0)
                if isinstance(item, Exception):
                    raise item
                return item

            def fake_tg(_tok, _chat, msg, _timeout=15):
                tg_messages.append(msg)
                return True

            with (
                patch.object(updater, "run_once", side_effect=fake_run_once),
                patch.object(updater, "send_telegram_message", side_effect=fake_tg),
            ):
                rc = updater.run_periodic_loop(
                    cfg,
                    max_cycles=3,
                    sleep_fn=lambda s: sleep_calls.append(s),
                    stop_check=lambda: False,
                )

            self.assertEqual(rc, 0)
            # First failure waits 10s, second failure waits 20s (10 * 2^1), 3rd cycle stops
            self.assertEqual(sum(sleep_calls), 30)
            self.assertEqual(len(tg_messages), 2)
            self.assertIn("Consecutive Errors (2)", tg_messages[0])
            self.assertIn("Recovered", tg_messages[1])

    def test_cron_and_systemd_helpers(self):
        self.assertEqual(updater._interval_to_cron_schedule(300), "*/5 * * * *")
        self.assertEqual(updater._interval_to_cron_schedule(3600), "0 */1 * * *")
        self.assertEqual(updater._interval_to_cron_schedule(86400), "0 0 * * *")

        existing = "0 2 * * * /usr/bin/backup.sh\n"
        entry1 = "*/5 * * * * echo old # binance-ip-whitelist-updater"
        entry2 = "*/10 * * * * echo new # binance-ip-whitelist-updater"

        with_first = updater._upsert_cron_entry(existing, entry1)
        self.assertIn(entry1, with_first)
        self.assertIn("/usr/bin/backup.sh", with_first)

        with_second = updater._upsert_cron_entry(with_first, entry2)
        self.assertNotIn(entry1, with_second)
        self.assertIn(entry2, with_second)
        self.assertIn("/usr/bin/backup.sh", with_second)

        removed = updater._remove_cron_entry(with_second)
        self.assertEqual(removed, existing)

        parser = updater.build_arg_parser()
        args = parser.parse_args(["--print-systemd", "--interval", "180"])
        cfg = updater.UpdaterConfig(bot_name="UnitBot", check_interval=180, reconcile_every=1800)
        unit = updater.render_systemd_unit(args, cfg)
        self.assertIn("--watch --interval 180 --reconcile-every 1800", unit)
        self.assertIn("Restart=always", unit)


if __name__ == "__main__":
    unittest.main()
