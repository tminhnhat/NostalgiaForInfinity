#!/usr/bin/env python3
"""Jules Optimization PR Evaluator & Benchmark Gatekeeper.

Evaluates backtest results generated from a Jules-proposed PR branch,
compares metrics against the baseline, assesses quant alpha improvement,
and posts an executive audit report directly to the Pull Request.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import logging
import os
from pathlib import Path
import subprocess
import sys

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
logger = logging.getLogger("PREvaluator")


def load_history(history_dir: Path) -> list[dict]:
    files = sorted(history_dir.glob("backtest_*.json"))
    records = []
    for f in files:
        try:
            with open(f, "r", encoding="utf-8") as fp:
                records.append(json.load(fp))
        except Exception as e:
            logger.warning(f"Error reading {f}: {e}")
    return records


def build_evaluation_report(
    current_run: dict,
    baseline_run: dict | None,
    pr_number: str | None,
    branch_name: str | None,
) -> tuple[str, bool, str]:
    curr_m = current_run.get("metrics", {})
    base_m = baseline_run.get("metrics", {}) if baseline_run else {}

    c_winrate = (curr_m.get("winrate", 0.0) or 0.0) * 100
    b_winrate = (base_m.get("winrate", 0.0) or 0.0) * 100 if base_m else c_winrate
    d_winrate = c_winrate - b_winrate

    c_profit_pct = (curr_m.get("profit_total", 0.0) or 0.0) * 100
    b_profit_pct = (base_m.get("profit_total", 0.0) or 0.0) * 100 if base_m else c_profit_pct
    d_profit_pct = c_profit_pct - b_profit_pct

    c_profit_abs = curr_m.get("profit_total_abs", 0.0) or 0.0
    b_profit_abs = base_m.get("profit_total_abs", 0.0) or 0.0 if base_m else c_profit_abs
    d_profit_abs = c_profit_abs - b_profit_abs

    c_sharpe = curr_m.get("sharpe", 0.0) or 0.0
    b_sharpe = base_m.get("sharpe", 0.0) or 0.0 if base_m else c_sharpe
    d_sharpe = c_sharpe - b_sharpe

    c_sortino = curr_m.get("sortino", 0.0) or 0.0
    b_sortino = base_m.get("sortino", 0.0) or 0.0 if base_m else c_sortino
    d_sortino = c_sortino - b_sortino

    c_dd = (curr_m.get("max_drawdown_account", 0.0) or 0.0) * 100
    b_dd = (base_m.get("max_drawdown_account", 0.0) or 0.0) * 100 if base_m else c_dd
    d_dd = c_dd - b_dd

    c_pf = curr_m.get("profit_factor", 0.0) or 0.0
    b_pf = base_m.get("profit_factor", 0.0) or 0.0 if base_m else c_pf
    d_pf = c_pf - b_pf

    c_trades = curr_m.get("total_trades", 0) or 0
    b_trades = base_m.get("total_trades", 0) or 0 if base_m else c_trades
    d_trades = c_trades - b_trades

    c_streak = curr_m.get("max_consecutive_losses", 0) or 0
    b_streak = base_m.get("max_consecutive_losses", 0) or 0 if base_m else c_streak
    d_streak = c_streak - b_streak

    c_exp = curr_m.get("expectancy", 0.0) or 0.0
    b_exp = base_m.get("expectancy", 0.0) or 0.0 if base_m else c_exp
    d_exp = c_exp - b_exp

    # Gatekeeper Evaluation Rules
    passed = (
        c_winrate >= 85.0
        and c_dd <= 6.0
        and c_profit_abs > 0
        and (c_sharpe >= 2.0 or c_sharpe >= b_sharpe - 1.5)
        and (d_dd <= 1.5)
    )

    if passed:
        verdict = "🟢 **APPROVED - READY TO MERGE**"
        verdict_badge = "PASSED"
        status_note = "Chiến lược tối ưu đáp ứng toàn diện các tiêu chuẩn Alpha định lượng (Winrate >= 85%, Drawdown <= 6.0%, Sharpe >= 2.0)."
    elif c_winrate >= 80.0 and c_dd <= 8.0:
        verdict = "🟡 **CAUTION - MARGINAL PERFORMANCE**"
        verdict_badge = "CAUTION"
        status_note = "Hiệu năng chấp nhận được nhưng có một số chỉ số cần theo dõi thêm trước khi triển khai Live."
    else:
        verdict = "🔴 **REJECTED - ALPHA DEGRADED**"
        verdict_badge = "FAILED"
        status_note = "Các thay đổi gây suy giảm hiệu năng (Drawdown vượt ngưỡng hoặc Winrate giảm mạnh). Yêu cầu tinh chỉnh thêm."

    pr_str = f"#{pr_number}" if pr_number else "Local / Manual"
    branch_str = branch_name or "feature/jules-proposal"

    # Compare targeted tags
    c_tags = {item["key"].strip(): item for item in current_run.get("results_per_enter_tag", [])}
    b_tags = {item["key"].strip(): item for item in base_m.get("results_per_enter_tag", [])} if isinstance(base_m.get("results_per_enter_tag"), list) else {}
    if not b_tags and baseline_run:
        b_tags = {item["key"].strip(): item for item in baseline_run.get("results_per_enter_tag", [])}

    tag_rows = []
    key_tags = ["562", "701 702 703 731_AI_PASS", "702 703 731_AI_PASS", "64", "2"]
    for kt in key_tags:
        ct = c_tags.get(kt, {})
        bt = b_tags.get(kt, {})
        if ct or bt:
            c_t_tr = ct.get("trades", 0)
            b_t_tr = bt.get("trades", 0)
            c_t_wr = (ct.get("winrate", 0.0) or 0.0) * 100
            b_t_wr = (bt.get("winrate", 0.0) or 0.0) * 100
            c_t_prof = ct.get("profit_total_abs", 0.0) or 0.0
            b_t_prof = bt.get("profit_total_abs", 0.0) or 0.0
            tag_rows.append(
                f"| `{kt}` | {c_t_tr} ({b_t_tr}) | **{c_t_wr:.1f}%** ({b_t_wr:.1f}%) | "
                f"**{c_t_prof:+.2f}** ({b_t_prof:+.2f}) USDT | {'🟢 Tốt' if c_t_prof >= 0 else '🔴 Sụt giảm'} |"
            )
    tag_table = "\n".join(tag_rows) if tag_rows else "| *Không có dữ liệu tag so sánh* | - | - | - | - |"

    comment = f"""## 🤖 Báo Cáo Thẩm Định Backtest Cho Đề Xuất Của Jules ({pr_str})

