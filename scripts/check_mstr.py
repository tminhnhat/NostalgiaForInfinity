import pandas as pd
import numpy as np

def main():
    # Load analyzed dataframe if available or compute cond_702 on MSTR
    df = pd.read_feather('user_data/data/binance/futures/MSTR_USDT_USDT-5m-futures.feather')
    df = df[(df['date'] >= '2026-06-30') & (df['date'] <= '2026-07-02')].copy()
    print("MSTR rows count:", len(df))
    
    # Let's inspect the candles around 12:40 on 2026-07-01
    target = df[(df['date'] >= '2026-07-01 12:00') & (df['date'] <= '2026-07-01 13:00')]
    for idx, row in target.iterrows():
        print(f"{row['date']} | Open: {row['open']} | High: {row['high']} | Low: {row['low']} | Close: {row['close']} | Vol: {row['volume']}")

if __name__ == '__main__':
    main()
