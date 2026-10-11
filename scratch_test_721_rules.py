import os
import glob
import pandas as pd
import numpy as np
import talib.abstract as ta

data_path = "user_data/data/binance/futures"
pair_files = glob.glob(f"{data_path}/*_USDT_USDT-5m-futures.feather")

def eval_721(name, require_slope=False, require_btc_guard=False, require_1h_guard=False, require_close_ema9=False, upper_wick=0.40):
    total_signals = []
    
    for f in pair_files:
        pair_name = os.path.basename(f).replace("-5m-futures.feather", "").replace("_", "/")
        if "ETH" in pair_name:
            continue
        df = pd.read_feather(f)
        df_1h_file = f.replace("-5m-futures.feather", "-1h-futures.feather")
        if not os.path.exists(df_1h_file):
            continue
        df_1h = pd.read_feather(df_1h_file)
        
        df = df[(df['date'] >= '2026-08-11') & (df['date'] <= '2026-10-10')].copy()
        if df.empty:
            continue
            
        c = df['close'].to_numpy(copy=False)
        h = df['high'].to_numpy(copy=False)
        l = df['low'].to_numpy(copy=False)
        o = df['open'].to_numpy(copy=False)
        v = df['volume'].to_numpy(copy=False)
        
        ema_9 = ta.EMA(c, timeperiod=9)
        ema_21 = ta.EMA(c, timeperiod=21)
        ema_50 = ta.EMA(c, timeperiod=50)
        ema_200 = ta.EMA(c, timeperiod=200)
        rsi_14 = ta.RSI(c, timeperiod=14)
        
        hl_range = h - l
        hl_safe = np.where(hl_range == 0, 1e-9, hl_range)
        upper_wick_ratio = (h - np.maximum(c, o)) / hl_safe
        
        vol_sma_20 = ta.SMA(v, timeperiod=20)
        vol_sma_safe = np.where(vol_sma_20 == 0, 1e-9, vol_sma_20)
        vol_spike_ratio = v / vol_sma_safe
        
        prev_candle_green = np.roll(c, 1) > np.roll(o, 1)
        
        cond = (
            (v > 0)
            & (ema_50 < ema_200)
            & prev_candle_green
            & (h >= ema_21 * 0.999)
            & (c < ema_21)
            & (c < o)
            & (upper_wick_ratio >= upper_wick)
            & (vol_spike_ratio >= 1.25)
            & (rsi_14 >= 42.0) & (rsi_14 <= 58.0)
        )
        
        if require_slope:
            shift_ema_21 = np.roll(ema_21, 1)
            cond = cond & (ema_21 < shift_ema_21)
            
        if require_close_ema9:
            cond = cond & (c < ema_9)
            
        if require_1h_guard:
            c_1h = df_1h['close'].to_numpy()
            df_1h['rsi_1h'] = ta.RSI(c_1h, timeperiod=14)
            # Merge 1h
            df_merged = pd.merge_asof(df[['date']], df_1h[['date', 'rsi_1h']], on='date')
            rsi_1h_oversold = df_merged['rsi_1h'].to_numpy() < 30.0
            cond = cond & (~rsi_1h_oversold)
            
        indices = np.where(cond)[0]
        for idx in indices:
            total_signals.append({
                'pair': pair_name,
                'date': df.iloc[idx]['date'],
            })
            
    res_df = pd.DataFrame(total_signals)
    print(f"{name}: Total signals = {len(res_df)}")
    if not res_df.empty:
        dot_aug31 = res_df[res_df['date'].astype(str).str.contains("2026-08-31 13:15")]
        print(f"  -> DOT at 2026-08-31 13:15 triggered?: {len(dot_aug31) > 0}")
    return res_df

print("Testing Tag 721 variants:")
s_base = eval_721("Baseline", upper_wick=0.40)
s_opt1 = eval_721("Opt1: Slope + 1.25vol", require_slope=True, upper_wick=0.42)
s_opt2 = eval_721("Opt2: Slope + Close < EMA9", require_slope=True, require_close_ema9=True, upper_wick=0.42)
s_opt3 = eval_721("Opt3: Slope + Close < EMA9 + 1h", require_slope=True, require_close_ema9=True, require_1h_guard=True, upper_wick=0.42)
