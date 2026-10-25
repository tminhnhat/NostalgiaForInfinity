#!/usr/bin/env python3
"""Automated Daily Evaluation Backtest Runner.

Executes rolling-window Freqtrade backtesting directly on the runner,
exports detailed metrics, and prints executive summary.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import os
from pathlib import Path
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def main():
    parser = argparse.ArgumentParser(description="Run evaluation backtest")
    parser.add_argument("--strategy", type=str, default="NostalgiaForInfinityX8")
    parser.add_argument("--days", type=int, default=30)
    parser.add_argument("--config", type=Path, default=Path("configs/exampleconfig.json"))
    parser.add_argument("--pairlist", type=Path, default=Path("configs/eval_pairs.json"))
    args = parser.parse_args()

    now_utc = datetime.now(timezone.utc)
    start_date = (now_utc - timedelta(days=args.days)).strftime("%Y%m%d")
    end_date = now_utc.strftime("%Y%m%d")
    timerange = f"{start_date}-{end_date}"

    print(f"🎯 Evaluation Window: {timerange} ({args.days} days)")
    print(f"🚀 Strategy: {args.strategy}")

    # Build backtesting command
    cmd = [
        "freqtrade",
        "backtesting",
        "--config", str(args.config),
        "--config", str(args.pairlist),
        "--strategy", args.strategy,
        "--strategy-path", ".",
        "--timerange", timerange,
        "--timeframe", "5m",
        "--export", "trades",
        "--breakdown", "day",
    ]

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
                if any(k in line for k in ["Win Rate", "Sharpe", "Sortino", "Max Drawdown", "Profit Factor", "Total Profit", "Longest Loss Streak"]):
                    print(line.strip())
        print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
