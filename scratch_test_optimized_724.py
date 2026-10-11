import pandas as pd
import numpy as np
import talib.abstract as ta

trades_724 = [
    {"pair": "OP/USDT:USDT", "open_date": "2026-08-15 15:00:00+00:00", "pnl": 8.42},
    {"pair": "DOT/USDT:USDT", "open_date": "2026-08-28 21:05:00+00:00", "pnl": 17.74},
    {"pair": "ARB/USDT:USDT", "open_date": "2026-08-31 04:50:00+00:00", "pnl": -92.31},
    {"pair": "INJ/USDT:USDT", "open_date": "2026-09-01 12:20:00+00:00", "pnl": 1.28},
    {"pair": "TIA/USDT:USDT", "open_date": "2026-08-31 04:50:00+00:00", "pnl": -91.52},
    {"pair": "BNB/USDT:USDT", "open_date": "2026-09-07 11:30:00+00:00", "pnl": 21.27},
    {"pair": "ARB/USDT:USDT", "open_date": "2026-09-12 03:10:00+00:00", "pnl": 22.62},
]

data_path = "user_data/data/binance/futures"

for t in trades_724:
    sym = t['pair'].split('/')[0]
    df = pd.read_feather(f"{data_path}/{sym}_USDT_USDT-5m-futures.feather")
    df_1h = pd.read_feather(f"{data_path}/{sym}_USDT_USDT-1h-futures.feather")
    
    c = df['close'].to_numpy()
    h = df['high'].to_numpy()
    l = df['low'].to_numpy()
    o = df['open'].to_numpy()
    v = df['volume'].to_numpy()
    
    ema_21 = ta.EMA(c, timeperiod=21)
    ema_50 = ta.EMA(c, timeperiod=50)
    ema_200 = ta.EMA(c, timeperiod=200)
    rsi_14 = ta.RSI(c, timeperiod=14)
    
    vol_sma_20 = ta.SMA(v, timeperiod=20)
    vol_spike_ratio = v / np.where(vol_sma_20 == 0, 1e-9, vol_sma_20)
    
    hl_range = h - l
    upper_wick_ratio = (h - np.maximum(c, o)) / np.where(hl_range == 0, 1e-9, hl_range)
    
    shift_ema_50 = np.roll(ema_50, 1)
    prev_candle_green = np.roll(c, 1) > np.roll(o, 1)
    
    target_dt = pd.to_datetime(t['open_date'])
    sub = df[df['date'] < target_dt]
    idx = sub.index[-1]
    
    # 1h RSI check
    df_1h['rsi_1h'] = ta.RSI(df_1h['close'].to_numpy(), timeperiod=14)
    sub_1h = df_1h[df_1h['date'] <= target_dt]
    last_1h = sub_1h.iloc[-1]
    rsi_1h_oversold = last_1h['rsi_1h'] < 30.0
    rsi_1h_overbought = (last_1h['rsi_1h'] > 62.0) & (c[idx] > ema_200[idx])
    
    is_sunday = df.iloc[idx]['date'].dayofweek == 6
    
    cond_optimized = (
        (v[idx] > 0)
        & (ema_50[idx] < ema_200[idx])
        & (ema_50[idx] < shift_ema_50[idx])
        & (h[idx] >= ema_50[idx] * 0.9995)
        & (c[idx] < ema_50[idx])
        & (c[idx] < ema_21[idx])
        & (c[idx] < o[idx])
        & (upper_wick_ratio[idx] >= 0.38)
        & (vol_spike_ratio[idx] >= 1.25)
        & (rsi_14[idx] >= 44.0) & (rsi_14[idx] <= 58.0)
        & (prev_candle_green[idx] | (h[idx] >= ema_50[idx]))
        & (~rsi_1h_oversold)
        & (~rsi_1h_overbought)
        & (~is_sunday)
    )
    
    print(f"{sym} ({t['open_date']}): PnL={t['pnl']:+.2f} | Triggers New 724?: {cond_optimized}")
