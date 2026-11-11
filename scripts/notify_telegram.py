#!/usr/bin/env python3
"""Send Backtest Executive Report to Telegram.

Reads Telegram token and chat_id from environment or .env, extracts key
metrics from reports/latest_report.md, and pushes a notification + report document.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import sys
import urllib.parse
import urllib.request

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def load_env_credentials():
    token = os.environ.get("FREQTRADE__TELEGRAM__TOKEN")
    chat_id = os.environ.get("FREQTRADE__TELEGRAM__CHAT_ID")

    if not token or not chat_id:
        env_path = Path(".env")
        if env_path.exists():
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("FREQTRADE__TELEGRAM__TOKEN="):
                        token = line.split("=", 1)[1].strip().strip('"').strip("'")
                    elif line.startswith("FREQTRADE__TELEGRAM__CHAT_ID="):
                        chat_id = line.split("=", 1)[1].strip().strip('"').strip("'")
    return token, chat_id


def parse_report_metrics(report_path: Path) -> dict:
    metrics = {
        "strategy": "NostalgiaForInfinityX8_Combined_AI",
        "version": "v9.0",
        "run_marker": "Backtest_Eval",
        "timerange": "185 ngày",
        "winrate": "N/A",
        "profit_pct": "N/A",
        "profit_usdt": "N/A",
        "max_drawdown": "N/A",
        "sharpe": "N/A",
        "profit_factor": "N/A",
        "total_trades": "N/A",
    }
    if not report_path.exists():
        return metrics

    with open(report_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract version & marker
    m_ver = re.search(r"Phiên bản Chiến lược.*?`([^`]+)`", content)
    if m_ver:
        metrics["version"] = m_ver.group(1)

    m_marker = re.search(r"Đánh dấu lần chạy.*?`([^`]+)`", content)
    if m_marker:
        metrics["run_marker"] = m_marker.group(1)

    m_time = re.search(r"Cửa sổ Backtest.*?`([^`]+)`", content)
    if m_time:
        metrics["timerange"] = m_time.group(1)

    # Extract metrics from comparison table or summary table
    m_wr = re.search(r"\*\*Tỷ lệ thắng \(Winrate\)\*\*\s*\|\s*\*\*([^\*]+)\*\*", content)
    if m_wr:
        metrics["winrate"] = m_wr.group(1).strip()

    m_prof_pct = re.search(r"\*\*Lợi nhuận ròng \(Net Profit %\)\*\*\s*\|\s*\*\*([^\*]+)\*\*", content)
    if m_prof_pct:
        metrics["profit_pct"] = m_prof_pct.group(1).strip()

    m_prof_usdt = re.search(r"\*\*Lợi nhuận tuyệt đối \(USDT\)\*\*\s*\|\s*\*\*([^\*]+)\*\*", content)
    if m_prof_usdt:
        metrics["profit_usdt"] = m_prof_usdt.group(1).strip()

    m_dd = re.search(r"\*\*Sụt giảm tối đa \(Max Drawdown %\)\*\*\s*\|\s*\*\*([^\*]+)\*\*", content)
    if m_dd:
        metrics["max_drawdown"] = m_dd.group(1).strip()

    m_sharpe = re.search(r"\*\*Hệ số Sharpe \(Sharpe Ratio\)\*\*\s*\|\s*\*\*([^\*]+)\*\*", content)
    if m_sharpe:
        metrics["sharpe"] = m_sharpe.group(1).strip()

    m_pf = re.search(r"\*\*Hệ số lãi/lỗ \(Profit Factor\)\*\*\s*\|\s*\*\*([^\*]+)\*\*", content)
    if m_pf:
        metrics["profit_factor"] = m_pf.group(1).strip()

    m_trades = re.search(r"\*\*Tổng số lệnh \(Total Trades\)\*\*\s*\|\s*\*\*([^\*]+)\*\*", content)
    if m_trades:
        metrics["total_trades"] = m_trades.group(1).strip()

    return metrics


def send_telegram_message(token: str, chat_id: str, message: str) -> bool:
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": "true",
    }
    data = urllib.parse.urlencode(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.status == 200
    except Exception as e:
        print(f"⚠️ Telegram sendMessage failed: {e}")
        return False


def send_telegram_document(token: str, chat_id: str, file_path: Path, caption: str = "") -> bool:
    url = f"https://api.telegram.org/bot{token}/sendDocument"
    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"

    if not file_path.exists():
        return False

    with open(file_path, "rb") as f:
        file_bytes = f.read()

    body = bytearray()
    # chat_id field
    body.extend(f"--{boundary}\r\n".encode("utf-8"))
    body.extend(f'Content-Disposition: form-data; name="chat_id"\r\n\r\n{chat_id}\r\n'.encode("utf-8"))

    # caption field
    if caption:
        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend(f'Content-Disposition: form-data; name="caption"\r\n\r\n{caption}\r\n'.encode("utf-8"))

    # document field
    body.extend(f"--{boundary}\r\n".encode("utf-8"))
    body.extend(
        f'Content-Disposition: form-data; name="document"; filename="{file_path.name}"\r\n'.encode("utf-8")
    )
    body.extend(b"Content-Type: text/markdown; charset=utf-8\r\n\r\n")
    body.extend(file_bytes)
    body.extend(b"\r\n")
    body.extend(f"--{boundary}--\r\n".encode("utf-8"))

    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status == 200
    except Exception as e:
        print(f"⚠️ Telegram sendDocument failed: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Send backtest report to Telegram")
    parser.add_argument("--report", type=Path, default=Path("reports/latest_report.md"))
    parser.add_argument("--token", type=str, default=None)
    parser.add_argument("--chat-id", type=str, default=None)
    parser.add_argument("--attach-file", action="store_true", default=True)
    parser.add_argument("--context-title", type=str, default="🚀 BÁO CÁO BACKTEST TỰ ĐỘNG")
    args = parser.parse_args()

    token = args.token
    chat_id = args.chat_id
    if not token or not chat_id:
        env_token, env_chat_id = load_env_credentials()
        token = token or env_token
        chat_id = chat_id or env_chat_id

    if not token or not chat_id:
        print("⚠️ Telegram token hoặc chat_id chưa được thiết lập. Bỏ qua gửi thông báo.")
        return 0

    metrics = parse_report_metrics(args.report)

    msg_lines = [
        f"<b>{args.context_title}</b>",
        f"🏷️ <b>Chiến lược:</b> {metrics['strategy']} ({metrics['version']})",
        f"🔖 <b>Run Marker:</b> <code>{metrics['run_marker']}</code>",
        f"⏱️ <b>Khung đánh giá:</b> {metrics['timerange']}",
        "──────────────────────────────",
        f"🎯 <b>Tỷ lệ thắng (Winrate):</b> <b>{metrics['winrate']}</b>",
        f"💰 <b>Lợi nhuận ròng:</b> <b>{metrics['profit_usdt']}</b> ({metrics['profit_pct']})",
        f"📉 <b>Sụt giảm tối đa (DD):</b> <b>{metrics['max_drawdown']}</b>",
        f"⚡ <b>Hệ số Sharpe:</b> <b>{metrics['sharpe']}</b> | <b>Profit Factor:</b> <b>{metrics['profit_factor']}</b>",
        f"📊 <b>Tổng số lệnh:</b> <b>{metrics['total_trades']}</b>",
        "──────────────────────────────",
        "✅ <i>Báo cáo chi tiết đã được đính kèm bên dưới.</i>",
    ]
    message_text = "\n".join(msg_lines)

    print("📤 Đang gửi thông báo Telegram...")
    success = send_telegram_message(token, chat_id, message_text)
    if success:
        print("✅ Đã gửi tin nhắn tóm tắt qua Telegram thành công!")
        if args.attach_file and args.report.exists():
            print("📎 Đang đính kèm file báo cáo latest_report.md...")
            doc_success = send_telegram_document(
                token, chat_id, args.report, caption=f"📄 Báo cáo chi tiết: {metrics['run_marker']}"
            )
            if doc_success:
                print("✅ Đã gửi file báo cáo thành công!")
    else:
        print("❌ Gửi thông báo Telegram thất bại.")


if __name__ == "__main__":
    main()
