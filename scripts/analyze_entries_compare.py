import pandas as pd
import numpy as np

def analyze_entry(pair, dt_str, label):
    f = f"user_data/data/binance/futures/{pair}-5m-futures.feather"
    df = pd.read_feather(f)
    dt = pd.to_datetime(dt_str)
    
    # Slice up to entry
    sub = df[df['date'] <= dt].copy()
    c = sub['close'].iloc[-1]
    
    # 72h surge & drop
    h72 = sub['high'].rolling(864, min_periods=50).max().iloc[-1]
    l72 = sub['low'].rolling(864, min_periods=50).min().iloc[-1]
    surge = (h72 - l72) / max(l72, 1e-5)
    drop = (c - h72) / max(h72, 1e-5)
    
    # 24h ROC
    c_24h = sub['close'].shift(288).iloc[-1]
    roc_24h = (c - c_24h) / max(c_24h, 1e-5)
    
    # 12h ROC
    c_12h = sub['close'].shift(144).iloc[-1]
    roc_12h = (c - c_12h) / max(c_12h, 1e-5)
    
    # 4h ROC
    c_4h = sub['close'].shift(48).iloc[-1]
    roc_4h = (c - c_4h) / max(c_4h, 1e-5)
    
    # Volume 24h ratio vs 7d median
    v24 = sub['volume'].rolling(288, min_periods=20).sum().iloc[-1]
    v7d = sub['volume'].rolling(288, min_periods=20).sum().rolling(2016, min_periods=100).median().iloc[-1]
    vratio = v24 / max(v7d, 1e-5)
    
    # EMAs
    ema50 = sub['close'].ewm(span=50).mean().iloc[-1]
    ema200 = sub['close'].ewm(span=200).mean().iloc[-1]
    
    # Distance to EMA200
    dist_ema200 = (c - ema200) / ema200
    
    # RSI 14
    delta = sub['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rs = gain / np.maximum(loss, 1e-5)
    rsi = 100 - (100 / (1 + rs)).iloc[-1]
    
    print(f"{label:<16} | Surge: {surge*100:5.1f}% | Drop: {drop*100:5.1f}% | ROC_24h: {roc_24h*100:5.1f}% | ROC_4h: {roc_4h*100:5.1f}% | RSI: {rsi:4.1f} | EMA200_dist: {dist_ema200*100:5.1f}% | VolR: {vratio:4.1f}x")

print("=== DISASTER TRADES ===")
analyze_entry("FF_USDT_USDT", "2026-09-21 01:40:00+00:00", "FF (Loss -55$)")
analyze_entry("HUMA_USDT_USDT", "2026-11-04 14:01:00+00:00", "HUMA (Loss -23$)")
analyze_entry("GTC_USDT_USDT", "2026-10-28 12:40:00+00:00", "GTC (Loss -31$)")
analyze_entry("PHA_USDT_USDT", "2026-10-23 18:05:00+00:00", "PHA (Loss -17$)")
analyze_entry("BTW_USDT_USDT", "2026-10-21 11:55:00+00:00", "BTW (Liq -32$)")
analyze_entry("NXPC_USDT_USDT", "2026-10-15 23:35:00+00:00", "NXPC (Loss -31$)")
analyze_entry("AXL_USDT_USDT", "2026-10-19 05:16:00+00:00", "AXL (Loss -17$)")
analyze_entry("ALGO_USDT_USDT", "2026-10-08 13:05:00+00:00", "ALGO_USDT (Loss -47$)")

print("\n=== WINNING BTW TRADES IN BACKTEST ===")
analyze_entry("BTW_USDT_USDT", "2026-10-05 06:45:00+00:00", "BTW (+123$)")
analyze_entry("BTW_USDT_USDT", "2026-10-23 18:30:00+00:00", "BTW (+116$)")
analyze_entry("BTW_USDT_USDT", "2026-10-26 19:15:00+00:00", "BTW (+82$)")
analyze_entry("BTW_USDT_USDT", "2026-08-24 10:50:00+00:00", "BTW (+30$)")
analyze_entry("BTW_USDT_USDT", "2026-09-05 00:55:00+00:00", "BTW (+27$)")
analyze_entry("BTW_USDT_USDT", "2026-06-21 16:45:00+00:00", "BTW (+20$)")

