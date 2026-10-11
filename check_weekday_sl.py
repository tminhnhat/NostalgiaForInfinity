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

weekday_sl = df[(~df['is_sunday']) & (df['exit_reason'] == 'stop_loss')]
print(f"Total weekday stoplosses: {len(weekday_sl)}")
for _, r in weekday_sl.iterrows():
    print(f"{r['pair']:<14} | Open: {r['open_date']} ({r['open_dt'].day_name()}) | Dur: {r['trade_duration']/60:4.1f}h | Tag: {r['enter_tag']} | PnL: {r['profit_abs']:.2f}$")
