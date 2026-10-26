#!/usr/bin/env python3
"""Export Freqtrade Backtest Results into History JSON and Latest Comprehensive Markdown Report.

Generates:
1. reports/history/backtest_<YYYYMMDD_HHMMSS>.json (Chronological historical audit)
2. reports/latest_report.md (Detailed Markdown Report with full tags, trade analysis,
   comprehensive metrics, and benchmark comparison against the previous run)
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import logging
from pathlib import Path
import sys
import zipfile

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


def find_previous_run(history_dir: Path, current_source_file: str = "") -> dict | None:
    """Find the most recent preceding historical backtest record for benchmark comparison."""
    if not history_dir.exists():
        return None
    candidates = sorted([f for f in history_dir.glob("backtest_*.json") if not f.name.endswith(".meta.json")])
    if not candidates:
        return None

    # Filter out records that originate from the exact same backtest run
    valid_candidates = []
    for f in candidates:
        try:
            with open(f, "r", encoding="utf-8") as fp:
                rec = json.load(fp)
                if current_source_file and rec.get("source_file") == current_source_file:
                    continue
                valid_candidates.append(rec)
        except Exception:
            continue

    if valid_candidates:
        return valid_candidates[-1]
    return None


def format_delta(
    curr: float | None,
    prev: float | None,
    is_pct: bool = False,
    reverse_better: bool = False,
    unit: str = "",
) -> tuple[str, str]:
    """Calculate delta, formatted string, and trend indicator (🟢/🔴/⚪)."""
    if curr is None or prev is None:
        return "N/A", "⚪ Không rõ"
    diff = curr - prev
    if abs(diff) < 0.0001:
        return "0.00" + ( "%" if is_pct else "" ) + unit, "⚪ Tương đương"

    sign = "+" if diff > 0 else ""
    pct_sym = "%" if is_pct else ""
    delta_str = f"`{sign}{diff:,.2f}{pct_sym}{unit}`"

    improved = (diff < 0) if reverse_better else (diff > 0)
    trend = "🟢 Cải thiện" if improved else "🔴 Suy giảm"
    return delta_str, trend


def classify_tag_type(tag_name: str) -> str:
    """Classify tag into Long Core, Short Custom, or AI Gatekeeper Short."""
    tn = str(tag_name).strip()
    if "_AI_PASS" in tn:
        return "🤖 Short AI Gatekeeper"
    if tn.startswith("7") or "short" in tn.lower():
        return "🔴 Short Custom"
    return "🟢 Long Core"


def generate_comparison_table(curr_metrics: dict, prev_metrics: dict | None, prev_date_str: str = "") -> str:
    """Generate Markdown comparison table between current run and previous run."""
    if not prev_metrics:
        return (
            "## ⚖️ So Sánh Hiệu Suất Với Lần Backtest Trước (Benchmark Comparison)\n\n"
            "> [!NOTE]\n"
            "> *Chưa có dữ liệu lần chạy trước trong lịch sử để đối chiếu. Đây là phiên chạy mốc chuẩn (Baseline Run).*\n"
        )

    prev_m = prev_metrics.get("metrics", prev_metrics)

    c_winrate = (curr_metrics.get("winrate", 0.0) or 0.0) * 100
    p_winrate = (prev_m.get("winrate", 0.0) or 0.0) * 100
    d_winrate, t_winrate = format_delta(c_winrate, p_winrate, is_pct=True)

    c_profit_pct = (curr_metrics.get("profit_total", 0.0) or 0.0) * 100
    p_profit_pct = (prev_m.get("profit_total", 0.0) or 0.0) * 100
    d_profit_pct, t_profit_pct = format_delta(c_profit_pct, p_profit_pct, is_pct=True)

    c_profit_abs = curr_metrics.get("profit_total_abs", 0.0) or 0.0
    p_profit_abs = prev_m.get("profit_total_abs", 0.0) or 0.0
    d_profit_abs, t_profit_abs = format_delta(c_profit_abs, p_profit_abs, unit=" USDT")

    c_sharpe = curr_metrics.get("sharpe", 0.0) or 0.0
    p_sharpe = prev_m.get("sharpe", 0.0) or 0.0
    d_sharpe, t_sharpe = format_delta(c_sharpe, p_sharpe)

    c_sortino = curr_metrics.get("sortino", 0.0) or 0.0
    p_sortino = prev_m.get("sortino", 0.0) or 0.0
    d_sortino, t_sortino = format_delta(c_sortino, p_sortino)

    c_max_dd = (curr_metrics.get("max_drawdown_account", 0.0) or 0.0) * 100
    p_max_dd = (prev_m.get("max_drawdown_account", 0.0) or 0.0) * 100
    d_max_dd, t_max_dd = format_delta(c_max_dd, p_max_dd, is_pct=True, reverse_better=True)

    c_profit_factor = curr_metrics.get("profit_factor", 0.0) or 0.0
    p_profit_factor = prev_m.get("profit_factor", 0.0) or 0.0
    d_profit_factor, t_profit_factor = format_delta(c_profit_factor, p_profit_factor)

    c_trades = curr_metrics.get("total_trades", 0) or 0
    p_trades = prev_m.get("total_trades", 0) or 0
    d_trades, t_trades = format_delta(c_trades, p_trades, unit=" lệnh")

    c_loss_streak = curr_metrics.get("max_consecutive_losses", 0) or 0
    p_loss_streak = prev_m.get("max_consecutive_losses", 0) or 0
    d_loss_streak, t_loss_streak = format_delta(c_loss_streak, p_loss_streak, reverse_better=True, unit=" lệnh")

    c_expectancy = curr_metrics.get("expectancy", 0.0) or 0.0
    p_expectancy = prev_m.get("expectancy", 0.0) or 0.0
    d_expectancy, t_expectancy = format_delta(c_expectancy, p_expectancy)

    c_calmar = curr_metrics.get("calmar", 0.0) or 0.0
    p_calmar = prev_m.get("calmar", 0.0) or 0.0
    d_calmar, t_calmar = format_delta(c_calmar, p_calmar)

    date_label = f" ({prev_date_str})" if prev_date_str else " (Previous)"

    return f"""## ⚖️ So Sánh Hiệu Suất Với Lần Backtest Trước (Benchmark Comparison)

