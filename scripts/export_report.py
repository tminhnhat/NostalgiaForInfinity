#!/usr/bin/env python3
"""Export Freqtrade Backtest Results into History JSON and Latest Markdown Report.

Generates:
1. reports/history/backtest_<YYYYMMDD>.json
2. reports/latest_report.md (Structured metrics table: Winrate, Sharpe, Sortino,
   Max Drawdown %, Profit Factor, Longest Loss Streak, and Tag breakdown)
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import logging
from pathlib import Path
import zipfile

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("ExportReport")


def find_latest_result(results_dir: Path) -> Path:
    """Find newest .zip or .json backtest result file."""
    candidates = list(results_dir.glob("backtest-result-*.zip")) + list(results_dir.glob("backtest-result-*.json"))
    candidates = [c for c in candidates if not c.name.endswith(".meta.json")]
    if not candidates:
        raise FileNotFoundError(f"No backtest result files found in {results_dir}")
    return max(candidates, key=lambda p: p.stat().st_mtime)


def load_backtest_data(file_path: Path) -> dict:
    if file_path.suffix == ".zip":
        with zipfile.ZipFile(file_path) as z:
            json_candidates = [
                n for n in z.namelist()
                if n.endswith(".json") and not n.endswith("_config.json") and not n.endswith(".meta.json")
            ]
            if not json_candidates:
                raise ValueError(f"No valid backtest result JSON found in zip {file_path}")
            return json.loads(z.read(json_candidates[0]))
    elif file_path.suffix == ".json":
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        raise ValueError(f"Unsupported result format: {file_path}")


def extract_strategy_metrics(data: dict, target_strategy: str | None = None) -> tuple[str, dict]:
    strategies = data.get("strategy")
    if isinstance(strategies, dict):
        if target_strategy and target_strategy in strategies:
            strat_name = target_strategy
        else:
            strat_name = next(iter(strategies))
        strat_data = strategies[strat_name]
    elif target_strategy and target_strategy in data:
        strat_name = target_strategy
        strat_data = data[strat_name]
    else:
        strat_name = list(data.keys())[0]
        strat_data = data[strat_name]

    return strat_name, strat_data


def generate_markdown(strat_name: str, s: dict, date_str: str) -> str:
    winrate = s.get("winrate", 0.0) * 100
    sharpe = s.get("sharpe", 0.0) or 0.0
    sortino = s.get("sortino", 0.0) or 0.0
    max_dd = (s.get("max_drawdown_account", 0.0) or 0.0) * 100
    profit_factor = s.get("profit_factor", 0.0) or 0.0
    longest_loss_streak = s.get("max_consecutive_losses", 0) or 0

    total_trades = s.get("total_trades", 0)
    profit_total = (s.get("profit_total", 0.0) or 0.0) * 100
    profit_total_abs = s.get("profit_total_abs", 0.0) or 0.0
    cagr = (s.get("cagr", 0.0) or 0.0) * 100
    calmar = s.get("calmar", 0.0) or 0.0
    expectancy = s.get("expectancy", 0.0) or 0.0
    trades_per_day = s.get("trades_per_day", 0.0) or 0.0
    timerange = s.get("timerange", "N/A")

    # Enter tag statistics
    tag_rows = []
    results_per_tag = s.get("results_per_enter_tag", {})
    if isinstance(results_per_tag, dict):
        # Sort by total profit ascending to immediately expose worst-performing conditions
        sorted_tags = sorted(
            results_per_tag.items(),
            key=lambda x: x[1].get("profit_total_abs", 0.0) if isinstance(x[1], dict) else 0.0,
        )
        for tag, stats in sorted_tags[:15]:  # Top 15 worst/interesting tags
            t_trades = stats.get("total_trades", 0)
            t_winrate = (stats.get("winrate", 0.0) or 0.0) * 100
            t_profit_pct = (stats.get("profit_total", 0.0) or 0.0) * 100
            t_profit_abs = stats.get("profit_total_abs", 0.0) or 0.0
            tag_rows.append(
                f"| `{tag}` | {t_trades} | {t_winrate:.1f}% | {t_profit_pct:+.2f}% | {t_profit_abs:+.2f} USDT |"
            )

    tag_table = "\n".join(tag_rows) if tag_rows else "| None | - | - | - | - |"

    md = f"""# 📈 Freqtrade Automated Evaluation Report

- **Evaluation Date**: {date_str}
- **Strategy**: `{strat_name}`
- **Backtest Timerange**: `{timerange}`
- **Backtest Duration**: {s.get('backtest_days', 0)} days

## 🎯 Executive Performance Metrics

