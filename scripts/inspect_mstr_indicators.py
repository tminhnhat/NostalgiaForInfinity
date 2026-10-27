import pandas as pd
import numpy as np

def main():
    df = pd.read_feather('user_data/data/binance/futures/MSTR_USDT_USDT-5m-futures.feather')
    # Let's inspect the candles of MSTR around that date
    sub = df[(df['date'] >= '2026-07-01 12:00') & (df['date'] <= '2026-07-01 13:00')].copy()
    
    # Calculate basic indicators
    df['ema_9'] = df['close'].ewm(span=9).mean()
    df['ema_21'] = df['close'].ewm(span=21).mean()
    df['ema_50'] = df['close'].ewm(span=50).mean()
    df['ema_200'] = df['close'].ewm(span=200).mean()
    df['vol_ma20'] = df['volume'].rolling(20).mean()
    df['vol_spike'] = df['volume'] / df['vol_ma20']
    
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / loss
    df['rsi'] = 100 - (100 / (1 + rs))

    idx = df[df['date'] == '2026-07-01 12:40:00+00:00'].index[0]
    row = df.loc[idx]
    print(f"Date: {row['date']}")
    print(f"Close: {row['close']}")
    print(f"EMA 9: {row['ema_9']:.3f}, EMA 21: {row['ema_21']:.3f}, EMA 50: {row['ema_50']:.3f}, EMA 200: {row['ema_200']:.3f}")
    print(f"RSI: {row['rsi']:.2f}")
    print(f"Volume: {row['volume']}, Vol Spike: {row['vol_spike']:.2f}")
    
    # Check previous 3 volumes
    v0 = df.loc[idx, 'volume']
    v1 = df.loc[idx-1, 'volume']
    v2 = df.loc[idx-2, 'volume']
    print(f"Volumes: 12:30={v2:.0f}, 12:35={v1:.0f}, 12:40={v0:.0f}")
    print(f"Volume declining: {v0 < v1 < v2}")

if __name__ == '__main__':
    main()
