import pandas as pd
import numpy as np
import talib.abstract as ta

df = pd.read_feather('user_data/data/binance/futures/MSTR_USDT_USDT-5m-futures.feather')
df['date'] = pd.to_datetime(df['date'])
macd, macdsignal, macdhist = ta.MACD(df['close'].to_numpy(), fastperiod=12, slowperiod=26, signalperiod=9)
df['macdhist'] = macdhist
df['ema21'] = ta.EMA(df['close'].to_numpy(), timeperiod=21)

sub = df[(df['date'] >= '2026-07-01 12:40:00+00:00') & (df['date'] <= '2026-07-01 13:35:00+00:00')]
for _, r in sub.iterrows():
    print(f"{r['date']} | C={r['close']:.2f} | EMA21={r['ema21']:.2f} | MACDHist={r['macdhist']:.4f}")
