import pandas as pd
import numpy as np
import talib.abstract as ta

data_path = "user_data/data/binance/futures"
df_arb = pd.read_feather(f"{data_path}/ARB_USDT_USDT-5m-futures.feather")
df_tia = pd.read_feather(f"{data_path}/TIA_USDT_USDT-5m-futures.feather")

for sym, df in [("ARB", df_arb), ("TIA", df_tia)]:
    c = df['close'].to_numpy()
    h = df['high'].to_numpy()
    l = df['low'].to_numpy()
    o = df['open'].to_numpy()
    v = df['volume'].to_numpy()
    
    ema_21 = ta.EMA(c, timeperiod=21)
    ema_50 = ta.EMA(c, timeperiod=50)
    ema_200 = ta.EMA(c, timeperiod=200)
    rsi_14 = ta.RSI(c, timeperiod=14)
    stoch_k, _ = ta.STOCHRSI(c, timeperiod=14, fastk_period=14, fastd_period=3)
    
    vol_sma_20 = ta.SMA(v, timeperiod=20)
    vol_spike_ratio = v / np.where(vol_sma_20 == 0, 1e-9, vol_sma_20)
    
    # Check 731
    cond_731 = (
        (v > 0)
        & (ema_50 < ema_200)
        & (c < ema_21)
        & (c < o)
        & (vol_spike_ratio >= 1.25)
        & (rsi_14 > 28.0) & (rsi_14 < 48.0)
        & (stoch_k >= 20.0)
    )
    
    df['date_str'] = df['date'].astype(str)
    row = df[df['date_str'].str.contains("2026-08-31 04:45")]
    idx = row.index[0]
    print(f"{sym} 731 triggered at 04:45?: {cond_731[idx]}")
