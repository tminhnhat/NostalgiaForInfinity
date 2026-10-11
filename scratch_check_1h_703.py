import json
import zipfile
import os
import pandas as pd
import numpy as np
import talib.abstract as ta

with open('user_data/backtest_results/.last_result.json') as f:
    last_file = json.load(f)['latest_backtest']

zip_path = os.path.join('user_data/backtest_results', last_file)
with zipfile.ZipFile(zip_path, 'r') as z:
    for name in z.namelist():
        if name.endswith('.json'):
            with z.open(name) as jf:
                data = json.load(jf)
            break

strat = list(data['strategy'].keys())[0]
trades = data['strategy'][strat]['trades']
trades_703 = [t for t in trades if '703' in t.get('enter_tag', '').split()]
loss_sl_703 = [t for t in trades_703 if t.get('exit_reason') == 'stop_loss']
win_703 = [t for t in trades_703 if t['profit_abs'] > 0]

print("=== CHECKING 1H & 4H TREND FOR STOP LOSS TRADES ===")
for t in loss_sl_703:
    pair = t['pair']
    sym = pair.replace('/', '_').replace(':', '_')
    fpath_1h = f"user_data/data/binance/futures/{sym}-1h-futures.feather"
    if not os.path.exists(fpath_1h):
        continue
    df_1h = pd.read_feather(fpath_1h)
    df_1h['date'] = pd.to_datetime(df_1h['date'])
    t_open = pd.to_datetime(t['open_date'])
    sub = df_1h[df_1h['date'] <= t_open]
    if sub.empty:
        continue
    c_1h = sub['close'].to_numpy()
    ema21_1h = ta.EMA(c_1h, timeperiod=21)
    ema50_1h = ta.EMA(c_1h, timeperiod=50)
    rsi_1h = ta.RSI(c_1h, timeperiod=14)
    
    last_c = c_1h[-1]
    last_e21 = ema21_1h[-1]
    last_e50 = ema50_1h[-1]
    last_rsi = rsi_1h[-1]
    
    above_ema21_1h = last_c > last_e21
    above_ema50_1h = last_c > last_e50
    print(f"{pair:<14} | Open: {str(t_open)[:16]} | 1h Close: {last_c:8.2f} | 1h EMA21: {last_e21:8.2f} (Above: {above_ema21_1h}) | 1h EMA50: {last_e50:8.2f} | 1h RSI: {last_rsi:4.1f}")