| Chỉ số định lượng | Lần chạy này (Current) | Lần chạy trước{date_label} | Chênh lệch (Δ Delta) | Xu hướng |
| :--- | :--- | :--- | :--- | :--- |
| **Tỷ lệ thắng (Winrate)** | **{c_winrate:.2f}%** | **{p_winrate:.2f}%** | {d_winrate} | {t_winrate} |
| **Lợi nhuận ròng (Net Profit %)** | **{c_profit_pct:+.2f}%** | **{p_profit_pct:+.2f}%** | {d_profit_pct} | {t_profit_pct} |
| **Lợi nhuận tuyệt đối (USDT)** | **{c_profit_abs:+,.2f} USDT** | **{p_profit_abs:+,.2f} USDT** | {d_profit_abs} | {t_profit_abs} |
| **Hệ số Sharpe (Sharpe Ratio)** | **{c_sharpe:.2f}** | **{p_sharpe:.2f}** | {d_sharpe} | {t_sharpe} |
| **Hệ số Sortino (Sortino Ratio)** | **{c_sortino:.2f}** | **{p_sortino:.2f}** | {d_sortino} | {t_sortino} |
| **Sụt giảm tối đa (Max Drawdown %)** | **{c_max_dd:.2f}%** | **{p_max_dd:.2f}%** | {d_max_dd} | {t_max_dd} |
| **Hệ số lãi/lỗ (Profit Factor)** | **{c_profit_factor:.2f}** | **{p_profit_factor:.2f}** | {d_profit_factor} | {t_profit_factor} |
| **Tổng số lệnh (Total Trades)** | **{c_trades}** | **{p_trades}** | {d_trades} | {t_trades} |
| **Chuỗi lệnh thua dài nhất** | **{c_loss_streak} trades** | **{p_loss_streak} trades** | {d_loss_streak} | {t_loss_streak} |
| **Kỳ vọng toán học (Expectancy)** | **{c_expectancy:.4f}** | **{p_expectancy:.4f}** | {d_expectancy} | {t_expectancy} |
| **Hệ số Calmar (Calmar Ratio)** | **{c_calmar:.2f}** | **{p_calmar:.2f}** | {d_calmar} | {t_calmar} |
"""


def generate_markdown(
    strat_name: str,
    s: dict,
    date_display: str,
    source_filename: str,
    prev_run: dict | None,
) -> str:
    """Generate exhaustive Markdown backtest report."""
    winrate = (s.get("winrate", 0.0) or 0.0) * 100
    sharpe = s.get("sharpe", 0.0) or 0.0
    sortino = s.get("sortino", 0.0) or 0.0
    max_dd = (s.get("max_drawdown_account", 0.0) or 0.0) * 100
    max_dd_abs = s.get("max_drawdown_abs", 0.0) or 0.0
    profit_factor = s.get("profit_factor", 0.0) or 0.0
    longest_loss_streak = s.get("max_consecutive_losses", 0) or 0

    total_trades = s.get("total_trades", 0) or 0
    profit_total = (s.get("profit_total", 0.0) or 0.0) * 100
    profit_total_abs = s.get("profit_total_abs", 0.0) or 0.0
    cagr = (s.get("cagr", 0.0) or 0.0) * 100
    calmar = s.get("calmar", 0.0) or 0.0
    expectancy = s.get("expectancy", 0.0) or 0.0
    trades_per_day = s.get("trades_per_day", 0.0) or 0.0
    timerange = s.get("timerange", "N/A")
    backtest_days = s.get("backtest_days", 0)

    trades = s.get("trades", [])

    # Trade counts
    wins_count = len([t for t in trades if t.get("profit_ratio", 0) > 0]) if trades else int(round(total_trades * (winrate / 100)))
    draws_count = len([t for t in trades if abs(t.get("profit_ratio", 0)) < 1e-6]) if trades else 0
    losses_count = total_trades - wins_count - draws_count
    avg_profit_per_trade = (profit_total_abs / total_trades) if total_trades > 0 else 0.0

    # 1. Comparison Section
    prev_date = prev_run.get("date", "") if prev_run else ""
    comparison_section = generate_comparison_table(s, prev_run, prev_date)

    # 2. Position Breakdown (Long vs Short)
    long_trades = [t for t in trades if not t.get("is_short", False)]
    short_trades = [t for t in trades if t.get("is_short", False)]

    pos_table = ""
    if trades:
        l_cnt = len(long_trades)
        l_wins = len([t for t in long_trades if t.get("profit_ratio", 0) > 0])
        l_wr = (l_wins / l_cnt * 100) if l_cnt else 0.0
        l_profit_abs = sum(t.get("profit_abs", 0.0) for t in long_trades)
        l_profit_pct = sum(t.get("profit_ratio", 0.0) for t in long_trades) * 100

        s_cnt = len(short_trades)
        s_wins = len([t for t in short_trades if t.get("profit_ratio", 0) > 0])
        s_wr = (s_wins / s_cnt * 100) if s_cnt else 0.0
        s_profit_abs = sum(t.get("profit_abs", 0.0) for t in short_trades)
        s_profit_pct = sum(t.get("profit_ratio", 0.0) for t in short_trades) * 100

        pos_table = f"""## ⚔️ Thống Kê Phân Bổ Vị Thế (Long vs Short Performance)

