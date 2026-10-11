import glob
import pandas as pd
import numpy as np
import talib.abstract as ta

files = glob.glob("user_data/data/binance/futures/*_USDT_USDT-5m-futures.feather")

# Load BTC data for cond_731 alignment
df_btc = pd.read_feather("user_data/data/binance/futures/BTC_USDT_USDT-5m-futures.feather")
df_btc['date'] = pd.to_datetime(df_btc['date'], utc=True)
df_btc_1h = pd.read_feather("user_data/data/binance/futures/BTC_USDT_USDT-1h-futures.feather")
df_btc_1h['date'] = pd.to_datetime(df_btc_1h['date'], utc=True)
df_btc_1h['btc_rsi_1h'] = ta.RSI(df_btc_1h['close'].to_numpy(), timeperiod=14)

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
    
    # Base cond_703
    cond_703 = (
        (volume > 0)
        & (ema9 < ema21) & (ema21 < ema50) & (ema50 < ema200)
        & (close < ema9) & (close < open_px)
        & (vol_spike >= 1.20)
        & (rsi14 > 30.0) & (rsi14 < 46.0)
        & (stoch_k >= 20.0)
        & (~is_sunday)
    )
    
    # BTC dumping proxy
    # merge BTC 1h RSI
    df_merged = pd.merge_asof(df[['date']], df_btc_1h[['date', 'btc_rsi_1h']], on='date')
    btc_dumping = df_merged['btc_rsi_1h'].fillna(50).to_numpy() < 48.0
    
    macro_bear = (close < ema200) & (ema50 < ema200) & (close < open_px) & (rsi14 > 32.0) & (~is_sunday)
    
    # SETUP 1: SFP High Rejection in Downtrend (Quét đỉnh ngắn hạn 24 nến rồi xả gập)
    rolling_high_24 = ta.MAX(high, timeperiod=24)
    shift_rh_24 = np.roll(rolling_high_24, 1)
    cond_sfp_bear = (
        (volume > 0)
        & (high > shift_rh_24) # quét qua đỉnh cũ 2h
        & (close < shift_rh_24) # đóng lọt lại dưới đỉnh
        & (close < open_px) # nến đỏ
        & (upper_wick >= 0.40) # râu trên từ chối
        & (vol_spike >= 1.30)
        & (close < ema21)
        & (ema50 < ema200)
        & btc_dumping
        & (~is_sunday)
    )
    
    # SETUP 2: EMA 50 Relief Pullback Rejection (Chạm cản EMA 50 bị đạp ngược)
    cond_ema50_reject = (
        (volume > 0)
        & (high >= ema50 * 0.998) & (close < ema50) # chạm EMA 50
        & (close < open_px)
        & (upper_wick >= 0.38)
        & (vol_spike >= 1.25)
        & (ema50 < ema200)
        & (rsi14 >= 44.0) & (rsi14 <= 56.0)
        & btc_dumping
        & (~is_sunday)
    )
    
    # SETUP 3: Bollinger Band Upper Rejection Scalp (cond_723 with BTC alignment)
    shift_bbm = np.roll(bbm, 3)
    cond_723_aligned = (
        (volume > 0)
        & (high >= bbu * 0.998) & (close < bbu * 0.995)
        & (bbm < shift_bbm)
        & (upper_wick >= 0.42)
        & (vol_spike >= 1.25)
        & (rsi14 >= 58.0)
        & (ema50 < ema200)
        & btc_dumping
        & (~is_sunday)
    )
    
    # SETUP 4: Donchian 48-candle (4h) Super Breakdown
    rolling_low_48 = ta.MAX(low, timeperiod=48)
    shift_rl_48 = np.roll(rolling_low_48, 1)
    cond_macro_breakdown = (
        (volume > 0)
        & (close < shift_rl_48)
        & (close < open_px)
        & (lower_wick <= 0.25)
        & (vol_spike >= 1.40)
        & (rsi14 > 32.0) & (rsi14 < 44.0)
        & (stoch_k >= 25.0)
        & cond_703
        & btc_dumping
        & (~is_sunday)
    )

    for s_name, s_mask in [
        ('1_SFP_Bear_Trap', cond_sfp_bear),
        ('2_EMA50_Pullback_Rejection', cond_ema50_reject),
        ('3_BB_Upper_Rejection', cond_723_aligned),
        ('4_Macro_Donchian_Breakdown', cond_macro_breakdown)
    ]:
        idxs = np.where(s_mask)[0]
        for i in idxs:
            if i + 36 < n_rows:
                entry = close[i]
                lowest = np.min(close[i+1:i+37])
                highest = np.max(close[i+1:i+37])
                gain_5x = (entry - lowest) / entry * 100 * 5
                loss_5x = (highest - entry) / entry * 100 * 5
                total_new_trades.append({
                    'setup': s_name,
                    'pair': pair_name,
                    'gain_5x': gain_5x,
                    'loss_5x': loss_5x,
                    'win': gain_5x >= 4.0 and loss_5x <= 12.0
                })

df_res = pd.DataFrame(total_new_trades)
print("=== KẾT QUẢ TEST CÁC SETUP CONFLUENCE ĐỒNG PHA BTC ===")
for setup_name, grp in df_res.groupby('setup'):
    print(f"\nSetup: {setup_name}")
    print(f"  Số tín hiệu: {len(grp)}")
    print(f"  Max Gain trung bình (5x): +{grp['gain_5x'].mean():.2f}%")
    print(f"  Max Loss trung bình (5x): -{grp['loss_5x'].mean():.2f}%")
    print(f"  Winrate đạt target trước stop: {grp['win'].mean()*100:.1f}%")
