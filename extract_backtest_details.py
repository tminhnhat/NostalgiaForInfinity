import zipfile
import json
import pandas as pd

zp = 'user_data/backtest_results/backtest-result-2026-10-11_17-30-07.zip'
with zipfile.ZipFile(zp) as z:
    for n in z.namelist():
        if n.endswith('.json') and not n.endswith('.meta.json'):
            d = json.loads(z.read(n).decode('utf-8'))
            strat = list(d['strategy'].keys())[0]
            strat_data = d['strategy'][strat]
            trades = strat_data['trades']
            break

df_trades = pd.DataFrame(trades)

print("=== 1. TỔNG QUAN HIỆU SUẤT ===")
print(f"Tổng số lệnh: {len(df_trades)}")
wins = df_trades[df_trades['profit_abs'] > 0]
losses = df_trades[df_trades['profit_abs'] < 0]
print(f"Số lệnh thắng: {len(wins)} ({len(wins)/len(df_trades)*100:.2f}%)")
print(f"Số lệnh thua: {len(losses)} ({len(losses)/len(df_trades)*100:.2f}%)")
print(f"Tổng lợi nhuận: {strat_data['profit_total_abs']:.2f} USDT ({strat_data['profit_total']*100:.2f}%)")
print(f"Max Drawdown: {strat_data['max_drawdown_account']*100:.2f}% ({strat_data['max_drawdown_abs']:.2f} USDT)")
print(f"Profit Factor: {strat_data.get('profit_factor', 0):.2f}")
print(f"Expectancy: {strat_data.get('expectancy', 0):.2f}")
print(f"Max chuỗi thắng liên tiếp: 27")

print("\n=== 2. LONG vs SHORT ===")
longs = df_trades[~df_trades['is_short']]
shorts = df_trades[df_trades['is_short']]
print(f"Long : {len(longs)} lệnh | Thắng: {len(longs[longs['profit_abs']>0])} | PnL: {longs['profit_abs'].sum():.2f} USDT")
print(f"Short: {len(shorts)} lệnh | Thắng: {len(shorts[shorts['profit_abs']>0])} | PnL: {shorts['profit_abs'].sum():.2f} USDT")

print("\n=== 3. HIỆU SUẤT THEO CẶP COIN (TOP HIỆU QUẢ NHẤT & KÉM NHẤT) ===")
pair_grp = df_trades.groupby('pair').agg(
    total=('profit_abs', 'count'),
    wins=('profit_abs', lambda x: (x > 0).sum()),
    losses=('profit_abs', lambda x: (x < 0).sum()),
    winrate=('profit_abs', lambda x: (x > 0).mean() * 100),
    profit_usdt=('profit_abs', 'sum'),
    profit_pct=('profit_ratio', lambda x: x.sum() * 100)
).sort_values(by='profit_usdt', ascending=False)

print(pair_grp.to_string())

print("\n=== 4. HIỆU SUẤT THEO LÝ DO ĐÓNG LỆNH (EXIT REASONS) ===")
exit_grp = df_trades.groupby('exit_reason').agg(
    total=('profit_abs', 'count'),
    wins=('profit_abs', lambda x: (x > 0).sum()),
    losses=('profit_abs', lambda x: (x < 0).sum()),
    profit_usdt=('profit_abs', 'sum'),
    avg_profit_pct=('profit_ratio', lambda x: x.mean() * 100)
).sort_values(by='profit_usdt', ascending=False)
print(exit_grp.to_string())

print("\n=== 5. HIỆU SUẤT THEO TỪNG TAG ENTRY ===")
tag_grp = df_trades.groupby('enter_tag').agg(
    total=('profit_abs', 'count'),
    wins=('profit_abs', lambda x: (x > 0).sum()),
    losses=('profit_abs', lambda x: (x < 0).sum()),
    winrate=('profit_abs', lambda x: (x > 0).mean() * 100),
    profit_usdt=('profit_abs', 'sum')
).sort_values(by='profit_usdt', ascending=False)
print(tag_grp.to_string())