| Vị thế (Position) | Số lệnh | Tỷ trọng | Tỷ lệ thắng (Winrate) | Lợi nhuận (USDT) | Lợi nhuận (%) | Đánh giá |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 **Lệnh Mua (Long)** | `{l_cnt}` | {l_cnt/total_trades*100:.1f}% | **{l_wr:.2f}%** | **{l_profit_abs:+,.2f} USDT** | {l_profit_pct:+.2f}% | {'🟢 Vượt trội' if l_wr >= 80 else '🟡 Tốt'} |
| 🔴 **Lệnh Bán (Short)** | `{s_cnt}` | {s_cnt/total_trades*100:.1f}% | **{s_wr:.2f}%** | **{s_profit_abs:+,.2f} USDT** | {s_profit_pct:+.2f}% | {'🟢 Vượt trội' if s_wr >= 80 else '🟡 Tốt'} |
| 🌐 **Toàn bộ danh mục** | `{total_trades}` | 100.0% | **{winrate:.2f}%** | **{profit_total_abs:+,.2f} USDT** | {profit_total:+.2f}% | 🎯 Hoàn tất |
"""

    # 3. Exit Reason Analysis
    exit_table = ""
    exit_summary = s.get("exit_reason_summary", {})
    exit_items = []
    if isinstance(exit_summary, dict):
        exit_items = list(exit_summary.items())
    elif isinstance(exit_summary, list):
        for item in exit_summary:
            if isinstance(item, dict):
                r_key = item.get("key") or item.get("exit_reason") or "unknown"
                exit_items.append((r_key, item))

    # If exit_summary not directly in strategy dict, calculate from trades
    if not exit_items and trades:
        reasons_map: dict[str, dict] = {}
        for t in trades:
            r = t.get("exit_reason") or "unknown"
            if r not in reasons_map:
                reasons_map[r] = {"trades": 0, "wins": 0, "profit_abs": 0.0, "profit_ratio": 0.0}
            reasons_map[r]["trades"] += 1
            if t.get("profit_ratio", 0) > 0:
                reasons_map[r]["wins"] += 1
            reasons_map[r]["profit_abs"] += t.get("profit_abs", 0.0)
            reasons_map[r]["profit_ratio"] += t.get("profit_ratio", 0.0)
        exit_items = list(reasons_map.items())

    if exit_items:
        exit_rows = []
        for r_name, r_stats in sorted(exit_items, key=lambda x: x[1].get("trades", 0) if isinstance(x[1], dict) else 0, reverse=True):
            r_cnt = r_stats.get("trades") or r_stats.get("total_trades") or 0
            r_wins = r_stats.get("wins") or 0
            r_wr = (r_stats.get("winrate", 0.0) or (r_wins / r_cnt if r_cnt else 0.0)) * 100
            r_p_abs = r_stats.get("profit_total_abs", r_stats.get("profit_abs", 0.0)) or 0.0
            r_share = (r_cnt / total_trades * 100) if total_trades else 0.0
            exit_rows.append(f"| `{r_name}` | `{r_cnt}` | {r_share:.1f}% | **{r_wr:.1f}%** | {r_p_abs:+,.2f} USDT |")

        exit_table = f"""## 🚪 Phân Tích Lý Do Thoát Lệnh (Exit Reason Breakdown)

