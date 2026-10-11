import zipfile
import json
import pandas as pd

zp = 'user_data/backtest_results/backtest-result-2026-10-11_17-30-07.zip'
with zipfile.ZipFile(zp) as z:
    for n in z.namelist():
        if n.endswith('.json') and not n.endswith('.meta.json'):
            d = json.loads(z.read(n).decode('utf-8'))
            strat = list(d['strategy'].keys())[0]
            trades = d['strategy'][strat]['trades']
            break

df = pd.DataFrame(trades)
df['open_dt'] = pd.to_datetime(df['open_date'])
df['day_name'] = df['open_dt'].dt.day_name()
df['is_win'] = df['profit_abs'] > 0

print("=== TẤT CẢ CÁC LỆNH THEO THỨ TRONG TUẦN ===")
print(df.groupby('day_name').agg(
    total=('profit_abs', 'count'),
    wins=('is_win', 'sum'),
    losses=('is_win', lambda x: (~x).sum()),
    winrate=('is_win', lambda x: x.mean()*100),
    pnl=('profit_abs', 'sum')
).to_string())

print("\n=== NẾU LOẠI BỎ CÁC LỆNH MỞ VÀO CHỦ NHẬT (SUNDAY) ===")
df_no_sun = df[df['day_name'] != 'Sunday']
print(f"Tổng lệnh: {len(df_no_sun)} | Thắng: {df_no_sun['is_win'].sum()} | Thua: {(~df_no_sun['is_win']).sum()} | Winrate: {df_no_sun['is_win'].mean()*100:.2f}% | PnL: {df_no_sun['profit_abs'].sum():.2f}$")
