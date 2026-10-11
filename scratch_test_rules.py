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

def evaluate_candle(trade):
    pair = trade['pair']
    sym = pair.replace('/', '_').replace(':', '_')
    fpath = f"user_data/data/binance/futures/{sym}-5m-futures.feather"
    fpath_1h = f"user_data/data/binance/futures/{sym}-1h-futures.feather"
    if not os.path.exists(fpath) or not os.path.exists(fpath_1h):
        return None
        
    df = pd.read_feather(fpath)
    df['date'] = pd.to_datetime(df['date'])
    t_open = pd.to_datetime(trade['open_date'])
    sub = df[df['date'] < t_open]
    if len(sub) < 50: return None
    idx = sub.index[-1]
    
    close = df['close'].to_numpy()
    high = df['high'].to_numpy()
    low = df['low'].to_numpy()
    open_px = df['open'].to_numpy()
    vol = df['volume'].to_numpy()
    
    ema_9 = ta.EMA(close, timeperiod=9)
    ema_21 = ta.EMA(close, timeperiod=21)
    ema_50 = ta.EMA(close, timeperiod=50)
    ema_200 = ta.EMA(close, timeperiod=200)
    vol_sma20 = ta.SMA(vol, timeperiod=20)
    rsi_14 = ta.RSI(close, timeperiod=14)
    
    # 1h RSI
    df_1h = pd.read_feather(fpath_1h)
    df_1h['date'] = pd.to_datetime(df_1h['date'])
    sub_1h = df_1h[df_1h['date'] <= t_open]
    rsi_1h = ta.RSI(sub_1h['close'].to_numpy(), timeperiod=14)[-1] if len(sub_1h) >= 15 else 50.0
    
    # Slopes
    e9_slope_down = ema_9[idx] < ema_9[idx - 1]
    e21_slope_down = ema_21[idx] < ema_21[idx - 1]
    
    # Spread
    spread = (ema_21[idx] - ema_9[idx]) / ema_21[idx]
    
    # Volume
    vol_ratio = vol[idx] / max(vol_sma20[idx], 1e-9)
    
    return {
        'e9_slope_down': e9_slope_down,
        'e21_slope_down': e21_slope_down,
        'spread_ge_06': spread >= 0.0006,
        'spread_ge_08': spread >= 0.0008,
        'rsi_1h_ge_30': rsi_1h >= 30.0,
        'rsi_1h_ge_32': rsi_1h >= 32.0,
        'vol_ge_125': vol_ratio >= 1.25,
    }

print("=== EVALUATING STOP LOSS TRADES (9 trades) ===")
sl_evals = [evaluate_candle(t) for t in loss_sl_703 if evaluate_candle(t)]
print(f"Total SL evaluated: {len(sl_evals)}")
print("Passed e9_slope_down:", sum(1 for e in sl_evals if e['e9_slope_down']))
print("Passed e21_slope_down:", sum(1 for e in sl_evals if e['e21_slope_down']))
print("Passed spread >= 0.06%:", sum(1 for e in sl_evals if e['spread_ge_06']))
print("Passed spread >= 0.08%:", sum(1 for e in sl_evals if e['spread_ge_08']))
print("Passed rsi_1h >= 30.0:", sum(1 for e in sl_evals if e['rsi_1h_ge_30']))
print("Passed rsi_1h >= 32.0:", sum(1 for e in sl_evals if e['rsi_1h_ge_32']))

# Combined filter A: e9_slope_down & spread >= 0.06% & rsi_1h >= 30.0
filtered_sl_A = sum(1 for e in sl_evals if e['e9_slope_down'] and e['spread_ge_06'] and e['rsi_1h_ge_30'])
print(f"\nSL passing Filter A (e9_slope & spread>=0.06% & rsi1h>=30): {filtered_sl_A} / {len(sl_evals)} (ELIMINATED {len(sl_evals) - filtered_sl_A} STOPLOSSES!)")

print("\n=== EVALUATING WINNING TRADES (37 trades) ===")
win_evals = [evaluate_candle(t) for t in win_703 if evaluate_candle(t)]
print(f"Total Wins evaluated: {len(win_evals)}")
win_passed_A = sum(1 for e in win_evals if e['e9_slope_down'] and e['spread_ge_06'] and e['rsi_1h_ge_30'])
print(f"Wins passing Filter A: {win_passed_A} / {len(win_evals)} (KEPT {win_passed_A}/{len(win_evals)} WINS!)")
