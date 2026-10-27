import csv
from collections import defaultdict

def main():
    trades = []
    with open('reports/latest_trades.csv', mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            trades.append(row)

    def get_category(tag, pos):
        t = tag.strip()
        if 'Short' in pos:
            if '562' in t:
                return 'Nhóm Bán Khống Cấu Trúc (Short Structural Scalp - Tag 562)'
            elif '_AI_PASS' in t:
                return 'Nhóm Bán Khống AI Gatekeeper (Short AI Validated - Tag 7xx)'
            else:
                return 'Nhóm Bán Khống Khác (Short Other)'
        else:
            tags = t.split()
            if any(x in ('61', '62', '63', '64', '65') for x in tags):
                return 'Nhóm Mua Bắt Đáy Tích Lũy (Long Dip-Rebuy - Tags 6x)'
            elif any(x in ('141', '142', '143', '144', '145') for x in tags):
                return 'Nhóm Mua Xu Hướng Kỹ Thuật (Long Trend Continuation - Tags 14x)'
            elif any(x in ('1', '2', '3', '4', '5', '6') for x in tags):
                return 'Nhóm Mua Sóng Chính Cơ Bản (Long Normal Trend - Tags 1-6)'
            elif any(x in ('41', '42', '43', '44', '46', '47') for x in tags):
                return 'Nhóm Mua Động Lượng Nhanh (Long Quick Momentum - Tags 4x)'
            elif any(x in ('161', '162', '163') for x in tags):
                return 'Nhóm Mua Lướt Sóng Ngắn (Long Scalp - Tags 16x)'
            elif any(x in ('101', '102') for x in tags):
                return 'Nhóm Mua Phản Ứng Nhanh (Long Rapid - Tags 10x)'
            else:
                return 'Nhóm Lệnh Ngoại Lệ / Cắt Bỏ (Long Abandoned / Underperforming)'

    cat_map = defaultdict(lambda: {'trades': 0, 'wins': 0, 'losses': 0, 'profit_usdt': 0.0, 'tags': defaultdict(lambda: {'trades': 0, 'wins': 0, 'losses': 0, 'profit_usdt': 0.0, 'profit_pct': 0.0})})

    for t in trades:
        pos = t['position']
        tag = t['enter_tag'].strip()
        cat = get_category(tag, pos)
        p_usdt = float(t['profit_usdt'])
        p_pct = float(t['profit_pct'])

        cat_map[cat]['trades'] += 1
        cat_map[cat]['profit_usdt'] += p_usdt
        if p_usdt > 0:
            cat_map[cat]['wins'] += 1
        elif p_usdt < 0:
            cat_map[cat]['losses'] += 1

        t_stat = cat_map[cat]['tags'][tag]
        t_stat['trades'] += 1
        t_stat['profit_usdt'] += p_usdt
        t_stat['profit_pct'] += p_pct
        if p_usdt > 0:
            t_stat['wins'] += 1
        elif p_usdt < 0:
            t_stat['losses'] += 1

    out_lines = ["# Báo Cáo Phân Loại Hiệu Suất Theo Tag (Tag Performance Breakdown)\n"]
    for cat, d in sorted(cat_map.items(), key=lambda x: x[1]['profit_usdt'], reverse=True):
        wr = d['wins'] / d['trades'] * 100
        out_lines.append(f"\n### {cat}")
        out_lines.append(f"- **Tổng số lệnh**: `{d['trades']}` | **Thắng/Thua**: `{d['wins']}/{d['losses']}` | **Tỷ lệ thắng (Winrate)**: **`{wr:.1f}%`** | **Tổng lợi nhuận**: **`+{d['profit_usdt']:.2f} USDT`**\n")
        out_lines.append("| Enter Tag | Số lệnh | Thắng/Thua | Tỷ lệ thắng (Winrate) | Lợi nhuận (USDT) | Lợi nhuận TB (%) | Đánh giá |")
        out_lines.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
        for tag, t_data in sorted(d['tags'].items(), key=lambda x: x[1]['profit_usdt'], reverse=True):
            t_wr = t_data['wins'] / t_data['trades'] * 100
            avg_pct = t_data['profit_pct'] / t_data['trades']
            rating = "🟢 Siêu hiệu quả" if t_wr == 100 and t_data['profit_usdt'] > 20 else ("🟢 Tốt" if t_wr >= 75 and t_data['profit_usdt'] > 0 else ("🟡 Ổn định" if t_data['profit_usdt'] >= 0 else "🔴 Thua lỗ / Cần rà soát"))
            sign = "+" if t_data['profit_usdt'] >= 0 else ""
            out_lines.append(f"| `{tag}` | {t_data['trades']} | {t_data['wins']}/{t_data['losses']} | **{t_wr:.1f}%** | **{sign}{t_data['profit_usdt']:.2f} USDT** | {avg_pct:+.2f}% | {rating} |")

    with open("reports/tag_analysis_report.md", "w", encoding="utf-8") as f:
        f.write("\n".join(out_lines))
    print("Exported successfully to reports/tag_analysis_report.md")

if __name__ == '__main__':
    main()
