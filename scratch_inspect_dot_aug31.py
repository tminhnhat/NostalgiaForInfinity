import pandas as pd
import numpy as np
import talib.abstract as ta

data_path = "user_data/data/binance/futures"
df_dot = pd.read_feather(f"{data_path}/DOT_USDT_USDT-5m-futures.feather")
df_dot_1h = pd.read_feather(f"{data_path}/DOT_USDT_USDT-1h-futures.feather")
df_btc_1h = pd.read_feather(f"{data_path}/BTC_USDT_USDT-1h-futures.feather")

c = df_dot['close'].to_numpy()
h = df_dot['high'].to_numpy()
l = df_dot['low'].to_numpy()
o = df_dot['open'].to_numpy()
v = df_dot['volume'].to_numpy()

df_dot['ema_9'] = ta.EMA(c, timeperiod=9)
df_dot['ema_21'] = ta.EMA(c, timeperiod=21)
df_dot['ema_50'] = ta.EMA(c, timeperiod=50)
df_dot['ema_200'] = ta.EMA(c, timeperiod=200)
df_dot['rsi_14'] = ta.RSI(c, timeperiod=14)

vol_sma_20 = ta.SMA(v, timeperiod=20)
df_dot['vol_spike_ratio'] = v / np.where(vol_sma_20 == 0, 1e-9, vol_sma_20)

hl_range = h - l
df_dot['upper_wick_ratio'] = (h - np.maximum(c, o)) / np.where(hl_range == 0, 1e-9, hl_range)

df_dot['date_str'] = df_dot['date'].astype(str)
sub = df_dot[df_dot['date_str'].str.contains("2026-08-31 13:10|2026-08-31 13:15|2026-08-31 13:20")]

print("=== DOT around 2026-08-31 13:15-13:20 ===")
for idx, r in sub.iterrows():
    print(f"Date: {r['date']} | C: {r['close']} | O: {r['open']} | H: {r['high']} | L: {r['low']}")
    print(f"EMA9: {r['ema_9']:.4f} | EMA21: {r['ema_21']:.4f} | EMA50: {r['ema_50']:.4f} | EMA200: {r['ema_200']:.4f}")
    print(f"RSI: {r['rsi_14']:.2f} | WickRatio: {r['upper_wick_ratio']:.2f} | VolSpike: {r['vol_spike_ratio']:.2f}")

# 1h indicators for DOT
df_dot_1h['rsi_1h'] = ta.RSI(df_dot_1h['close'].to_numpy(), timeperiod=14)
df_dot_1h['date_str'] = df_dot_1h['date'].astype(str)
sub_1h = df_dot_1h[df_dot_1h['date_str'].str.contains("2026-08-31 12:00|2026-08-31 13:00")]
print("\n=== DOT 1h around 13:00 ===")
print(sub_1h[['date', 'open', 'high', 'low', 'close', 'rsi_1h']])

# BTC 1h indicators
df_btc_1h['rsi_1h'] = ta.RSI(df_btc_1h['close'].to_numpy(), timeperiod=14)
df_btc_1h['date_str'] = df_btc_1h['date'].astype(str)
sub_btc = df_btc_1h[df_btc_1h['date_str'].str.contains("2026-08-31 12:00|2026-08-31 13:00")]
print("\n=== BTC 1h around 13:00 ===")
print(sub_btc[['date', 'open', 'high', 'low', 'close', 'rsi_1h']])