| Lý do đóng lệnh (Exit Reason) | Số lệnh | Tỷ trọng | Tỷ lệ thắng (Winrate) | Lợi nhuận (USDT) |
| :--- | :--- | :--- | :--- | :--- |
""" + "\n".join(exit_rows) + "\n"

    # 4. ALL Entry Tags Breakdown (No truncation!)
    tag_rows = []
    results_per_tag = s.get("results_per_enter_tag", {})
    tag_items = []
    if isinstance(results_per_tag, dict):
        tag_items = list(results_per_tag.items())
    elif isinstance(results_per_tag, list):
        for item in results_per_tag:
            if isinstance(item, dict):
                tag_name = item.get("key") or item.get("tag") or item.get("enter_tag") or "unknown"
                tag_items.append((tag_name.strip(), item))

    if tag_items:
        # Sort by total profit abs descending (best performing to worst)
        sorted_tags = sorted(
            tag_items,
            key=lambda x: x[1].get("profit_total_abs", 0.0) if isinstance(x[1], dict) else 0.0,
            reverse=True,
        )
        for tag, stats in sorted_tags:
            t_trades = stats.get("total_trades") or stats.get("trades") or 0
            t_wins = stats.get("wins") or 0
            t_losses = stats.get("losses") or 0
            t_draws = stats.get("draws") or 0
            t_winrate = (stats.get("winrate", 0.0) or 0.0) * 100
            t_profit_pct = (stats.get("profit_total", 0.0) or 0.0) * 100
            t_profit_abs = stats.get("profit_total_abs", 0.0) or 0.0
            t_mean_pct = stats.get("profit_mean_pct", stats.get("profit_mean", 0.0) * 100) or 0.0
            t_dur = stats.get("duration_avg", "N/A")
            t_type = classify_tag_type(tag)

            if t_winrate >= 80.0 and t_profit_abs > 0:
                status = "🟢 Tối ưu"
            elif t_winrate >= 60.0 and t_profit_abs > 0:
                status = "🟡 Hiệu quả"
            elif t_profit_abs <= 0:
                status = "🔴 Cần tinh chỉnh"
            else:
                status = "⚪ Theo dõi"

            tag_rows.append(
                f"| `{tag}` | {t_type} | `{t_trades}` | **{t_winrate:.1f}%** | {t_wins}/{t_draws}/{t_losses} | {t_profit_pct:+.2f}% | **{t_profit_abs:+,.2f} USDT** | {t_mean_pct:+.2f}% | {t_dur} | {status} |"
            )

    tag_table = "\n".join(tag_rows) if tag_rows else "| `N/A` | - | - | - | - | - | - | - | - | - |"

    # 5. Top Winning, Top Drawdown & Recent Trade Journal
    trade_journal_section = ""
    if trades:
        # Top 10 Winning
        win_sorted = sorted(trades, key=lambda x: x.get("profit_abs", 0.0), reverse=True)
        win_rows = []
        for i, t in enumerate(win_sorted[:10], start=1):
            pair = t.get("pair", "N/A")
            pos = "🔴 Short" if t.get("is_short") else "🟢 Long"
            tag = t.get("enter_tag") or "N/A"
            dur_min = t.get("trade_duration", 0)
            dur_str = f"{dur_min // 60}h {dur_min % 60}m" if dur_min >= 60 else f"{dur_min}m"
            p_pct = (t.get("profit_ratio", 0.0) or 0.0) * 100
            p_abs = t.get("profit_abs", 0.0) or 0.0
            exit_r = t.get("exit_reason") or "N/A"
            open_d = str(t.get("open_date", ""))[:16]
            close_d = str(t.get("close_date", ""))[:16]
            win_rows.append(
                f"| #{i} | **{pair}** | {pos} | `{tag}` | {open_d} ➔ {close_d} | {dur_str} | **{p_pct:+.2f}%** | **{p_abs:+,.2f} USDT** | `{exit_r}` |"
            )

        # Top 10 Drawdown / Loss
        loss_candidates = [t for t in trades if t.get("profit_ratio", 0.0) < 0]
        loss_sorted = sorted(loss_candidates, key=lambda x: x.get("profit_abs", 0.0))
        loss_rows = []
        for i, t in enumerate(loss_sorted[:10], start=1):
            pair = t.get("pair", "N/A")
            pos = "🔴 Short" if t.get("is_short") else "🟢 Long"
            tag = t.get("enter_tag") or "N/A"
            dur_min = t.get("trade_duration", 0)
            dur_str = f"{dur_min // 60}h {dur_min % 60}m" if dur_min >= 60 else f"{dur_min}m"
            p_pct = (t.get("profit_ratio", 0.0) or 0.0) * 100
            p_abs = t.get("profit_abs", 0.0) or 0.0
            exit_r = t.get("exit_reason") or "N/A"
            open_d = str(t.get("open_date", ""))[:16]
            close_d = str(t.get("close_date", ""))[:16]
            loss_rows.append(
                f"| #{i} | **{pair}** | {pos} | `{tag}` | {open_d} ➔ {close_d} | {dur_str} | **{p_pct:+.2f}%** | **{p_abs:+,.2f} USDT** | `{exit_r}` |"
            )

        # Recent 15 trades
        recent_sorted = sorted(trades, key=lambda x: str(x.get("close_date", "")), reverse=True)
        recent_rows = []
        for i, t in enumerate(recent_sorted[:15], start=1):
            pair = t.get("pair", "N/A")
            pos = "🔴 Short" if t.get("is_short") else "🟢 Long"
            tag = t.get("enter_tag") or "N/A"
            dur_min = t.get("trade_duration", 0)
            dur_str = f"{dur_min // 60}h {dur_min % 60}m" if dur_min >= 60 else f"{dur_min}m"
            p_pct = (t.get("profit_ratio", 0.0) or 0.0) * 100
            p_abs = t.get("profit_abs", 0.0) or 0.0
            exit_r = t.get("exit_reason") or "N/A"
            close_d = str(t.get("close_date", ""))[:16]
            recent_rows.append(
                f"| #{i} | **{pair}** | {pos} | `{tag}` | {close_d} | {dur_str} | **{p_pct:+.2f}%** | **{p_abs:+,.2f} USDT** | `{exit_r}` |"
            )

        loss_table_content = "\n".join(loss_rows) if loss_rows else "| - | *Không có lệnh thua lỗ trong đợt đánh giá này* | - | - | - | - | - | - | - |"

        trade_journal_section = f"""## 📑 Chi Tiết Các Lệnh Giao Dịch (Trade Execution Journal)

