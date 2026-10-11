import pandas as pd
import numpy as np
import talib.abstract as ta

data_path = "user_data/data/binance/futures"
df_apt = pd.read_feather(f"{data_path}/APT_USDT_USDT-5m-futures.feather")
df_apt_1h = pd.read_feather(f"{data_path}/APT_USDT_USDT-1h-futures.feather")

df_apt['date_str'] = df_apt['date'].astype(str)
row = df_apt[df_apt['date_str'].str.contains("2026-08-31 01:30|2026-08-31 01:35")]

c = df_apt['close'].to_numpy()
df_apt['rsi_14'] = ta.RSI(c, timeperiod=14)
df_apt['ema_9'] = ta.EMA(c, timeperiod=9)
df_apt['ema_21'] = ta.EMA(c, timeperiod=21)
df_apt['ema_50'] = ta.EMA(c, timeperiod=50)

df_apt_1h['rsi_14_1h'] = ta.RSI(df_apt_1h['close'].to_numpy(), timeperiod=14)
df_apt_1h['date_str'] = df_apt_1h['date'].astype(str)
row_1h = df_apt_1h[df_apt_1h['date_str'].str.contains("2026-08-31 01:00")]

print("APT 5m around 01:35:")
print(df_apt[df_apt['date_str'].str.contains("2026-08-31 01:30|2026-08-31 01:35")][['date', 'open', 'high', 'low', 'close', 'volume', 'rsi_14', 'ema_9', 'ema_21']])
print("\nAPT 1h around 01:00:")
print(row_1h[['date', 'open', 'high', 'low', 'close', 'rsi_14_1h']])