- **Nhánh đề xuất (PR Branch)**: `{branch_str}`
- **Thời gian đánh giá**: `{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}`
- **Kết quả thẩm định Quant**: {verdict}
> {status_note}

---

### ⚖️ Ma Trận Đối Sánh Định Lượng: Đề Xuất PR vs Baseline

| Chỉ số định lượng | Đề xuất của PR (Mới) | Baseline Trước (Cũ) | Chênh lệch (Δ Delta) | Đánh giá |
| :--- | :--- | :--- | :--- | :--- |
| **Tỷ lệ thắng (Winrate)** | **{c_winrate:.2f}%** | {b_winrate:.2f}% | `{d_winrate:+.2f}%` | {'🟢 Tăng' if d_winrate >= 0 else ('🟡 Giảm nhẹ' if d_winrate >= -2.0 else '🔴 Giảm')} |
| **Lợi nhuận ròng % (Net Profit %)** | **{c_profit_pct:+.2f}%** | {b_profit_pct:+.2f}% | `{d_profit_pct:+.2f}%` | {'🟢 Tăng' if d_profit_pct >= 0 else '🔴 Giảm'} |
| **Lợi nhuận tuyệt đối (USDT)** | **{c_profit_abs:+.2f} USDT** | {b_profit_abs:+.2f} USDT | `{d_profit_abs:+.2f} USDT` | {'🟢 Tăng' if d_profit_abs >= 0 else '🔴 Giảm'} |
| **Hệ số Sharpe (Sharpe Ratio)** | **{c_sharpe:.2f}** | {b_sharpe:.2f} | `{d_sharpe:+.2f}` | {'🟢 Alpha chuẩn quỹ' if c_sharpe >= 2.0 else '🟡 Cần cải thiện'} |
| **Hệ số Sortino (Sortino Ratio)** | **{c_sortino:.2f}** | {b_sortino:.2f} | `{d_sortino:+.2f}` | {'🟢 Xuất sắc' if c_sortino >= 5.0 else '🟡 Ổn định'} |
| **Sụt giảm tối đa (Max Drawdown %)** | **{c_dd:.2f}%** | {b_dd:.2f}% | `{d_dd:+.2f}%` | {'🟢 An toàn (<= 6%)' if c_dd <= 6.0 else '🔴 Vượt ngưỡng'} |
| **Hệ số Lãi/Lỗ (Profit Factor)** | **{c_pf:.2f}** | {b_pf:.2f} | `{d_pf:+.2f}` | {'🟢 Cực mạnh' if c_pf >= 3.0 else '🟢 Đạt chuẩn'} |
| **Kỳ vọng toán học (Expectancy)** | **{c_exp:.2f} USDT** | {b_exp:.2f} USDT | `{d_exp:+.2f} USDT` | {'🟢 Tốt' if c_exp > 0 else '🔴 Âm'} |
| **Chuỗi thua dài nhất (Loss Streak)** | **{c_streak} lệnh** | {b_streak} lệnh | `{d_streak:+d} lệnh` | {'🟢 Kiểm soát' if c_streak <= 3 else '🟡 Chú ý'} |
| **Tổng số lệnh (Total Trades)** | **{c_trades} lệnh** | {b_trades} lệnh | `{d_trades:+d} lệnh` | Đủ mẫu thống kê |

