import pandas as pd
import numpy as np
import talib.abstract as ta

data_path = "user_data/data/binance/futures"
for sym in ["ARB", "TIA"]:
    df = pd.read_feather(f"{data_path}/{sym}_USDT_USDT-5m-futures.feather")
    df['ema_9'] = ta.EMA(df, timeperiod=9)
    df['ema_21'] = ta.EMA(df, timeperiod=21)
    df['ema_50'] = ta.EMA(df, timeperiod=50)
    df['ema_200'] = ta.EMA(df, timeperiod=200)
    df['rsi_14'] = ta.RSI(df, timeperiod=14)
    
    df['date_str'] = df['date'].astype(str)
    row = df[df['date_str'].str.contains("2026-08-31 04:45")]
    idx = row.index[0]
    sub = df.loc[idx-8:idx+2, ['date', 'open', 'high', 'low', 'close', 'volume', 'ema_9', 'ema_21', 'ema_50', 'rsi_14']]
    print(f"\n=== {sym} around 2026-08-31 04:45 ===")
    print(sub)
