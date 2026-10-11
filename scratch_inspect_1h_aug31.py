import pandas as pd
import numpy as np
import talib.abstract as ta

data_path = "user_data/data/binance/futures"
df_btc_1h = pd.read_feather(f"{data_path}/BTC_USDT_USDT-1h-futures.feather")
df_arb_1h = pd.read_feather(f"{data_path}/ARB_USDT_USDT-1h-futures.feather")
df_tia_1h = pd.read_feather(f"{data_path}/TIA_USDT_USDT-1h-futures.feather")

for name, df in [("BTC", df_btc_1h), ("ARB", df_arb_1h), ("TIA", df_tia_1h)]:
    df['rsi_14'] = ta.RSI(df, timeperiod=14)
    df['ema_9'] = ta.EMA(df, timeperiod=9)
    df['ema_21'] = ta.EMA(df, timeperiod=21)
    df['ema_50'] = ta.EMA(df, timeperiod=50)
    df['ema_200'] = ta.EMA(df, timeperiod=200)
    df['date_str'] = df['date'].astype(str)
    
    row = df[df['date_str'].str.contains("2026-08-31 04:00")]
    print(f"\n=== {name} 1h at 2026-08-31 04:00 ===")
    r = row.iloc[0]
    print(f"Close: {r['close']} | EMA9: {r['ema_9']:.5f} | EMA21: {r['ema_21']:.5f} | EMA50: {r['ema_50']:.5f} | EMA200: {r['ema_200']:.5f}")
    print(f"RSI 14: {r['rsi_14']:.2f}")
    print(f"Close > EMA9: {r['close'] > r['ema_9']} | Close > EMA21: {r['close'] > r['ema_21']}")
    print(f"EMA9 > EMA21: {r['ema_9'] > r['ema_21']}")