### 🥇 Top 10 Lệnh Lãi Cao Nhất (Top Winning Trades)
| # | Cặp giao dịch | Vị thế | Enter Tag | Thời gian Mở ➔ Đóng | Thời lượng | Lợi nhuận % | Lợi nhuận USDT | Lý do thoát |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
""" + "\n".join(win_rows) + f"""

### ⚠️ Top Lệnh Thua Lỗ / Sụt Giảm Lớn Nhất (Top Drawdown Trades)
| # | Cặp giao dịch | Vị thế | Enter Tag | Thời gian Mở ➔ Đóng | Thời lượng | Thua lỗ % | Thua lỗ USDT | Lý do thoát |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
""" + loss_table_content + f"""

### ⏱️ Nhật Ký 15 Lệnh Giao Dịch Gần Nhất (Recent Trades Log)
| # | Cặp giao dịch | Vị thế | Enter Tag | Thời gian Đóng | Thời lượng | Lợi nhuận % | Lợi nhuận USDT | Lý do thoát |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
""" + "\n".join(recent_rows) + "\n"

    md = f"""# 📈 Báo Cáo Đánh Giá Hiệu Suất Backtest Toàn Diện (Comprehensive Quantitative Report)

- **Chiến lược (Strategy)**: `{strat_name}`
- **Thời gian đánh giá (Evaluation Date)**: `{date_display}`
- **Cửa sổ Backtest (Timerange)**: `{timerange}`
- **Tổng thời lượng (Duration)**: `{backtest_days} ngày`
- **Mã nguồn dữ liệu (Source File)**: `{source_filename}`

