import pandas as pd
import numpy as np

# Load feather 5m for MSTR, STRK, PUMP, PYTH
pairs = {
    'MSTR': ('user_data/data/binance/futures/MSTR_USDT_USDT-5m-futures.feather', '2026-07-01 12:40:00', '2026-07-01 13:35:00', 86.29),
    'STRK': ('user_data/data/binance/futures/STRK_USDT_USDT-5m-futures.feather', '2026-07-01 13:10:00', '2026-07-01 13:30:00', 0.0291),
    'PUMP': ('user_data/data/binance/futures/PUMP_USDT_USDT-5m-futures.feather', '2026-05-27 04:20:00', '2026-05-27 04:30:00', 0.0018),
    'PYTH': ('user_data/data/binance/futures/PYTH_USDT_USDT-5m-futures.feather', '2026-06-02 12:20:00', '2026-06-02 14:20:00', 0.0408)
}

for name, (fpath, open_d, close_d, open_r) in pairs.items():
    df = pd.read_feather(fpath)
    df['date'] = pd.to_datetime(df['date'])
    sub = df[(df['date'] >= open_d) & (df['date'] <= close_d)]
    print(f"=== {name} Trade Details ===")
    for _, r in sub.iterrows():
        min_rate = r['low']
        max_rate = r['high']
        close_rate = r['close']
        cur_prof_close = (open_r - close_rate) / open_r * 5.0
        cur_prof_low = (open_r - min_rate) / open_r * 5.0
        print(f"  {r['date']} | C_prof={cur_prof_close*100:+.2f}% | L_prof(MFE)={cur_prof_low*100:+.2f}% | C={r['close']} L={r['low']} H={r['high']}")
