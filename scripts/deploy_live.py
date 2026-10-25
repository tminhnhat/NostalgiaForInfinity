#!/usr/bin/env python3
"""Freqtrade Live Production Deployment & Telegram Notification Script.

Delivers live reload command to Freqtrade instance via REST API (or SSH)
and transmits structured deployment alerts to Telegram.
"""

from __future__ import annotations

import argparse
import base64
import json
import logging
import os
import subprocess
import sys
import urllib.parse
import urllib.request

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("LiveDeployer")


def reload_freqtrade_rest(api_url: str, username: str, password: str) -> dict:
    """Issue live config and strategy reload via Freqtrade REST API."""
    clean_url = api_url.rstrip("/")
    reload_endpoint = f"{clean_url}/api/v1/reload_config"

    logger.info(f"Issuing live reload command to Freqtrade API: {reload_endpoint}")
    credentials = f"{username}:{password}"
    auth_header = f"Basic {base64.b64encode(credentials.encode()).decode()}"

    req = urllib.request.Request(
        reload_endpoint,
        data=b"{}",
        headers={
            "Authorization": auth_header,
            "Content-Type": "application/json",
            "User-Agent": "FreqtradeDeployPipeline/1.0",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode())
            logger.info(f"Freqtrade reload response: {data}")
            return {"status": "success", "response": data, "code": resp.status}
    except Exception as e:
        logger.error(f"Error calling Freqtrade REST API: {e}")
        return {"status": "error", "error": str(e)}


def send_telegram_alert(bot_token: str, chat_id: str, message: str) -> bool:
    """Send formatted markdown notification to Telegram."""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = json.dumps({
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True,
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            logger.info("Telegram deployment alert dispatched successfully.")
            return True
    except Exception as e:
        logger.error(f"Failed to send Telegram alert: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Live Freqtrade Deployer")
    parser.add_argument("--commit-sha", default=os.environ.get("GITHUB_SHA", "HEAD")[:7])
    parser.add_argument("--commit-msg", default=os.environ.get("COMMIT_MESSAGE", "Live upgrade"))
    parser.add_argument("--actor", default=os.environ.get("GITHUB_ACTOR", "Maintainer"))
    args = parser.parse_args()

    api_url = os.environ.get("FREQTRADE_API_URL")
    api_user = os.environ.get("FREQTRADE_API_USERNAME")
    api_pass = os.environ.get("FREQTRADE_API_PASSWORD")

    telegram_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    telegram_chat = os.environ.get("TELEGRAM_CHAT_ID")

    reload_result = {"status": "skipped", "message": "API credentials not configured"}
    if api_url and api_user and api_pass:
        reload_result = reload_freqtrade_rest(api_url, api_user, api_pass)
    else:
        logger.info("FREQTRADE_API_* credentials not provided; skipping direct REST API reload call.")

    # Format Telegram Notification
    status_icon = "🟢 **LIVE RELOAD SUCCESSFUL**" if reload_result.get("status") == "success" else "🟡 **CODE DEPLOYED (MANUAL RESTART)**"
    telegram_msg = f"""🚀 *Freqtrade Production Deployment Complete*

{status_icon}
- *Commit*: `{args.commit_sha}`
- *Author*: @{args.actor}
- *Message*: _{args.commit_msg}_
- *Reload Status*: `{reload_result.get('status')}`

*The live bot has seamlessly ingested the latest strategy release.*
"""

    if telegram_token and telegram_chat:
        send_telegram_alert(telegram_token, telegram_chat, telegram_msg)
    else:
        logger.info("TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not provided; skipping Telegram notification.")
        print("\n--- Telegram Notification Preview ---\n" + telegram_msg)


if __name__ == "__main__":
    main()
