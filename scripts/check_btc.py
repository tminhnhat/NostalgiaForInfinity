import pandas as pd
import glob
import os

data_dir = 'user_data/data/binance/futures'
fpath = os.path.join(data_dir, "BTC_USDT_USDT-5m-futures.feather")
if os.path.exists(fpath):
    df = pd.read_feather(fpath)
    df['date'] = pd.to_datetime(df['date'])
    sub = df[(df['date'] >= "2026-07-01 12:00:00") & (df['date'] <= "2026-07-01 14:00:00")]
    print("=== BTC 5m on 2026-07-01 ===")
    for _, r in sub.iterrows():
        print(f"{r['date']} | O={r['open']:.1f} H={r['high']:.1f} L={r['low']:.1f} C={r['close']:.1f} V={r['volume']:.1f}")
