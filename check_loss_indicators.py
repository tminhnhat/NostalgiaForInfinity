import zipfile
import json
import pandas as pd
import glob
import talib.abstract as ta

# Load trades from 12-11-43
zp = 'user_data/backtest_results/backtest-result-2026-10-11_12-11-43.zip'
with zipfile.ZipFile(zp) as z:
    for n in z.namelist():
        if n.endswith('.json') and not n.endswith('.meta.json'):
            d = json.loads(z.read(n).decode('utf-8'))
            if 'strategy' in d:
                trades = d['strategy']['NostalgiaForInfinityX8_Combined']['trades']
                break

losses = [t for t in trades if t.get('profit_abs', 0) < 0]

print("Analyzing indicator values at open_date for the 13 losses:")
for l in losses:
    pair = l['pair']
    open_date = l['open_date']
    base = pair.split('/')[0]
    # find feather file
    f_files = glob.glob(f"user_data/data/binance/futures/{base}_USDT_USDT-5m-futures.feather")
    if not f_files:
        print(f"No feather for {pair}")
        continue
    df = pd.read_feather(f_files[0])
    df['date'] = pd.to_datetime(df['date'], utc=True)
    row = df[df['date'] == pd.to_datetime(open_date)]
    if len(row) == 0:
        print(f"Row not found for {pair} at {open_date}")
        continue
    idx = row.index[0]
    sub_df = df.iloc[max(0, idx-100):idx+1].copy()
    rsi14 = ta.RSI(sub_df['close'].to_numpy(), timeperiod=14)[-1]
    fastk, fastd = ta.STOCHRSI(sub_df['close'].to_numpy(), timeperiod=14, fastk_period=3, fastd_period=3)
    k = fastk[-1]
    d = fastd[-1]
    
    print(f"{pair:<14} | Open: {open_date} | Tag: {l.get('enter_tag')} | RSI14: {rsi14:.1f} | StochRSI_K: {k:.1f} | StochRSI_D: {d:.1f} | Loss: {l.get('profit_abs'):.2f}$")
