import pandas as pd
import numpy as np
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")

cases = [
    ("FF/USDT:USDT", "user_data/data/binance/futures/FF_USDT_USDT-5m-futures.feather", "2026-09-21 01:40:00+00:00", -55.10, "FF"),
    ("ALGO/USDT:USDT", "user_data/data/binance/futures/ALGO_USDT_USDT-5m-futures.feather", "2026-10-08 13:05:00+00:00", -47.66, "ALGO"),
    ("NXPC/USDT:USDT", "user_data/data/binance/futures/NXPC_USDT_USDT-5m-futures.feather", "2026-10-15 23:35:00+00:00", -31.01, "NXPC"),
    ("BTW/USDT:USDT", "user_data/data/binance/futures/BTW_USDT_USDT-5m-futures.feather", "2026-10-21 11:55:00+00:00", -32.50, "BTW"),
    ("PHA/USDT:USDT", "user_data/data/binance/futures/PHA_USDT_USDT-5m-futures.feather", "2026-10-23 18:05:00+00:00", -16.92, "PHA"),
    ("GTC/USDT:USDT", "user_data/data/binance/futures/GTC_USDT_USDT-5m-futures.feather", "2026-10-28 12:40:00+00:00", -31.32, "GTC"),
    ("HUMA/USDT:USDT", "user_data/data/binance/futures/HUMA_USDT_USDT-5m-futures.feather", "2026-11-04 14:01:00+00:00", -23.35, "HUMA"),
    ("AXL/USDT:USDT", "user_data/data/binance/futures/AXL_USDT_USDT-5m-futures.feather", "2026-10-19 05:16:00+00:00", -17.01, "AXL"),
]

def add_pnd_features(df):
    high_72h = df["high"].rolling(window=864, min_periods=50).max()
    low_72h = df["low"].rolling(window=864, min_periods=50).min()
    df["pump_surge"] = (high_72h - low_72h) / np.maximum(low_72h, 1e-5)
    df["drop_peak"] = (df["close"] - high_72h) / np.maximum(high_72h, 1e-5)
    
    vol_24h = df["volume"].rolling(window=288, min_periods=20).sum()
    vol_7d_med = vol_24h.rolling(window=2016, min_periods=100).median()
    df["vol_ratio"] = vol_24h / np.maximum(vol_7d_med, 1e-5)
    
    p_24h_ago = df["close"].shift(288)
    df["roc_24h"] = (df["close"] - p_24h_ago) / np.maximum(p_24h_ago, 1e-5)
    
    p_4h_ago = df["close"].shift(48)
    df["roc_4h"] = (df["close"] - p_4h_ago) / np.maximum(p_4h_ago, 1e-5)
    
    c1 = (df["pump_surge"] >= 0.40) & (df["drop_peak"] <= -0.22) & (df["vol_ratio"] >= 2.2)
    c2 = (df["pump_surge"] >= 0.65) & (df["drop_peak"] <= -0.30) & (df["roc_4h"] <= -0.10)
    c3 = (df["roc_24h"] <= -0.20) & (df["vol_ratio"] >= 2.5)
    df["is_pnd"] = c1 | c2 | c3
    return df

print("=" * 105)
print("VERIFICATION OF DISASTER TRADES UNDER ASYMMETRIC P&D GUARD (v8.5)")
print("=" * 105)
print(f"{'Pair':<12} | {'Entry Date (UTC)':<16} | {'Actual Loss':<11} | {'Surge 72h':<10} | {'Drop Peak':<10} | {'Vol Ratio':<10} | {'ROC 4h':<9} | {'PND Guard Status'}")
print("-" * 105)

saved_loss = 0.0
for pair, f, dt_str, actual_loss, sym in cases:
    try:
        df = pd.read_feather(f)
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
        df = add_pnd_features(df)
        dt = pd.to_datetime(dt_str)
        idx = df.index.get_loc(dt) if dt in df.index else df.index.searchsorted(dt)
        row = df.iloc[idx]
        is_blocked = bool(row['is_pnd'])
        if is_blocked:
            status = "BLOCKED (Long Suppressed)"
            saved_loss += abs(actual_loss)
        else:
            status = "ALLOWED"
            
        print(f"{sym:<12} | {dt_str[:16]:<16} | {actual_loss:+7.2f} USDT | {row['pump_surge']*100:>8.1f}% | {row['drop_peak']*100:>8.1f}% | {row['vol_ratio']:>8.1f}x | {row['roc_4h']*100:>7.1f}% | {status}")
    except Exception as e:
        print(f"{sym:<12} | Error: {e}")

print("-" * 105)
print(f"Total Capital Saved from Blocked Disaster Trades: +{saved_loss:.2f} USDT")
print("=" * 105)