| Metric | Value | Status Benchmark |
| :--- | :--- | :--- |
| **Winrate** | **{winrate:.2f}%** | {'🟢 Robust' if winrate >= 80 else '🟡 Moderate' if winrate >= 65 else '🔴 Low'} |
| **Sharpe Ratio** | **{sharpe:.2f}** | {'🟢 Exceptional' if sharpe >= 3.0 else '🟡 Good' if sharpe >= 1.5 else '🔴 Low'} |
| **Sortino Ratio** | **{sortino:.2f}** | {'🟢 Excellent' if sortino >= 4.0 else '🟡 Moderate'} |
| **Max Drawdown %** | **{max_dd:.2f}%** | {'🟢 Defended' if max_dd <= 10 else '🟡 Watch' if max_dd <= 20 else '🔴 Severe'} |
| **Profit Factor** | **{profit_factor:.2f}** | {'🟢 High' if profit_factor >= 2.0 else '🟡 Acceptable' if profit_factor >= 1.2 else '🔴 Unfavorable'} |
| **Longest Loss Streak** | **{longest_loss_streak} trades** | {'🟢 Safe' if longest_loss_streak <= 3 else '🟡 Elevated' if longest_loss_streak <= 6 else '🔴 Critical'} |

---

## 📊 Secondary Quantitative Indicators

| Metric | Result | Description |
| :--- | :--- | :--- |
| **Total Trades** | `{total_trades}` | Cumulative trade executions |
| **Net Profit %** | `{profit_total:+.2f}%` | Total percentage portfolio return |
| **Net Profit Abs** | `{profit_total_abs:+.2f} USDT` | Absolute profit generated |
| **Trades Per Day** | `{trades_per_day:.2f}` | Trade turnover density |
| **Expectancy** | `{expectancy:.4f}` | Mathematical expectancy per trade |
| **Calmar Ratio** | `{calmar:.2f}` | Return-to-max-drawdown ratio |
| **CAGR** | `{cagr:.2f}%` | Compound Annual Growth Rate |

---

## 🔍 Condition Diagnostics (Underperforming & Active Tags)

| Enter Tag | Trades | Winrate | Total Profit % | Profit (USDT) |
| :--- | :--- | :--- | :--- | :--- |
{tag_table}

---
*Report automatically generated by `scripts/export_report.py` for Closed-Loop Agentic Optimization.*
"""
    return md


def main():
    parser = argparse.ArgumentParser(description="Export Freqtrade backtest report to JSON & Markdown")
    parser.add_argument("--result-file", type=Path, default=None, help="Path to backtest zip or json")
    parser.add_argument("--results-dir", type=Path, default=Path("user_data/backtest_results"), help="Results directory")
    parser.add_argument("--strategy", type=str, default=None, help="Strategy name")
    parser.add_argument("--output-json", type=Path, default=None, help="Destination for historical json")
    parser.add_argument("--output-md", type=Path, default=Path("reports/latest_report.md"), help="Destination markdown")
    args = parser.parse_args()

    result_file = args.result_file or find_latest_result(args.results_dir)
    logger.info(f"Processing backtest result file: {result_file}")

    data = load_backtest_data(result_file)
    strat_name, strat_metrics = extract_strategy_metrics(data, args.strategy)

    date_str = datetime.now(timezone.utc).strftime("%Y%m%d")
    date_display = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    # Destination paths
    history_dir = Path("reports/history")
    history_dir.mkdir(parents=True, exist_ok=True)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)

    json_dest = args.output_json or (history_dir / f"backtest_{date_str}.json")

    # 1. Save normalized historical JSON
    compact_history = {
        "strategy": strat_name,
        "date": date_str,
        "source_file": result_file.name,
        "metrics": {
            "winrate": strat_metrics.get("winrate"),
            "sharpe": strat_metrics.get("sharpe"),
            "sortino": strat_metrics.get("sortino"),
            "max_drawdown_account": strat_metrics.get("max_drawdown_account"),
            "profit_factor": strat_metrics.get("profit_factor"),
            "max_consecutive_losses": strat_metrics.get("max_consecutive_losses"),
            "total_trades": strat_metrics.get("total_trades"),
            "profit_total": strat_metrics.get("profit_total"),
            "profit_total_abs": strat_metrics.get("profit_total_abs"),
            "expectancy": strat_metrics.get("expectancy"),
            "calmar": strat_metrics.get("calmar"),
        },
        "results_per_enter_tag": strat_metrics.get("results_per_enter_tag", {}),
        "exit_reason_summary": strat_metrics.get("exit_reason_summary", {}),
    }

    with open(json_dest, "w", encoding="utf-8") as f:
        json.dump(compact_history, f, indent=2)
    logger.info(f"Saved historical report: {json_dest}")

    # 2. Save Markdown Report
    md_content = generate_markdown(strat_name, strat_metrics, date_display)
    with open(args.output_md, "w", encoding="utf-8") as f:
        f.write(md_content)
    logger.info(f"Saved latest markdown report: {args.output_md}")


if __name__ == "__main__":
    main()
