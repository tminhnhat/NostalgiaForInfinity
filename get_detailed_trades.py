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

print("=== DANH SÁCH 7 LỆNH LONG (100% THẮNG) ===")
longs = df[~df['is_short']]
for _, r in longs.iterrows():
    print(f"Long | {r['pair']:<14} | Open: {r['open_date']} | Close: {r['close_date']} | Dur: {r['trade_duration']/60:4.1f}h | Tag: {r['enter_tag']} | Exit: {r['exit_reason']} | PnL: +{r['profit_abs']:.2f}$ (+{r['profit_ratio']*100:.2f}%)")

print("\n=== TOP 10 LỆNH SHORT THẮNG LỚN NHẤT ===")
shorts_win = df[df['is_short'] & (df['profit_abs'] > 0)].sort_values(by='profit_abs', ascending=False).head(10)
for _, r in shorts_win.iterrows():
    print(f"Short | {r['pair']:<14} | Open: {r['open_date']} | Close: {r['close_date']} | Dur: {r['trade_duration']/60:4.1f}h | Tag: {r['enter_tag']} | Exit: {r['exit_reason']} | PnL: +{r['profit_abs']:.2f}$ (+{r['profit_ratio']*100:.2f}%)")

print("\n=== CHI TIẾT TOÀN BỘ 14 LỆNH THUA ===")
losses = df[df['profit_abs'] < 0].sort_values(by='profit_abs', ascending=True)
for _, r in losses.iterrows():
    print(f"Short | {r['pair']:<14} | Open: {r['open_date']} | Close: {r['close_date']} | Dur: {r['trade_duration']/60:4.1f}h | Tag: {r['enter_tag']} | Exit: {r['exit_reason']} | PnL: {r['profit_abs']:.2f}$ ({r['profit_ratio']*100:.2f}%)")
