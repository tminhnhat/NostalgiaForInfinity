import pandas as pd
import numpy as np
import talib.abstract as ta
import os
import glob
import zipfile
import json

data_dir = 'user_data/data/binance/futures'

zips = sorted(glob.glob('user_data/backtest_results/backtest-result-*.zip'))
latest = zips[-1]
trades_702 = []
with zipfile.ZipFile(latest, 'r') as z:
    for n in z.namelist():
        if n.endswith('.json') and not n.endswith('.meta.json'):
            d = json.loads(z.read(n))
            if 'strategy' in d and isinstance(d['strategy'], dict):
                strat_data = d['strategy'].get('NostalgiaForInfinityX8_Combined_AI', {})
                if 'trades' in strat_data:
                    for t in strat_data['trades']:
                        if t.get('enter_tag') == '702 703 731_AI_PASS':
                            trades_702.append(t)

print("Checking Dist to BBL for 16 trades at signal candle:")
for t in trades_702:
    pair_clean = t['pair'].replace('/', '_').replace(':', '_')
    df_5m = pd.read_feather(os.path.join(data_dir, f"{pair_clean}-5m-futures.feather"))
    df_5m['date'] = pd.to_datetime(df_5m['date'])
    close = df_5m['close'].to_numpy()
    bbu, bbm, bbl = ta.BBANDS(close, timeperiod=20, nbdevup=2.0, nbdevdn=2.0)
    
    op_dt = pd.to_datetime(t['open_date'])
    idx = df_5m[df_5m['date'] == op_dt].index[0]
    sig_idx = idx - 1
    
    c = close[sig_idx]
    b_low = bbl[sig_idx]
    dist_bbl = (c - b_low) / c * 100.0
    
    print(f"{t['pair'].split('/')[0]:<5} | date={str(t['open_date'])[:16]} | ROE={t['profit_ratio']*100:+.2f}% | c={c:.4f} | bbl={b_low:.4f} | dist_bbl={dist_bbl:+.2f}%")
