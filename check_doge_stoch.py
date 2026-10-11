import pandas as pd
import talib.abstract as ta
import numpy as np

df = pd.read_feather("user_data/data/binance/futures/DOGE_USDT_USDT-5m-futures.feather")
df['date'] = pd.to_datetime(df['date'], utc=True)
row = df[df['date'] == pd.to_datetime('2026-09-20 07:55:00+00:00')]
idx = row.index[0]
sub = df.iloc[max(0, idx-100):idx+1].copy()

close = sub['close'].to_numpy()
rsi14 = ta.RSI(close, timeperiod=14)
stoch_rsi_low = ta.MIN(rsi14, timeperiod=14)
stoch_rsi_high = ta.MAX(rsi14, timeperiod=14)
stoch_range = np.where(stoch_rsi_high - stoch_rsi_low == 0, 1e-9, stoch_rsi_high - stoch_rsi_low)
raw_stoch_k = ((rsi14 - stoch_rsi_low) / stoch_range) * 100.0
k_custom = ta.SMA(raw_stoch_k, timeperiod=3)[-1]

fastk, fastd = ta.STOCHRSI(close, timeperiod=14, fastk_period=3, fastd_period=3)

print("At 2026-09-20 07:55 for DOGE:")
print(f"k_custom (in ShortSignals): {k_custom}")
print(f"ta.STOCHRSI fastk: {fastk[-1]}")
