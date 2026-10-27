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
os.environ["PYTHONUTF8"] = "1"


def main():
    parser = argparse.ArgumentParser(description="Run evaluation backtest")
    parser.add_argument("--strategy", type=str, default="NostalgiaForInfinityX8_Combined_AI")
    parser.add_argument("--days", type=int, default=None)
    parser.add_argument("--config", type=Path, default=Path("configs/backtest_config.json"))
    parser.add_argument("--pairlist", type=Path, default=None)
    parser.add_argument("--version", type=str, default=None, help="Strategy version tag")
    parser.add_argument("--commit-sha", type=str, default=None, help="Git commit SHA")
    parser.add_argument("--run-label", type=str, default=None, help="Run marker/label for differentiation")
    parser.add_argument("--run-id", type=str, default=None, help="GitHub Actions run ID")
    parser.add_argument("--run-url", type=str, default=None, help="GitHub Actions run URL")
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
    if args.version:
        print(f"🏷️ Version: {args.version}")
    if args.run_label:
        print(f"🔖 Run Marker: {args.run_label}")
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
    sub_env = dict(os.environ, PYTHONUTF8="1")
    result = subprocess.run(cmd, check=False, env=sub_env)
    if result.returncode != 0:
        print(f"❌ Backtest failed with code {result.returncode}")
        sys.exit(result.returncode)

    print("📊 Exporting metrics and generating reports/latest_report.md...")
    export_cmd = [sys.executable, "scripts/export_report.py", "--strategy", args.strategy]
    if args.version:
        export_cmd.extend(["--version", args.version])
    if args.commit_sha:
        export_cmd.extend(["--commit-sha", args.commit_sha])
    if args.run_label:
        export_cmd.extend(["--run-label", args.run_label])
    if args.run_id:
        export_cmd.extend(["--run-id", args.run_id])
    if args.run_url:
        export_cmd.extend(["--run-url", args.run_url])

    export_res = subprocess.run(export_cmd, check=False, env=sub_env)
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
