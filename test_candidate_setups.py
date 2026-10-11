import glob
import pandas as pd
import numpy as np
import talib.abstract as ta

# Load all 25 pairs
files = glob.glob("user_data/data/binance/futures/*_USDT_USDT-5m-futures.feather")

total_new_trades = []

for f in files:
    pair_name = f.split('\\')[-1].split('_USDT')[0]
    df = pd.read_feather(f)
    df['date'] = pd.to_datetime(df['date'], utc=True)
    df = df[(df['date'] >= '2026-09-10') & (df['date'] <= '2026-10-10')].reset_index(drop=True)
    if len(df) < 200:
        continue
    
    close = df['close'].to_numpy()
    high = df['high'].to_numpy()
    low = df['low'].to_numpy()
    open_px = df['open'].to_numpy()
    volume = df['volume'].to_numpy()
    n_rows = len(df)
    
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
    
    is_sunday = df['date'].dt.dayofweek.to_numpy() == 6
    
    # StochRSI
    rsi_low = ta.MIN(rsi14, timeperiod=14)
    rsi_high = ta.MAX(rsi14, timeperiod=14)
    stoch_range = np.where(rsi_high - rsi_low == 0, 1e-9, rsi_high - rsi_low)
    raw_k = ((rsi14 - rsi_low) / stoch_range) * 100.0
    stoch_k = ta.SMA(raw_k, timeperiod=3)
    stoch_d = ta.SMA(stoch_k, timeperiod=3)
    
    # Macro bear
    macro_bear = (close < ema200) & (ema50 < ema200) & (close < open_px) & (rsi14 > 30.0) & (~is_sunday)
    
    # 1. BB Rejection Scalp (cond_723 confluence)
    shift_bbm = np.roll(bbm, 3)
    cond_723 = (
        (volume > 0)
        & (high >= bbu * 0.998)
        & (close < bbu * 0.995)
        & (bbm < shift_bbm)
        & (upper_wick >= 0.40)
        & (vol_spike >= 1.25)
        & (rsi14 >= 58.0)
    )
    sig_723 = cond_723 & macro_bear
    
    # 2. Lower High Price Action Rejection (Tag 724)
    rolling_h12 = ta.MAX(high, timeperiod=12)
    rolling_h24 = ta.MAX(high, timeperiod=24)
    shift_h24 = np.roll(rolling_h24, 12)
    cond_724 = (
        (volume > 0)
        & (rolling_h12 < shift_h24 * 0.995) # lower high confirmed
        & (high >= ema21 * 0.998) & (close < ema21) # test EMA 21
        & (upper_wick >= 0.35)
        & (vol_spike >= 1.20)
        & (rsi14 >= 42.0) & (rsi14 <= 56.0)
        & (stoch_k >= 30.0)
    )
    sig_724 = cond_724 & macro_bear
    
    # 3. MACD Zero Cross Breakdown (Tag 705)
    shift_macdhist = np.roll(macdhist, 1)
    cond_705 = (
        (volume > 0)
        & (shift_macdhist >= 0.0) & (macdhist < 0.0) # cross to red
        & (close < ema9) & (close < ema21)
        & (vol_spike >= 1.30)
        & (stoch_k >= 30.0) & (stoch_k <= 70.0)
        & (rsi14 > 35.0) & (rsi14 < 48.0)
    )
    sig_705 = cond_705 & macro_bear
    
    # Evaluate 24-candle forward outcome
    for sig_name, sig_mask in [('723_BB_Rejection', sig_723), ('724_Lower_High', sig_724), ('705_MACD_Cross', sig_705)]:
        idxs = np.where(sig_mask)[0]
        for i in idxs:
            if i + 24 < n_rows:
                entry = close[i]
                lowest = np.min(close[i+1:i+25])
                highest = np.max(close[i+1:i+25])
                gain_5x = (entry - lowest) / entry * 100 * 5
                loss_5x = (highest - entry) / entry * 100 * 5
                total_new_trades.append({
                    'setup': sig_name,
                    'pair': pair_name,
                    'gain_5x': gain_5x,
                    'loss_5x': loss_5x,
                    'win': gain_5x >= 5.0 and loss_5x <= 15.0 # hit 1% drop before 3% pump
                })

df_res = pd.DataFrame(total_new_trades)
print("=== KẾT QUẢ TEST CÁC ENTRY LOGIC SHORT MỚI ===")
for setup_name, grp in df_res.groupby('setup'):
    print(f"\nSetup: {setup_name}")
    print(f"  Số tín hiệu kích hoạt: {len(grp)}")
    print(f"  Lãi tối đa trung bình (x5): +{grp['gain_5x'].mean():.2f}%")
    print(f"  Sụt giảm tối đa trung bình (x5): -{grp['loss_5x'].mean():.2f}%")
    print(f"  Tỷ lệ thắng (Winrate đạt target trước stop): {grp['win'].mean()*100:.1f}%")
