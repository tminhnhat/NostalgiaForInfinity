import os
import glob
import pandas as pd
import numpy as np
import talib.abstract as ta

data_path = "user_data/data/binance/futures"
pair_files = glob.glob(f"{data_path}/*_USDT_USDT-5m-futures.feather")

print(f"Found {len(pair_files)} pairs for 5m data.")

# Let's test Tag 724 rules
def eval_rule(rule_name, high_mult=0.998, require_prev_green=False, require_ema50_slope=False, require_below_ema21=False, require_rsi_1h=False):
    total_signals = 0
    signals_list = []
    
    for f in pair_files:
        pair_name = os.path.basename(f).replace("-5m-futures.feather", "").replace("_", "/")
        df = pd.read_feather(f)
        df_1h_file = f.replace("-5m-futures.feather", "-1h-futures.feather")
        if not os.path.exists(df_1h_file):
            continue
        df_1h = pd.read_feather(df_1h_file)
        
        # 60 day timerange: 2026-08-11 to 2026-10-10
        df = df[(df['date'] >= '2026-08-11') & (df['date'] <= '2026-10-10')].copy()
        if df.empty:
            continue
            
        c = df['close'].to_numpy(copy=False)
        h = df['high'].to_numpy(copy=False)
        l = df['low'].to_numpy(copy=False)
        o = df['open'].to_numpy(copy=False)
        v = df['volume'].to_numpy(copy=False)
        
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
        
        is_sunday = df['date'].dt.dayofweek.to_numpy() == 6
        
        # Base 724 conditions
        cond = (
            (v > 0)
            & (ema_50 < ema_200)
            & (h >= ema_50 * high_mult)
            & (c < ema_50)
            & (c < o)
            & (upper_wick_ratio >= 0.38)
            & (vol_spike_ratio >= 1.25)
            & (rsi_14 >= 44.0) & (rsi_14 <= 58.0)
            & (~is_sunday)
        )
        
        if require_prev_green:
            shift_c = np.roll(c, 1)
            shift_o = np.roll(o, 1)
            cond = cond & (shift_c > shift_o)
            
        if require_ema50_slope:
            shift_ema_50 = np.roll(ema_50, 1)
            cond = cond & (ema_50 < shift_ema_50)
            
        if require_below_ema21:
            cond = cond & (c < ema_21)
            
        indices = np.where(cond)[0]
        for idx in indices:
            signals_list.append({
                'pair': pair_name,
                'date': df.iloc[idx]['date'],
                'close': c[idx],
                'high': h[idx],
                'ema_50': ema_50[idx],
            })
            
    return pd.DataFrame(signals_list)

# Baseline
res_base = eval_rule("Baseline", high_mult=0.998)
print(f"Baseline signals: {len(res_base)}")

# Option A: high >= ema_50 * 0.9995 (Actually tests EMA 50)
res_a = eval_rule("A_TouchEMA50", high_mult=0.9995)
print(f"Option A (Touch EMA50) signals: {len(res_a)}")

# Option B: require_prev_green (True relief bounce)
res_b = eval_rule("B_PrevGreen", high_mult=0.998, require_prev_green=True)
print(f"Option B (Prev Green) signals: {len(res_b)}")

# Option C: require_ema50_slope (EMA 50 downward slope)
res_c = eval_rule("C_Slope", high_mult=0.998, require_ema50_slope=True)
print(f"Option C (Slope) signals: {len(res_c)}")

# Check 2026-08-31 04:45 in each
for name, res in [("Baseline", res_base), ("Option A", res_a), ("Option B", res_b), ("Option C", res_c)]:
    if not res.empty:
        aug31 = res[res['date'].astype(str).str.contains("2026-08-31 04:45")]
        print(f"Signals at 2026-08-31 04:45 in {name}: {len(aug31)} pairs ({aug31['pair'].tolist() if not aug31.empty else []})")
