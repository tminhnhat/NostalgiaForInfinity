import pandas as pd
import numpy as np

df = pd.read_feather('user_data/data/binance/futures/MSTR_USDT_USDT-1h-futures.feather')
df['date'] = pd.to_datetime(df['date'])
df['ema50'] = df['close'].ewm(span=50).mean()
df['ema200'] = df['close'].ewm(span=200).mean()

sub = df[(df['date'] >= '2026-07-01 08:00:00') & (df['date'] <= '2026-07-01 16:00:00')]
for _, r in sub.iterrows():
    print(f"{r['date']} | C={r['close']:.2f} | EMA50_1h={r['ema50']:.2f} | EMA200_1h={r['ema200']:.2f}")
