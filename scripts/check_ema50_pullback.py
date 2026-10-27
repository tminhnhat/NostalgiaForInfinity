import pandas as pd
import numpy as np
import os

data_dir = 'user_data/data/binance/futures'

def check_trade_ema50_1h(pair, open_dt, close_dt):
    f_5m = os.path.join(data_dir, f"{pair}-5m-futures.feather")
    f_1h = os.path.join(data_dir, f"{pair}-1h-futures.feather")
    df_5m = pd.read_feather(f_5m)
    df_1h = pd.read_feather(f_1h)
    df_5m['date'] = pd.to_datetime(df_5m['date'])
    df_1h['date'] = pd.to_datetime(df_1h['date'])
    df_1h['ema50_1h'] = df_1h['close'].ewm(span=50).mean()
    
    # Merge 1h ema50 to 5m
    merged = pd.merge_asof(df_5m.sort_values('date'), df_1h[['date', 'ema50_1h']].sort_values('date'), on='date')
    sub = merged[(merged['date'] >= open_dt) & (merged['date'] <= close_dt)]
    print(f"\n=== {pair} during trade ===")
    open_p = sub.iloc[0]['open']
    for _, r in sub.iterrows():
        p_loss = (r['close'] - open_p) / open_p * 5.0 # ROE loss
        above_ema = r['close'] > r['ema50_1h']
        if p_loss > 0.05: # only print when loss > 5%
            print(f"  {r['date']} | C={r['close']} | EMA50_1h={r['ema50_1h']:.4f} | Loss={p_loss*100:+.2f}% | Above_EMA50_1h={above_ema}")

check_trade_ema50_1h('NEAR_USDT_USDT', '2026-05-06 19:50:00', '2026-05-07 02:00:00')
check_trade_ema50_1h('PYTH_USDT_USDT', '2026-06-02 12:15:00', '2026-06-02 14:30:00')
check_trade_ema50_1h('MSTR_USDT_USDT', '2026-07-01 12:35:00', '2026-07-01 13:40:00')