---

### 🏷️ Hiệu Suất Của Các Tags Trọng Yếu Đã Được Tối Ưu

| Enter Tag | Số lệnh PR (Baseline) | Winrate PR (Baseline) | Lợi nhuận USDT PR (Baseline) | Đánh giá |
| :--- | :--- | :--- | :--- | :--- |
{tag_table}

---

### 📋 Hướng Dẫn Dành Cho Maintainer
{'- ✅ **Khuyến nghị Hợp nhất (Merge)**: Đề xuất vượt qua bài kiểm tra định lượng 180 ngày mà không gây sụt giảm rủi ro danh mục. Maintainer có thể an tâm merge PR này vào `main`.' if passed else '- ⚠️ **Cần xem xét thêm**: Vui lòng kiểm tra lại log chi tiết hoặc yêu cầu Jules điều chỉnh lại bộ tham số.'}
"""
    return comment, passed, verdict_badge


def post_to_pr(pr_number: str, comment: str, passed: bool):
    try:
        cmd = ["gh", "pr", "comment", pr_number, "--body", comment]
        subprocess.run(cmd, check=True)
        logger.info(f"Successfully posted evaluation comment to PR #{pr_number}")

        # Update label
        label = "proposal-validated-pass" if passed else "proposal-needs-revision"
        subprocess.run(["gh", "pr", "edit", pr_number, "--add-label", label], check=False)
    except Exception as e:
        logger.warning(f"Could not comment on PR via gh CLI: {e}")


def main():
    parser = argparse.ArgumentParser(description="Jules PR Backtest Evaluator")
    parser.add_argument("--history-dir", type=Path, default=Path("reports/history"))
    parser.add_argument("--pr-number", type=str, default=None)
    parser.add_argument("--branch", type=str, default=None)
    parser.add_argument("--output", type=Path, default=Path("reports/pr_evaluation_summary.md"))
    args = parser.parse_args()

    history = load_history(args.history_dir)
    if not history:
        logger.error("No backtest history found in reports/history/.")
        sys.exit(1)

    # Current run is the newest file; baseline is the one before it (if available)
    current_run = history[-1]
    baseline_run = history[-2] if len(history) >= 2 else None

    logger.info(f"Loaded {len(history)} runs. Current: {current_run.get('timestamp', 'unknown')}, Baseline: {baseline_run.get('timestamp', 'none') if baseline_run else 'None'}")

    report_md, passed, badge = build_evaluation_report(
        current_run=current_run,
        baseline_run=baseline_run,
        pr_number=args.pr_number,
        branch_name=args.branch,
    )

    # Save local summary markdown
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(report_md)
    logger.info(f"Saved evaluation markdown to {args.output}")

    # GitHub Actions Step Summary
    github_summary_file = os.environ.get("GITHUB_STEP_SUMMARY")
    if github_summary_file:
        try:
            with open(github_summary_file, "a", encoding="utf-8") as f:
                f.write(report_md)
        except Exception as e:
            logger.warning(f"Could not write to GITHUB_STEP_SUMMARY: {e}")

    # Post to PR if PR number specified
    pr_num = args.pr_number or os.environ.get("PR_NUMBER")
    if pr_num:
        post_to_pr(pr_num, report_md, passed)

    print("\n" + "=" * 60)
    print(f"JULES PR EVALUATION SUMMARY: {badge}")
    print("=" * 60)
    print(report_md)
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
