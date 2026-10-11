import os
import glob
import pandas as pd
import numpy as np
import talib.abstract as ta

data_path = "user_data/data/binance/futures"
pair_files = glob.glob(f"{data_path}/*_USDT_USDT-5m-futures.feather")

trades_found = []

for f in pair_files:
    pair_name = os.path.basename(f).replace("-5m-futures.feather", "").replace("_", "/")
    if "ETH" in pair_name:
        continue
    df = pd.read_feather(f)
    df = df[(df['date'] >= '2026-08-11') & (df['date'] <= '2026-10-10')].copy()
    if df.empty:
        continue
        
    c = df['close'].to_numpy()
    h = df['high'].to_numpy()
    l = df['low'].to_numpy()
    o = df['open'].to_numpy()
    v = df['volume'].to_numpy()
    
    ema_9 = ta.EMA(c, timeperiod=9)
    ema_21 = ta.EMA(c, timeperiod=21)
    ema_50 = ta.EMA(c, timeperiod=50)
    ema_200 = ta.EMA(c, timeperiod=200)
    rsi_14 = ta.RSI(c, timeperiod=14)
    macd, macdsignal, macdhist = ta.MACD(c, fastperiod=12, slowperiod=26, signalperiod=9)
    
    vol_sma_20 = ta.SMA(v, timeperiod=20)
    vol_spike_ratio = v / np.where(vol_sma_20 == 0, 1e-9, vol_sma_20)
    
    hl_range = h - l
    upper_wick_ratio = (h - np.maximum(c, o)) / np.where(hl_range == 0, 1e-9, hl_range)
    
    prev_candle_green = np.roll(c, 1) > np.roll(o, 1)
    shift_ema_21 = np.roll(ema_21, 1)
    shift_macdhist = np.roll(macdhist, 1)
    
    cond_721_opt = (
        (v > 0)
        & (ema_50 < ema_200)
        & (ema_21 < shift_ema_21)
        & prev_candle_green
        & (h >= ema_21 * 0.9995)
        & (c < ema_21)
        & (c < o)
        & (upper_wick_ratio >= 0.40)
        & (vol_spike_ratio >= 1.25)
        & (rsi_14 >= 42.0) & (rsi_14 <= 58.0)
    )
    
    cond_702 = (
        (v > 0)
        & (ema_50 < ema_200)
        & (macd < 0) & (macdhist < 0)
        & (macdhist < shift_macdhist)
        & (c < ema_21) & (c < ema_50)
        & (c < o)
        & (vol_spike_ratio >= 1.20)
    )
    
    trigger_721_opt = cond_721_opt & cond_702
    indices = np.where(trigger_721_opt)[0]
    for idx in indices:
        trades_found.append({
            'pair': pair_name,
            'date': df.iloc[idx]['date'],
            'close': c[idx],
        })

df_res = pd.DataFrame(trades_found)
print(f"Total trigger_721_opt signals: {len(df_res)}")
if not df_res.empty:
    print(df_res.head(20))
