import zipfile
import json
import pandas as pd
import glob
import talib.abstract as ta

zp = 'user_data/backtest_results/backtest-result-2026-10-11_12-11-43.zip'
with zipfile.ZipFile(zp) as z:
    for n in z.namelist():
        if n.endswith('.json') and not n.endswith('.meta.json'):
            d = json.loads(z.read(n).decode('utf-8'))
            if 'strategy' in d:
                trades = d['strategy']['NostalgiaForInfinityX8_Combined']['trades']
                break

wins = [t for t in trades if t.get('profit_abs', 0) > 0 and t.get('is_short', False)]
print(f"Total winning short trades: {len(wins)}")

k_vals = []
for w in wins:
    pair = w['pair']
    open_date = w['open_date']
    base = pair.split('/')[0]
    f_files = glob.glob(f"user_data/data/binance/futures/{base}_USDT_USDT-5m-futures.feather")
    if not f_files:
        continue
    df = pd.read_feather(f_files[0])
    df['date'] = pd.to_datetime(df['date'], utc=True)
    row = df[df['date'] == pd.to_datetime(open_date)]
    if len(row) == 0:
        continue
    idx = row.index[0]
    sub_df = df.iloc[max(0, idx-100):idx+1].copy()
    fastk, fastd = ta.STOCHRSI(sub_df['close'].to_numpy(), timeperiod=14, fastk_period=3, fastd_period=3)
    k = fastk[-1]
    k_vals.append(k)

k_ge_20 = [k for k in k_vals if k >= 20.0]
k_lt_20 = [k for k in k_vals if k < 20.0]
print(f"Wins analyzed: {len(k_vals)}")
print(f"Wins with StochRSI >= 20: {len(k_ge_20)} ({len(k_ge_20)/len(k_vals)*100:.1f}%)")
print(f"Wins with StochRSI < 20: {len(k_lt_20)} ({len(k_lt_20)/len(k_vals)*100:.1f}%)")
