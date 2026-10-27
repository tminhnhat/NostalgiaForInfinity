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

print("Checking Pair 1H RSI for all 16 trades:")
for t in trades_702:
    pair_clean = t['pair'].replace('/', '_').replace(':', '_')
    f_1h = os.path.join(data_dir, f"{pair_clean}-1h-futures.feather")
    df_1h = pd.read_feather(f_1h)
    df_1h['date'] = pd.to_datetime(df_1h['date'])
    df_1h['rsi_1h'] = ta.RSI(df_1h['close'].to_numpy(), timeperiod=14)
    op_dt = pd.to_datetime(t['open_date'])
    sub = df_1h[df_1h['date'] <= op_dt]
    r = sub.iloc[-1]
    print(f"{t['pair'].split('/')[0]:<5} | date={str(op_dt)[:16]} | ROE={t['profit_ratio']*100:+.2f}% | Pair_1h_RSI={r['rsi_1h']:.2f}")
