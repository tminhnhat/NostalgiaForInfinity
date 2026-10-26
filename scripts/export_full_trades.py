#!/usr/bin/env python3
"""Export all trades from backtest result to full markdown and CSV journal."""

from datetime import datetime
import json
from pathlib import Path
import shutil
import zipfile

def main():
    backtest_dir = Path("user_data/backtest_results")
    zip_files = sorted(list(backtest_dir.glob("backtest-result-*.zip")), key=lambda p: p.stat().st_mtime, reverse=True)
    if not zip_files:
        print("No backtest results found!")
        return
    result_zip = zip_files[0]
    print(f"Reading latest backtest zip: {result_zip.name}")
    
    with zipfile.ZipFile(result_zip) as z:
        for name in z.namelist():
            if name.endswith(".json") and not name.endswith(".meta.json") and not name.endswith("_config.json"):
                data = json.loads(z.read(name).decode("utf-8"))
                strat_key = list(data.get("strategy", data).keys())[0]
                strat_data = data.get("strategy", data)[strat_key]
                trades = strat_data.get("trades", [])
                break

    trades.sort(key=lambda x: x.get("open_date", ""))

    total_trades = len(trades)
    wins = len([t for t in trades if (t.get("profit_abs", 0.0) or 0.0) > 0])
    losses = len([t for t in trades if (t.get("profit_abs", 0.0) or 0.0) < 0])
    winrate = (wins / total_trades * 100) if total_trades > 0 else 0.0
    start_balance = strat_data.get("dry_run_wallet", 200.0)
    net_profit_abs = strat_data.get("profit_total_abs", 0.0)
    net_profit_pct = strat_data.get("profit_total", 0.0) * 100
    final_balance = start_balance + net_profit_abs

    md_lines = [
        f"# 📑 Bảng Kê Chi Tiết Toàn Bộ {total_trades} Lệnh Giao Dịch Backtest (Vốn 200 USD - Sizing Tỷ Lệ)",
        "",
        "- **Chiến lược**: `NostalgiaForInfinityX8_Combined_AI`",
        f"- **Số vốn ban đầu**: `{start_balance:.2f} USDT` | **Số dư kết thúc**: `{final_balance:.2f} USDT`",
        f"- **Tổng số lệnh**: `{total_trades}` ({wins} Thắng / {losses} Thua) | **Tỷ lệ thắng (Winrate)**: `{winrate:.2f}%`",
        "- **Đòn bẩy áp dụng**: `5x Isolated Margin`",
        f"- **Tổng lợi nhuận ròng**: `+{net_profit_abs:.2f} USDT (+{net_profit_pct:.2f}%)`",
        "",
        "| # | Cặp tiền | Vị thế | Enter Tag | Ký quỹ (USDT) | Giá trị vị thế (5x) | Thời gian Mở | Thời gian Đóng | Thời lượng | Lợi nhuận % | Lợi nhuận (USDT) | Lý do đóng lệnh |",
        "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |",
    ]

    csv_lines = [
        "trade_num,pair,position,enter_tag,stake_usdt,position_value_5x_usdt,open_date,close_date,duration_min,profit_pct,profit_usdt,exit_reason"
    ]

    for i, t in enumerate(trades, 1):
        pair = t.get("pair", "").replace("/USDT:USDT", "").replace(":USDT", "")
        pos = "🔴 Short" if t.get("is_short") else "🟢 Long"
        tag = t.get("enter_tag") or "none"
        stake = t.get("stake_amount", 0.0)
        pos_val = stake * (t.get("leverage") or 5.0)
        open_d = t.get("open_date", "")[:16].replace("T", " ")
        close_d = t.get("close_date", "")[:16].replace("T", " ")
        dur_min = t.get("trade_duration", 0)
        dur_str = f"{dur_min//60}h {dur_min%60}m" if dur_min >= 60 else f"{dur_min}m"
        prof_pct = (t.get("profit_ratio", 0.0) or 0.0) * 100
        prof_abs = t.get("profit_abs", 0.0) or 0.0
        exit_r = t.get("exit_reason", "")
        exit_clean = exit_r.split("(")[0].strip()

        prof_pct_str = f"+{prof_pct:.2f}%" if prof_pct >= 0 else f"{prof_pct:.2f}%"
        prof_abs_str = f"+{prof_abs:.2f} USDT" if prof_abs >= 0 else f"{prof_abs:.2f} USDT"

        row = f"| {i} | **{pair}** | {pos} | `{tag}` | {stake:.2f} | {pos_val:.2f} | {open_d} | {close_d} | {dur_str} | **{prof_pct_str}** | **{prof_abs_str}** | `{exit_clean}` |"
        md_lines.append(row)

        csv_row = f'{i},{pair},{pos},{tag},{stake:.2f},{pos_val:.2f},{open_d},{close_d},{dur_min},{prof_pct:.2f},{prof_abs:.2f},"{exit_clean}"'
        csv_lines.append(csv_row)

    md_content = "\n".join(md_lines)
    csv_content = "\n".join(csv_lines)

    out_md = Path("reports/full_trade_journal_200usd.md")
    out_csv = Path("reports/latest_trades.csv")
    out_md.write_text(md_content, encoding="utf-8")
    out_csv.write_text(csv_content, encoding="utf-8")

    # Copy to brain artifact directory
    artifact_dir = Path(r"C:\Users\Nhat\.gemini\antigravity-ide\brain\2be52438-dbc4-400d-88e7-cdf3e22d20a8")
    if artifact_dir.exists():
        shutil.copy(out_md, artifact_dir / "full_trade_journal_200usd.md")

    print(f"Exported {len(trades)} trades successfully!")
    print(f"MD file: {out_md} ({out_md.stat().st_size} bytes)")
    print(f"CSV file: {out_csv} ({out_csv.stat().st_size} bytes)")

if __name__ == "__main__":
    main()
