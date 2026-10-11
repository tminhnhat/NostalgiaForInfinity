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

print(f"Inspecting {len(loss_sl_703)} StopLoss trades vs {len(win_703)} Winning trades of Tag 703...\n")

def get_candle_features(trade):
    pair = trade['pair']
    # pair format: BTC/USDT:USDT -> BTC_USDT_USDT-5m-futures.feather
    sym = pair.replace('/', '_').replace(':', '_')
    fpath = f"user_data/data/binance/futures/{sym}-5m-futures.feather"
    if not os.path.exists(fpath):
        return None
    df = pd.read_feather(fpath)
    df['date'] = pd.to_datetime(df['date'])
    
    # trade open_date is the candle where trade entered. The signal candle was 1 candle BEFORE open_date (5m prior)
    t_open = pd.to_datetime(trade['open_date'])
    sub = df[df['date'] < t_open]
    if sub.empty:
        return None
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
    rsi_14 = ta.RSI(close, timeperiod=14)
    vol_sma20 = ta.SMA(vol, timeperiod=20)
    
    c = close[idx]
    h = high[idx]
    l = low[idx]
    o = open_px[idx]
    v = vol[idx]
    vs = vol_sma20[idx]
    r = rsi_14[idx]
    e9 = ema_9[idx]
    e21 = ema_21[idx]
    e50 = ema_50[idx]
    e200 = ema_200[idx]
    
    # features
    hl = max(h - l, 1e-9)
    lower_wick = (min(c, o) - l) / hl
    upper_wick = (h - max(c, o)) / hl
    body = abs(c - o) / hl
    vol_ratio = v / max(vs, 1e-9)
    dist_ema9 = (c - e9) / e9 * 100
    dist_ema21 = (c - e21) / e21 * 100
    ribbon_spread = (e21 - e9) / e21 * 100
    
    return {
        'pair': pair,
        'open_date': str(trade['open_date']),
        'profit': trade['profit_abs'],
        'rsi': r,
        'vol_ratio': vol_ratio,
        'lower_wick': lower_wick,
        'upper_wick': upper_wick,
        'body': body,
        'dist_ema9': dist_ema9,
        'dist_ema21': dist_ema21,
        'ribbon_spread': ribbon_spread,
    }

print("=== STOP LOSS TRADES FEATURES ===")
sl_feats = []
for t in loss_sl_703:
    f = get_candle_features(t)
    if f:
        sl_feats.append(f)
        print(f"{f['pair']:<14} | RSI: {f['rsi']:4.1f} | Vol: {f['vol_ratio']:4.2f}x | Body: {f['body']:4.2f} | LowWick: {f['lower_wick']:4.2f} | UpWick: {f['upper_wick']:4.2f} | Spread: {f['ribbon_spread']:4.2f}% | DistEMA9: {f['dist_ema9']:5.2f}%")

print("\n=== SAMPLE WINNING TRADES FEATURES ===")
win_feats = []
for t in win_703[:15]:
    f = get_candle_features(t)
    if f:
        win_feats.append(f)
        print(f"{f['pair']:<14} | RSI: {f['rsi']:4.1f} | Vol: {f['vol_ratio']:4.2f}x | Body: {f['body']:4.2f} | LowWick: {f['lower_wick']:4.2f} | UpWick: {f['upper_wick']:4.2f} | Spread: {f['ribbon_spread']:4.2f}% | DistEMA9: {f['dist_ema9']:5.2f}%")

df_sl = pd.DataFrame(sl_feats)
df_win = pd.DataFrame([get_candle_features(t) for t in win_703 if get_candle_features(t)])

print("\n=== COMPARISON MEANS ===")
for col in ['rsi', 'vol_ratio', 'body', 'lower_wick', 'upper_wick', 'ribbon_spread', 'dist_ema9']:
    print(f"{col:<15} | StopLoss Mean: {df_sl[col].mean():6.2f} | Win Mean: {df_win[col].mean():6.2f}")
