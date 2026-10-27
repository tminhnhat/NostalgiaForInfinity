import pandas as pd
import numpy as np
import talib.abstract as ta

df_1h = pd.read_feather('user_data/data/binance/futures/NEAR_USDT_USDT-1h-futures.feather')
df_1h['date'] = pd.to_datetime(df_1h['date'])
df_1h['EMA_50_1h'] = ta.EMA(df_1h['close'], timeperiod=50)

sub = df_1h[(df_1h['date'] >= '2026-10-19 18:00:00+00:00') & (df_1h['date'] <= '2026-10-20 03:00:00+00:00')]
for _, r in sub.iterrows():
    print(r['date'], 'Close:', r['close'], 'EMA_50_1h:', r['EMA_50_1h'])
