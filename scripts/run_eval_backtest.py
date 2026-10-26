#!/usr/bin/env python3
"""Automated Daily Evaluation Backtest Runner.

Executes rolling-window Freqtrade backtesting directly on the runner,
exports detailed metrics, and prints executive summary.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import json
import os
from pathlib import Path
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def main():
    parser = argparse.ArgumentParser(description="Run evaluation backtest")
    parser.add_argument("--strategy", type=str, default="NostalgiaForInfinityX8_Combined_AI")
    parser.add_argument("--days", type=int, default=None)
    parser.add_argument("--config", type=Path, default=Path("configs/backtest_config.json"))
    parser.add_argument("--pairlist", type=Path, default=None)
    args = parser.parse_args()

    days = 180
    if args.days is not None:
        days = args.days
    elif args.config and args.config.exists():
        try:
            with open(args.config, "r", encoding="utf-8") as f:
                cfg = json.load(f)
                days = int(cfg.get("backtest_days", 180))
        except Exception:
            days = 180

    now_utc = datetime.now(timezone.utc)
    start_date = (now_utc - timedelta(days=days)).strftime("%Y%m%d")
    end_date = now_utc.strftime("%Y%m%d")
    timerange = f"{start_date}-{end_date}"

    print(f"🎯 Evaluation Window: {timerange} ({days} days)")
    print(f"🚀 Strategy: {args.strategy}")
    print(f"⚙️ Config: {args.config}")

    # Build backtesting command
    cmd = [
        "freqtrade",
        "backtesting",
        "--config", str(args.config),
    ]

    if args.pairlist and args.pairlist.exists():
        cmd.extend(["--config", str(args.pairlist)])

    cmd.extend([
        "--strategy", args.strategy,
        "--strategy-path", ".",
        "--timerange", timerange,
        "--timeframe", "5m",
        "--export", "trades",
        "--breakdown", "day",
    ])

    print(f"Executing: {' '.join(cmd)}")
    result = subprocess.run(cmd, check=False)
    if result.returncode != 0:
        print(f"❌ Backtest failed with code {result.returncode}")
        sys.exit(result.returncode)

    print("📊 Exporting metrics and generating reports/latest_report.md...")
    export_cmd = [sys.executable, "scripts/export_report.py", "--strategy", args.strategy]
    export_res = subprocess.run(export_cmd, check=False)
    if export_res.returncode != 0:
        print(f"⚠️ Report export warning (code {export_res.returncode})")

    report_path = Path("reports/latest_report.md")
    if report_path.exists():
        print("\n" + "=" * 60)
        print("EXECUTIVE PERFORMANCE SUMMARY")
        print("=" * 60)
        with open(report_path, "r", encoding="utf-8") as f:
            for line in f:
                if any(k in line for k in ["Winrate", "Win Rate", "Sharpe", "Sortino", "Max Drawdown", "Sụt giảm", "Profit Factor", "Lợi nhuận", "Longest Loss Streak", "Chuỗi", "Tổng số lệnh"]):
                    if line.strip().startswith("|") and not line.strip().startswith("| :---"):
                        print(line.strip())
        print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
