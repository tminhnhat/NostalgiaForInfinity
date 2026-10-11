import os
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
            all_702 = [t for t in trades if t.get('enter_tag') == '702 703 731']
            losses = [t for t in all_702 if t.get('profit_abs', 0) <= 0]
            wins = [t for t in all_702 if t.get('profit_abs', 0) > 0]
            break

print(f"Total 702 703 731 trades: {len(all_702)} (Wins: {len(wins)}, Losses: {len(losses)})")

filtered_losses = 0
for t in losses:
    pair = t['pair']
    symbol = pair.replace('/', '_').replace(':', '_')
    feather_file = f"user_data/data/binance/futures/{symbol}-5m-futures.feather"
    if not os.path.exists(feather_file):
        continue
    df = pd.read_feather(feather_file)
    close = df['close'].to_numpy()
    rsi_14 = ta.RSI(close, timeperiod=14)
    stoch_low = ta.MIN(rsi_14, timeperiod=14)
    stoch_high = ta.MAX(rsi_14, timeperiod=14)
    stoch_range = np.where(stoch_high - stoch_low == 0, 1e-9, stoch_high - stoch_low)
    raw_stoch_k = ((rsi_14 - stoch_low) / stoch_range) * 100.0
    stoch_k = ta.SMA(raw_stoch_k, timeperiod=3)
    
    open_dt = pd.to_datetime(t['open_date'])
    match = df[df['date'] == open_dt]
    if not match.empty:
        idx = match.index[0]
        k_val = stoch_k[idx]
        if k_val < 25.0:
            filtered_losses += 1

print(f"So lenh thua bi LOAI BO neu bat buoc StochRSI >= 25: {filtered_losses} / {len(losses)} lenh thua!")
print(f"Tuc la loai bo duoc {filtered_losses/len(losses)*100:.1f}% tong so lenh thua!")
