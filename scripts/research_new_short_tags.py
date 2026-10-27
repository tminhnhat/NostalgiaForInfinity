import os
import glob
import pandas as pd
import numpy as np
import talib.abstract as ta

data_dir = 'user_data/data/binance/futures'
files = glob.glob(os.path.join(data_dir, '*-5m-futures.feather'))
print(f"Scanning {len(files)} pairs...")

results = {'741': [], '742': [], '743': []}

for fpath in files:
    pair_name = os.path.basename(fpath).replace('-5m-futures.feather', '')
    df = pd.read_feather(fpath)
    if len(df) < 500:
        continue
    
    close = df['close'].to_numpy(dtype=float)
    high = df['high'].to_numpy(dtype=float)
    low = df['low'].to_numpy(dtype=float)
    open_px = df['open'].to_numpy(dtype=float)
    volume = df['volume'].to_numpy(dtype=float)
    
    hl_range = high - low
    hl_safe = np.where(hl_range == 0, 1e-9, hl_range)
    upper_wick = (high - np.maximum(close, open_px)) / hl_safe
    lower_wick = (np.minimum(close, open_px) - low) / hl_safe
    body_ratio = np.abs(close - open_px) / hl_safe
    
    ema_9 = ta.EMA(close, timeperiod=9)
    ema_21 = ta.EMA(close, timeperiod=21)
    ema_50 = ta.EMA(close, timeperiod=50)
    ema_200 = ta.EMA(close, timeperiod=200)
    
    rsi = ta.RSI(close, timeperiod=14)
    vol_sma = ta.SMA(volume, timeperiod=20)
    vol_safe = np.where(vol_sma == 0, 1e-9, vol_sma)
    vol_spike = volume / vol_safe
    
    rolling_high_24 = ta.MAX(high, timeperiod=24)
    rolling_low_12 = ta.MIN(low, timeperiod=12)
    bbu, bbm, bbl = ta.BBANDS(close, timeperiod=20, nbdevup=2.0, nbdevdn=2.0, matype=0)
    
    macd, macdsignal, macdhist = ta.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
    shift_macdhist = np.roll(macdhist, 1)
    
    # Macro downtrend: close < ema_200 and ema_50 < ema_200
    macro_down = (close < ema_200) & (ema_50 < ema_200) & (close < open_px)
    
    # 1. TAG 741: Liquidity Sweep Fakeout Rejection
    shift_high_24 = np.roll(rolling_high_24, 1)
    cond_741 = (
        macro_down
        & (high > shift_high_24)
        & (close < shift_high_24)
        & (upper_wick >= 0.38)
        & (vol_spike >= 1.25)
        & (rsi >= 44.0) & (rsi <= 68.0)
    )
    
    # 2. TAG 742: Fair Value Gap Retest Failure
    shift_low_2 = np.roll(low, 2)
    has_fvg = (shift_low_2 > np.roll(high, 1))
    cond_742 = (
        macro_down
        & (high >= np.roll(ema_21, 1) * 0.998)
        & (close < ema_21)
        & (upper_wick >= 0.35)
        & (vol_spike >= 1.20)
        & (rsi >= 42.0) & (rsi <= 58.0)
        & (close < ema_9)
    )
    
    # 3. TAG 743: Market Structure Shift (Gãy đáy hồi gần nhất)
    shift_low_12 = np.roll(rolling_low_12, 1)
    cond_743 = (
        macro_down
        & (close < shift_low_12)
        & (body_ratio >= 0.45)
        & (lower_wick <= 0.25)
        & (macdhist < 0) & (macdhist < shift_macdhist)
        & (vol_spike >= 1.30)
        & (rsi >= 33.0) & (rsi <= 50.0)
    )
    
    # Measure forward returns for candidate entries (over next 24 bars = 2h)
    for tag_name, cond in [('741', cond_741), ('742', cond_742), ('743', cond_743)]:
        sig_indices = np.where(cond)[0]
        for idx in sig_indices:
            if idx + 24 < len(close):
                entry_px = close[idx]
                min_px = np.min(low[idx+1:idx+25])
                max_px = np.max(high[idx+1:idx+25])
                exit_px = close[idx+24]
                # Short return: (entry_px - exit_px) / entry_px * 5 (5x leverage)
                roe = (entry_px - exit_px) / entry_px * 5.0
                max_favorable_roe = (entry_px - min_px) / entry_px * 5.0
                max_adverse_roe = (entry_px - max_px) / entry_px * 5.0
                results[tag_name].append({
                    'pair': pair_name,
                    'date': df['date'].iloc[idx],
                    'roe': roe,
                    'mfe': max_favorable_roe,
                    'mae': max_adverse_roe,
                    'win': roe > 0
                })

for t, res in results.items():
    if not res:
        print(f"Tag {t}: 0 signals found.")
        continue
    df_res = pd.DataFrame(res)
    winrate = (df_res['win'].mean()) * 100
    avg_roe = df_res['roe'].mean() * 100
    avg_mfe = df_res['mfe'].mean() * 100
    print(f"Tag {t}: {len(df_res)} signals | Winrate: {winrate:.1f}% | Avg ROE (2h hold): {avg_roe:+.2f}% | Max Potential ROE: {avg_mfe:+.2f}%")

