import pandas as pd
import glob
import os

data_dir = 'user_data/data/binance/futures'

def check_pair_candles(pair_filename, start_dt, end_dt):
    matches = glob.glob(os.path.join(data_dir, f"{pair_filename}-5m-futures.feather")) + glob.glob(os.path.join(data_dir, f"{pair_filename}-5m-futures.parquet"))
    if not matches:
        print(f"No data for {pair_filename}")
        return
    fpath = matches[0]
    if fpath.endswith('.feather'):
        df = pd.read_feather(fpath)
    else:
        df = pd.read_json(fpath)
    df['date'] = pd.to_datetime(df['date'])
    sub = df[(df['date'] >= start_dt) & (df['date'] <= end_dt)]
    print(f"\n=== {pair_filename} from {start_dt} to {end_dt} ===")
    for _, row in sub.iterrows():
        o, h, l, c, v = row['open'], row['high'], row['low'], row['close'], row['volume']
        print(f"{row['date']} | O={o:.4f} H={h:.4f} L={l:.4f} C={c:.4f} V={v:.1f}")

check_pair_candles("MSTR_USDT_USDT", "2026-07-01 12:00:00", "2026-07-01 14:00:00")
check_pair_candles("STRK_USDT_USDT", "2026-07-01 12:50:00", "2026-07-01 14:00:00")
check_pair_candles("PUMP_USDT_USDT", "2026-05-27 04:00:00", "2026-05-27 05:00:00")
check_pair_candles("PYTH_USDT_USDT", "2026-06-02 12:00:00", "2026-06-02 14:40:00")
