import pandas as pd
import talib.abstract as ta
import numpy as np

df = pd.read_feather("user_data/data/binance/futures/DOGE_USDT_USDT-5m-futures.feather")
df['date'] = pd.to_datetime(df['date'], utc=True)

for t_str in ['2026-09-20 07:45:00+00:00', '2026-09-20 07:50:00+00:00', '2026-09-20 07:55:00+00:00']:
    row = df[df['date'] == pd.to_datetime(t_str)]
    idx = row.index[0]
    sub = df.iloc[max(0, idx-100):idx+1].copy()

    close = sub['close'].to_numpy()
    rsi14 = ta.RSI(close, timeperiod=14)
    stoch_rsi_low = ta.MIN(rsi14, timeperiod=14)
    stoch_rsi_high = ta.MAX(rsi14, timeperiod=14)
    stoch_range = np.where(stoch_rsi_high - stoch_rsi_low == 0, 1e-9, stoch_rsi_high - stoch_rsi_low)
    raw_stoch_k = ((rsi14 - stoch_rsi_low) / stoch_range) * 100.0
    k_custom = ta.SMA(raw_stoch_k, timeperiod=3)[-1]
    
    print(f"Candle {t_str}: close={close[-1]}, rsi={rsi14[-1]:.2f}, k_custom={k_custom:.2f}")
