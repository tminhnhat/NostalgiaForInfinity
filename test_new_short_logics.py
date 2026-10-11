import glob
import pandas as pd
import numpy as np
import talib.abstract as ta

files = glob.glob("user_data/data/binance/futures/*_USDT_USDT-5m-futures.feather")
print(f"Total pairs to analyze: {len(files)}")

# Let's test candidate setups on sample pairs: ARB, OP, SUI, APT, NEAR, DOGE, BCH, INJ, FET, LINK, LTC, DOT, AVAX, TIA
sample_bases = ['ARB', 'OP', 'SUI', 'APT', 'NEAR', 'DOGE', 'BCH', 'INJ', 'FET', 'LINK', 'LTC', 'DOT', 'AVAX', 'TIA', 'BTC', 'ETH']

def evaluate_signals(df):
    close = df['close'].to_numpy()
    high = df['high'].to_numpy()
    low = df['low'].to_numpy()
    open_px = df['open'].to_numpy()
    volume = df['volume'].to_numpy()
    n = len(df)
    if n < 300:
        return {}

    ema9 = ta.EMA(close, timeperiod=9)
    ema21 = ta.EMA(close, timeperiod=21)
    ema50 = ta.EMA(close, timeperiod=50)
    ema200 = ta.EMA(close, timeperiod=200)
    rsi14 = ta.RSI(close, timeperiod=14)
    macd, macdsig, macdhist = ta.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
    bbu, bbm, bbl = ta.BBANDS(close, timeperiod=20, nbdevup=2.0, nbdevdn=2.0, matype=0)
    
    vol_sma20 = ta.SMA(volume, timeperiod=20)
    vol_spike = volume / np.where(vol_sma20==0, 1e-9, vol_sma20)
    
    hl = high - low
    hl_safe = np.where(hl == 0, 1e-9, hl)
    upper_wick = (high - np.maximum(close, open_px)) / hl_safe
    lower_wick = (np.minimum(close, open_px) - low) / hl_safe
    body = np.abs(close - open_px) / hl_safe
    
    is_sunday = df['date'].dt.dayofweek.to_numpy() == 6
    
    # Candidate 1: EMA 50 Relief Pullback Rejection in Downtrend (Tag 742)
    prev_green = np.roll(close > open_px, 1)
    cond_ema50_reject = (
        (volume > 0)
        & (ema50 < ema200)
        & (close < ema200)
        & prev_green
        & (high >= ema50 * 0.998)
        & (close < ema50)
        & (close < open_px)
        & (upper_wick >= 0.35)
        & (vol_spike >= 1.20)
        & (rsi14 >= 44.0) & (rsi14 <= 58.0)
        & (~is_sunday)
    )
    
    # Candidate 2: Bearish Divergence in Pullback (Tag 741)
    # Higher high in 24 candles vs lower high in RSI
    rolling_high_24 = ta.MAX(high, timeperiod=24)
    shift_rh_24 = np.roll(rolling_high_24, 1)
    shift_rsi = np.roll(rsi14, 1)
    cond_bear_div = (
        (volume > 0)
        & (ema50 < ema200)
        & (close < ema200)
        & (high > shift_rh_24)
        & (close < shift_rh_24) # SFP / rejection
        & (upper_wick >= 0.38)
        & (close < open_px)
        & (rsi14 >= 58.0)
        & (vol_spike >= 1.25)
        & (~is_sunday)
    )
    
    # Candidate 3: BB Squeeze Breakdown Expansion (Tag 743)
    bb_width = (bbu - bbl) / bbm
    bb_width_sma = ta.SMA(bb_width, timeperiod=20)
    cond_bb_squeeze_break = (
        (volume > 0)
        & (ema50 < ema200)
        & (close < ema200)
        & (bb_width < bb_width_sma * 0.85) # previous tight squeeze
        & (close < bbl) # breakdown band
        & (close < open_px)
        & (body >= 0.50) # strong red candle
        & (vol_spike >= 1.50)
        & (rsi14 > 32.0) & (rsi14 < 46.0)
        & (~is_sunday)
    )
    
    return {
        'ema50_reject': np.where(cond_ema50_reject)[0],
        'bear_div': np.where(cond_bear_div)[0],
        'bb_squeeze': np.where(cond_bb_squeeze_break)[0]
    }

# Test forward returns on sample pairs
results = {'ema50_reject': [], 'bear_div': [], 'bb_squeeze': []}

for b in sample_bases:
    f_match = glob.glob(f"user_data/data/binance/futures/{b}_USDT_USDT-5m-futures.feather")
    if not f_match:
        continue
    df = pd.read_feather(f_match[0])
    df['date'] = pd.to_datetime(df['date'], utc=True)
    # filter timerange 2026-09-10 to 2026-10-10
    df = df[(df['date'] >= '2026-09-10') & (df['date'] <= '2026-10-10')].reset_index(drop=True)
    if len(df) < 100:
        continue
    signals = evaluate_signals(df)
    c_arr = df['close'].to_numpy()
    
    for sig_name, idxs in signals.items():
        for i in idxs:
            if i + 36 < len(c_arr): # evaluate 3h forward (36 candles)
                entry_p = c_arr[i]
                # max favorable short move (lowest price in next 36 candles)
                lowest = np.min(c_arr[i+1:i+37])
                highest = np.max(c_arr[i+1:i+37])
                max_gain = (entry_p - lowest) / entry_p * 100 * 5 # 5x lev
                max_loss = (highest - entry_p) / entry_p * 100 * 5
                final_p = (entry_p - c_arr[i+36]) / entry_p * 100 * 5
                results[sig_name].append({
                    'pair': b,
                    'max_gain': max_gain,
                    'max_loss': max_loss,
                    'final_p': final_p,
                    'win': max_gain >= 5.0 and max_loss <= 15.0 # target +1% price (5% margin) before 3% loss
                })

for sig_name, res_list in results.items():
    if not res_list:
        continue
    df_r = pd.DataFrame(res_list)
    print(f"\n--- {sig_name.upper()} ---")
    print(f"Total triggers: {len(df_r)}")
    print(f"Average Max Gain (5x): {df_r['max_gain'].mean():.2f}%")
    print(f"Average Max Loss (5x): {df_r['max_loss'].mean():.2f}%")
    print(f"Winrate (Target 5% gain before 15% DD): {df_r['win'].mean()*100:.1f}%")
