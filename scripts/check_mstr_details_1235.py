import pandas as pd
import numpy as np
import talib.abstract as ta

df = pd.read_feather('user_data/data/binance/futures/MSTR_USDT_USDT-5m-futures.feather')
df['date'] = pd.to_datetime(df['date'])
close = df['close'].to_numpy()
low = df['low'].to_numpy()
high = df['high'].to_numpy()
volume = df['volume'].to_numpy()

bbu, bbm, bbl = ta.BBANDS(close, timeperiod=20, nbdevup=2.0, nbdevdn=2.0)
rsi = ta.RSI(close, timeperiod=14)
ema21 = ta.EMA(close, timeperiod=21)
ema50 = ta.EMA(close, timeperiod=50)
ema200 = ta.EMA(close, timeperiod=200)

idx = df[df['date'] == '2026-07-01 12:35:00+00:00'].index[0]
r = df.iloc[idx]

print(f"MSTR at 12:35:")
print(f"Close: {r['close']}, Open: {r['open']}, Low: {r['low']}, High: {r['high']}")
print(f"BBL: {bbl[idx]:.4f}, BBM: {bbm[idx]:.4f}, BBU: {bbu[idx]:.4f}")
print(f"Dist to BBL: {(r['close'] - bbl[idx]) / r['close'] * 100:.2f}%")
print(f"RSI: {rsi[idx]:.2f}")
print(f"EMA21: {ema21[idx]:.2f}, EMA50: {ema50[idx]:.2f}, EMA200: {ema200[idx]:.2f}")
