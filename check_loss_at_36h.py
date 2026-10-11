import zipfile
import json
import pandas as pd
import glob

zp = 'user_data/backtest_results/backtest-result-2026-10-11_12-11-43.zip'
with zipfile.ZipFile(zp) as z:
    for n in z.namelist():
        if n.endswith('.json') and not n.endswith('.meta.json'):
            d = json.loads(z.read(n).decode('utf-8'))
            if 'strategy' in d:
                trades = d['strategy']['NostalgiaForInfinityX8_Combined']['trades']
                break

losses = [t for t in trades if t.get('profit_abs', 0) < 0]

for l in losses:
    pair = l['pair']
    open_date = l['open_date']
    close_date = l['close_date']
    open_rate = l['open_rate']
    base = pair.split('/')[0]
    f_files = glob.glob(f"user_data/data/binance/futures/{base}_USDT_USDT-5m-futures.feather")
    if not f_files:
        continue
    df = pd.read_feather(f_files[0])
    df['date'] = pd.to_datetime(df['date'], utc=True)
    open_t = pd.to_datetime(open_date)
    sub = df[df['date'] >= open_t].copy()
    if len(sub) == 0:
        continue
    # find candle at +36h
    t_36h = open_t + pd.Timedelta(hours=36)
    c_36h = sub[sub['date'] >= t_36h]
    if len(c_36h) > 0:
        rate_36h = c_36h.iloc[0]['close']
        p_pct_36h = (open_rate - rate_36h) / open_rate * 100 * 5 # 5x leverage
        print(f"{pair:<14} | Open: {open_date} | Actual Dur: {l['trade_duration']/60:.1f}h | Loss: {l['profit_abs']:.2f}$ | Profit at 36h: {p_pct_36h:.1f}%")
    else:
        print(f"{pair:<14} | Open: {open_date} | Dur < 36h ({l['trade_duration']/60:.1f}h) | Loss: {l['profit_abs']:.2f}$")
