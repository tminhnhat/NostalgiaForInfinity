import pandas as pd
import numpy as np

def main():
    df_mstr = pd.read_feather('user_data/data/binance/futures/MSTR_USDT_USDT-15m-futures.feather')
    df_btc = pd.read_feather('user_data/data/binance/futures/BTC_USDT_USDT-5m-futures.feather')
    
    # Calculate 1h EMA50 on MSTR and 4h EMA200 on BTC
    df_mstr['ema_50_1h'] = df_mstr['close'].ewm(span=50*4).mean()
    mstr_sub = df_mstr[(df_mstr['date'] >= '2026-07-01 12:00') & (df_mstr['date'] <= '2026-07-01 13:00')]
    print("MSTR at 12:40:")
    for idx, r in mstr_sub.iterrows():
        dist_50 = (r['close'] - r['ema_50_1h']) / r['ema_50_1h']
        print(f"{r['date']} | Close: {r['close']} | EMA50_1h: {r['ema_50_1h']:.2f} | Dist: {dist_50*100:.2f}%")

if __name__ == '__main__':
    main()
