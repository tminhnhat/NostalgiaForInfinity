import os
import glob
import pandas as pd
import numpy as np
import talib.abstract as ta
import json
import zipfile
import sys

sys.stdout.reconfigure(encoding='utf-8')

latest_zip = 'user_data/backtest_results/backtest-result-2026-10-11_12-11-43.zip'

with zipfile.ZipFile(latest_zip, 'r') as z:
    for name in z.namelist():
        if name.endswith('.json') and not name.endswith('.meta.json'):
            data = json.loads(z.read(name).decode('utf-8'))
            strat = list(data['strategy'].keys())[0]
            trades = data['strategy'][strat]['trades']
            losses = [t for t in trades if t.get('enter_tag') == '702 703 731' and t.get('profit_abs', 0) <= 0]
            break

print("Checking indicators from feather files for the 11 losses...")

for i, t in enumerate(losses, 1):
    pair = t['pair']
    # pair format: NEAR/USDT:USDT -> NEAR_USDT_USDT-5m-futures.feather
    symbol = pair.replace('/', '_').replace(':', '_')
    feather_file = f"user_data/data/binance/futures/{symbol}-5m-futures.feather"
    
    if not os.path.exists(feather_file):
        print(f"File not found: {feather_file}")
        continue
        
    df = pd.read_feather(feather_file)
    
    # Calculate indicators
    close = df['close'].to_numpy()
    high = df['high'].to_numpy()
    low = df['low'].to_numpy()
    
    df['rsi_14'] = ta.RSI(close, timeperiod=14)
    stoch_low = ta.MIN(df['rsi_14'], timeperiod=14)
    stoch_high = ta.MAX(df['rsi_14'], timeperiod=14)
    stoch_range = np.where(stoch_high - stoch_low == 0, 1e-9, stoch_high - stoch_low)
    raw_stoch_k = ((df['rsi_14'] - stoch_low) / stoch_range) * 100.0
    df['stoch_k'] = ta.SMA(raw_stoch_k, timeperiod=3)
    df['ema_50'] = ta.EMA(close, timeperiod=50)
    df['ema_200'] = ta.EMA(close, timeperiod=200)
    
    # Match open date with timezone
    open_dt = pd.to_datetime(t['open_date'])
    match = df[df['date'] == open_dt]
    
    if not match.empty:
        row = match.iloc[0]
        idx = match.index[0]
        prev_row = df.iloc[idx - 1]
        
        # Distance from EMA 200 (trend distance)
        dist_ema200 = (row['close'] - row['ema_200']) / row['ema_200'] * 100
        dist_ema50 = (row['close'] - row['ema_50']) / row['ema_50'] * 100
        
        print(f"Lệnh #{i:2d} | {pair:14} | Vào: {open_dt} | Close: {row['close']:.4f}")
        print(f"   RSI_14: {row['rsi_14']:.1f} | StochRSI_K: {row['stoch_k']:.1f} (Trước đó: {prev_row['stoch_k']:.1f})")
        print(f"   Cách EMA50: {dist_ema50:.2f}% | Cách EMA200: {dist_ema200:.2f}%")
        print(f"   Lý do thoát: {t['exit_reason']} | PnL: {t['profit_abs']:.2f}$\n")
