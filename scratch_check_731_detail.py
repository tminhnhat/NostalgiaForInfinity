import pandas as pd
import numpy as np
import talib.abstract as ta

data_path = "user_data/data/binance/futures"
for sym in ["ARB", "TIA"]:
    df = pd.read_feather(f"{data_path}/{sym}_USDT_USDT-5m-futures.feather")
    
    c = df['close'].to_numpy()
    h = df['high'].to_numpy()
    l = df['low'].to_numpy()
    o = df['open'].to_numpy()
    v = df['volume'].to_numpy()
    
    ema_21 = ta.EMA(c, timeperiod=21)
    ema_50 = ta.EMA(c, timeperiod=50)
    ema_200 = ta.EMA(c, timeperiod=200)
    rsi_14 = ta.RSI(c, timeperiod=14)
    stoch_k, stoch_d = ta.STOCHRSI(c, timeperiod=14, fastk_period=14, fastd_period=3)
    
    vol_sma_20 = ta.SMA(v, timeperiod=20)
    vol_spike_ratio = v / np.where(vol_sma_20 == 0, 1e-9, vol_sma_20)
    
    is_sunday = df['date'].dt.dayofweek.to_numpy() == 6
    
    c_731 = (
        (v > 0)
        & (ema_50 < ema_200)
        & (c < ema_21)
        & (c < o)
        & (vol_spike_ratio >= 1.25)
        & (rsi_14 > 28.0) & (rsi_14 < 48.0)
        & (stoch_k >= 20.0)
        & (~is_sunday)
    )
    
    df['c_731'] = c_731
    df['date_str'] = df['date'].astype(str)
    row = df[df['date_str'].str.contains("2026-08-31 04:45")]
    idx = row.index[0]
    print(f"\n=== {sym} at 04:45 ===")
    print(f"close: {c[idx]} | ema_21: {ema_21[idx]:.5f} | close < ema_21: {c[idx] < ema_21[idx]}")
    print(f"vol_spike_ratio: {vol_spike_ratio[idx]:.2f} (>= 1.25: {vol_spike_ratio[idx] >= 1.25})")
    print(f"rsi_14: {rsi_14[idx]:.2f} (in 28..48: {28.0 < rsi_14[idx] < 48.0})")
    print(f"stoch_k: {stoch_k[idx]:.2f} (>= 20: {stoch_k[idx] >= 20.0})")
    print(f"c_731 True?: {c_731[idx]}")
