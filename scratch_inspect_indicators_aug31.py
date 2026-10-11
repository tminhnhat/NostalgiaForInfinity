import pandas as pd
import numpy as np
from NostalgiaForInfinityX8_ShortSignals import NostalgiaForInfinityX8_ShortSignals

data_path = "user_data/data/binance/futures"
df_arb = pd.read_feather(f"{data_path}/ARB_USDT_USDT-5m-futures.feather")
df_tia = pd.read_feather(f"{data_path}/TIA_USDT_USDT-5m-futures.feather")
df_btc = pd.read_feather(f"{data_path}/BTC_USDT_USDT-5m-futures.feather")
df_arb_1h = pd.read_feather(f"{data_path}/ARB_USDT_USDT-1h-futures.feather")
df_tia_1h = pd.read_feather(f"{data_path}/TIA_USDT_USDT-1h-futures.feather")
df_btc_1h = pd.read_feather(f"{data_path}/BTC_USDT_USDT-1h-futures.feather")

# Populate indicators
signals = NostalgiaForInfinityX8_ShortSignals()

# Add 1h indicators merge like strategy does
import talib.abstract as ta
for df_1h, prefix in [(df_arb_1h, 'arb'), (df_tia_1h, 'tia')]:
    df_1h['rsi_14_1h'] = ta.RSI(df_1h, timeperiod=14)
    df_1h['ema_21_1h'] = ta.EMA(df_1h, timeperiod=21)
    df_1h['ema_50_1h'] = ta.EMA(df_1h, timeperiod=50)

df_arb = signals.populate_indicators(df_arb, {'pair': 'ARB/USDT:USDT'})
df_tia = signals.populate_indicators(df_tia, {'pair': 'TIA/USDT:USDT'})

# Find rows around 2026-08-31 04:45 to 04:55
for name, df in [("ARB", df_arb), ("TIA", df_tia)]:
    df['date_str'] = df['date'].astype(str)
    sub = df[df['date_str'].str.contains("2026-08-31 04:4[0-9]|2026-08-31 04:5[0-9]")]
    cols_to_show = ['date', 'open', 'high', 'low', 'close', 'volume', 'ema_50', 'ema_200', 'rsi_14', 'upper_wick_ratio', 'vol_spike_ratio']
    # Check if 1h columns exist
    for c in ['rsi_14_1h', 'ema_21_1h', 'ema_50_1h']:
        if c in df.columns:
            cols_to_show.append(c)
    print(f"\n=== {name} Indicators ===")
    print(sub[cols_to_show])