---

{comparison_section}
---

## 🎯 Chỉ Số Hiệu Suất Cốt Lõi (Executive Performance Metrics)

| Chỉ số định lượng | Giá trị thực tế | Đánh giá Benchmark | Tiêu chuẩn chất lượng |
| :--- | :--- | :--- | :--- |
| **Tỷ lệ thắng (Winrate)** | **{winrate:.2f}%** | {'🟢 Robust' if winrate >= 80 else '🟡 Moderate' if winrate >= 65 else '🔴 Low'} | Ngưỡng an toàn >= 70% |
| **Hệ số Sharpe (Sharpe Ratio)** | **{sharpe:.2f}** | {'🟢 Exceptional' if sharpe >= 3.0 else '🟡 Good' if sharpe >= 1.5 else '🔴 Low'} | Chuẩn Alpha quỹ >= 2.0 |
| **Hệ số Sortino (Sortino Ratio)** | **{sortino:.2f}** | {'🟢 Excellent' if sortino >= 4.0 else '🟡 Moderate'} | Đo lường rủi ro sụt giảm âm |
| **Sụt giảm tài khoản tối đa (Max Drawdown %)** | **{max_dd:.2f}%** | {'🟢 Defended' if max_dd <= 10 else '🟡 Watch' if max_dd <= 20 else '🔴 Severe'} | Giới hạn rủi ro < 15% |
| **Sụt giảm tuyệt đối (Max Drawdown Abs)** | **{max_dd_abs:+,.2f} USDT** | 🟢 Đã kiểm soát | Độ sâu drawdown danh mục |
| **Hệ số lãi/lỗ (Profit Factor)** | **{profit_factor:.2f}** | {'🟢 High' if profit_factor >= 2.0 else '🟡 Acceptable' if profit_factor >= 1.2 else '🔴 Unfavorable'} | Chuẩn định lượng >= 1.5 |
| **Chuỗi thua dài nhất (Longest Loss Streak)** | **{longest_loss_streak} trades** | {'🟢 Safe' if longest_loss_streak <= 3 else '🟡 Elevated' if longest_loss_streak <= 6 else '🔴 Critical'} | Kiểm soát chuỗi sụt giảm |

