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
df['is_sunday'] = df['open_dt'].dt.dayofweek == 6

sunday_trades = df[df['is_sunday']]
print("ALL TRADES ENTERED ON SUNDAY:")
for _, r in sunday_trades.iterrows():
    print(f"Short={r['is_short']} | {r['pair']:<14} | Open: {r['open_date']} | Tag: {r['enter_tag']} | Exit: {r['exit_reason']} | PnL: {r['profit_abs']:.2f}$ ({r['profit_ratio']*100:.2f}%)")
