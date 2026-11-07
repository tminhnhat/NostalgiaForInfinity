import pandas as pd
import numpy as np
import sys

sys.stdout.reconfigure(encoding="utf-8")

# Let's inspect the entry moments of the bad trades:
# FF: 2026-09-21 01:40
# HUMA: 2026-11-04 14:01
# GTC: 2026-10-28 12:40
# PHA: 2026-10-23 18:05
# BTW: 2026-10-21 11:55
# NXPC: 2026-10-15 23:35
# AXL: 2026-10-19 05:16
# ALGO: 2026-10-08 13:05

cases = [
    ("FF_USDT_USDT", "2026-09-21 01:40:00+00:00", "42"),
    ("HUMA_USDT_USDT", "2026-11-04 14:01:00+00:00", "46"),
    ("GTC_USDT_USDT", "2026-10-28 12:40:00+00:00", "6"),
    ("PHA_USDT_USDT", "2026-10-23 18:05:00+00:00", "63"),
    ("BTW_USDT_USDT", "2026-10-21 11:55:00+00:00", "44"),
    ("NXPC_USDT_USDT", "2026-10-15 23:35:00+00:00", "4"),
    ("AXL_USDT_USDT", "2026-10-19 05:16:00+00:00", "64"),
    ("ALGO_USDT_USDT", "2026-10-08 13:05:00+00:00", "145"),
]

for pair_file, entry_time_str, tag in cases:
    f5m = f"user_data/data/binance/futures/{pair_file}-5m-futures.feather"
    f1h = f"user_data/data/binance/futures/{pair_file}-1h-futures.feather"
    f1d = f"user_data/data/binance/futures/{pair_file}-1d-futures.feather"
    
    df5 = pd.read_feather(f5m)
    entry_dt = pd.to_datetime(entry_time_str)
    
    # Filter up to entry
    sub = df5[df5['date'] <= entry_dt].copy()
    if len(sub) < 288:
        continue
    
    curr_close = sub['close'].iloc[-1]
    
    # Rolling 24h (288 candles) and 72h (864 candles)
    high_24h = sub['high'].tail(288).max()
    high_72h = sub['high'].tail(864).max()
    low_24h = sub['low'].tail(288).min()
    low_72h = sub['low'].tail(864).min()
    
    # Surge from 72h low to 72h high (How massive was the pump?)
    pump_surge_pct = ((high_72h - low_72h) / low_72h) * 100.0
    
    # Drop from the peak
    drop_from_24h_high = ((curr_close - high_24h) / high_24h) * 100.0
    drop_from_72h_high = ((curr_close - high_72h) / high_72h) * 100.0
    
    # 24h volume vs previous 7-day median 24h volume
    vol_24h = sub['volume'].tail(288).sum()
    vol_7d_med_24h = sub['volume'].tail(288 * 7).rolling(288).sum().median()
    vol_surge_ratio = vol_24h / max(vol_7d_med_24h, 1e-5)
    
    # 24h Price Change (ROC_288)
    p_24h_ago = sub['close'].iloc[-288]
    roc_24h = ((curr_close - p_24h_ago) / p_24h_ago) * 100.0
    
    # 72h Price Change (ROC_864)
    idx_72h = -864 if len(sub) >= 864 else 0
    p_72h_ago = sub['close'].iloc[idx_72h]
    roc_72h = ((curr_close - p_72h_ago) / p_72h_ago) * 100.0
    
    print(f"=== {pair_file.replace('_USDT_USDT', '')} (Tag {tag}) at {entry_time_str} ===")
    print(f"  Close at entry: {curr_close:.6f}")
    print(f"  72h Range: Low {low_72h:.6f} ➔ Peak {high_72h:.6f} (Pump Surge: +{pump_surge_pct:.1f}%)")
    print(f"  Position relative to Peak: Drop from 24h High: {drop_from_24h_high:.1f}% | Drop from 72h High: {drop_from_72h_high:.1f}%")
    print(f"  Volume Surge Ratio (24h Vol / 7d Med Vol): {vol_surge_ratio:.2f}x")
    print(f"  24h ROC: {roc_24h:+.1f}% | 72h ROC: {roc_72h:+.1f}%")
    print()