---

## 📊 Chỉ Số Định Lượng Mở Rộng (Secondary Quantitative Indicators)

| Chỉ số định lượng | Kết quả | Mô tả & Ý nghĩa kỹ thuật |
| :--- | :--- | :--- |
| **Tổng số lệnh (Total Trades)** | `{total_trades}` | Tổng số lệnh đã hoàn tất trong timerange |
| **Tổng lệnh thắng / hòa / thua** | `{wins_count}` thắng / `{draws_count}` hòa / `{losses_count}` thua | Phân bổ kết quả các giao dịch |
| **Lợi nhuận ròng % (Net Profit %)** | `{profit_total:+.2f}%` | Tỷ lệ tăng trưởng toàn bộ tài khoản |
| **Lợi nhuận tuyệt đối (Net Profit Abs)** | `{profit_total_abs:+,.2f} USDT` | Lợi nhuận bằng tiền mặt (USDT) |
| **Lợi nhuận trung bình / lệnh** | `{avg_profit_per_trade:+,.2f} USDT` | Hiệu quả trung bình mỗi lần vào lệnh |
| **Mật độ giao dịch (Trades Per Day)** | `{trades_per_day:.2f} lệnh / ngày` | Tần suất giao dịch bình quân |
| **Kỳ vọng toán học (Expectancy)** | `{expectancy:.4f}` | Lợi nhuận kỳ vọng trên mỗi 1 đơn vị rủi ro |
| **Hệ số Calmar (Calmar Ratio)** | `{calmar:.2f}` | Tỷ lệ lợi nhuận trên sụt giảm vốn tối đa |
| **Tốc độ tăng trưởng kép (CAGR)** | `{cagr:.2f}%` | Compound Annual Growth Rate quy năm |

---

{pos_table}
{exit_table}
## 🔍 Bảng Phân Tích Đầy Đủ Tất Cả Các Entry Tags (Full Enter Tag Breakdown)

