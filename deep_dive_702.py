import zipfile
import json
import pandas as pd
import glob
import talib.abstract as ta
import numpy as np

zp = 'user_data/backtest_results/backtest-result-2026-10-11_12-11-43.zip'
with zipfile.ZipFile(zp) as z:
    for n in z.namelist():
        if n.endswith('.json') and not n.endswith('.meta.json'):
            d = json.loads(z.read(n).decode('utf-8'))
            if 'strategy' in d:
                trades = d['strategy']['NostalgiaForInfinityX8_Combined']['trades']
                break

short_trades = [t for t in trades if t.get('is_short', False) and '702' in t.get('enter_tag', '')]
print(f"Total Short trades with tag 702: {len(short_trades)}")

data = []
for t in short_trades:
    pair = t['pair']
    open_date = t['open_date']
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
    sub_df = df.iloc[max(0, idx-300):idx+1].copy()
    close = sub_df['close'].to_numpy()
    high = sub_df['high'].to_numpy()
    low = sub_df['low'].to_numpy()
    vol = sub_df['volume'].to_numpy()
    
    ema20 = ta.EMA(close, timeperiod=20)[-1]
    ema50 = ta.EMA(close, timeperiod=50)[-1]
    ema200 = ta.EMA(close, timeperiod=200)[-1]
    rsi14 = ta.RSI(close, timeperiod=14)[-1]
    k, d_val = ta.STOCHRSI(close, timeperiod=14, fastk_period=3, fastd_period=3)
    
    # 1h trend if available or approx
    # distance to EMA 200
    dist_ema200 = (close[-1] - ema200) / ema200 * 100
    
    is_win = t.get('profit_abs', 0) > 0
    profit = t.get('profit_abs', 0)
    dur = t.get('trade_duration', 0) / 60
    exit_r = t.get('exit_reason', '')
    
    data.append({
        'pair': pair,
        'open_date': open_date,
        'win': is_win,
        'profit': profit,
        'dur_h': dur,
        'exit': exit_r,
        'dist_ema200': dist_ema200,
        'rsi14': rsi14,
        'stoch_k': k[-1],
        'close': close[-1],
        'ema200': ema200
    })

df_res = pd.DataFrame(data)
print("\n--- SUMMARY OF WINS vs LOSSES for TAG 702 ---")
print(df_res.groupby('win')[['profit', 'dur_h', 'dist_ema200', 'rsi14', 'stoch_k']].mean())
print("\n--- ALL LOSSES ---")
print(df_res[~df_res['win']][['pair', 'open_date', 'profit', 'dur_h', 'dist_ema200', 'rsi14', 'stoch_k', 'exit']])
