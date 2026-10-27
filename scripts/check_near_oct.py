import pandas as pd
import numpy as np

# Load feather of NEAR
df = pd.read_feather('user_data/data/binance/futures/NEAR_USDT_USDT-5m-futures.feather')
df['date'] = pd.to_datetime(df['date'])
sub = df[(df['date'] >= '2026-10-19 19:50:00') & (df['date'] <= '2026-10-20 02:00:00')]
print("NEAR actual open_date in October 2026:")
for _, r in sub.iterrows():
    print(r['date'], r['open'], r['close'])