> *Bảng tổng hợp chi tiết 100% tất cả các tag tín hiệu vào lệnh (Entry Tags) đã hoạt động trong phiên backtest.*

| Enter Tag | Vị thế | Số lệnh | Tỷ lệ thắng (Winrate) | Thắng/Hòa/Thua | Tổng LN % | Tổng LN (USDT) | LN TB/Lệnh | Thời lượng TB | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
{tag_table}

---

{trade_journal_section}
---
*Báo cáo được khởi tạo tự động bởi `scripts/export_report.py` phục vụ chu trình Tối ưu hóa Tự động Agentic AI.*
"""
    return md


def main():
    parser = argparse.ArgumentParser(description="Export exhaustive Freqtrade backtest report to JSON & Markdown")
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

    now_utc = datetime.now(timezone.utc)
    timestamp_str = now_utc.strftime("%Y%m%d_%H%M%S")
    date_str = now_utc.strftime("%Y%m%d")
    date_display = now_utc.strftime("%Y-%m-%d %H:%M:%S UTC")

    # Destination paths
    history_dir = Path("reports/history")
    history_dir.mkdir(parents=True, exist_ok=True)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)

    # Find previous run before saving new one
    prev_run = find_previous_run(history_dir, current_source_file=result_file.name)
    if prev_run:
        logger.info(f"Found previous historical run for benchmark comparison: date={prev_run.get('date')} source={prev_run.get('source_file')}")
    else:
        logger.info("No prior benchmark run found in reports/history/. This run will establish the baseline.")

    # 1. Save normalized historical JSON
    compact_history = {
        "strategy": strat_name,
        "date": date_str,
        "timestamp": timestamp_str,
        "source_file": result_file.name,
        "timerange": strat_metrics.get("timerange"),
        "backtest_days": strat_metrics.get("backtest_days"),
        "metrics": {
            "winrate": strat_metrics.get("winrate"),
            "sharpe": strat_metrics.get("sharpe"),
            "sortino": strat_metrics.get("sortino"),
            "max_drawdown_account": strat_metrics.get("max_drawdown_account"),
            "max_drawdown_abs": strat_metrics.get("max_drawdown_abs"),
            "profit_factor": strat_metrics.get("profit_factor"),
            "max_consecutive_losses": strat_metrics.get("max_consecutive_losses"),
            "total_trades": strat_metrics.get("total_trades"),
            "profit_total": strat_metrics.get("profit_total"),
            "profit_total_abs": strat_metrics.get("profit_total_abs"),
            "expectancy": strat_metrics.get("expectancy"),
            "calmar": strat_metrics.get("calmar"),
            "cagr": strat_metrics.get("cagr"),
        },
        "results_per_enter_tag": strat_metrics.get("results_per_enter_tag", {}),
        "exit_reason_summary": strat_metrics.get("exit_reason_summary", {}),
    }

    # Save timestamped history so multiple runs aren't lost
    ts_json = history_dir / f"backtest_{timestamp_str}.json"
    daily_json = history_dir / f"backtest_{date_str}.json"
    target_json = args.output_json or ts_json

    with open(target_json, "w", encoding="utf-8") as f:
        json.dump(compact_history, f, indent=2)
    # Also update daily canonical backtest_<date>.json
    with open(daily_json, "w", encoding="utf-8") as f:
        json.dump(compact_history, f, indent=2)
    logger.info(f"Saved historical report to: {target_json} & {daily_json}")

    # 2. Save Comprehensive Markdown Report
    md_content = generate_markdown(
        strat_name=strat_name,
        s=strat_metrics,
        date_display=date_display,
        source_filename=result_file.name,
        prev_run=prev_run,
    )

    with open(args.output_md, "w", encoding="utf-8") as f:
        f.write(md_content)
    logger.info(f"Saved comprehensive latest markdown report: {args.output_md}")


if __name__ == "__main__":
    main()
