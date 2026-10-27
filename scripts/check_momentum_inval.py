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

print("Checking Tag 702 Momentum Invalidation (duration >= 30m, profit <= -0.02, macdhist > 0, close > ema21):")
for t in trades_702:
    pair_clean = t['pair'].replace('/', '_').replace(':', '_')
    df_5m = pd.read_feather(os.path.join(data_dir, f"{pair_clean}-5m-futures.feather"))
    df_5m['date'] = pd.to_datetime(df_5m['date'])
    close = df_5m['close'].to_numpy()
    ema21 = ta.EMA(close, timeperiod=21)
    macd, macdsignal, macdhist = ta.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
    df_5m['ema21'] = ema21
    df_5m['macdhist'] = macdhist
    
    op_dt = pd.to_datetime(t['open_date'])
    cl_dt = pd.to_datetime(t['close_date'])
    open_rate = t['open_rate']
    
    sub = df_5m[(df_5m['date'] >= op_dt) & (df_5m['date'] <= cl_dt)]
    inval_triggered = False
    inval_time = None
    inval_profit = None
    for _, r in sub.iterrows():
        dur_mins = (r['date'] - op_dt).total_seconds() / 60.0
        cur_prof = (open_rate - r['close']) / open_rate * 5.0
        if dur_mins >= 30 and cur_prof <= -0.035 and r['macdhist'] > 0 and r['close'] > r['ema21']:
            inval_triggered = True
            inval_time = r['date']
            inval_profit = cur_prof
            break
            
    print(f"{t['pair'].split('/')[0]:<5} | ROE={t['profit_ratio']*100:+.2f}% | Inval={inval_triggered} | time={str(inval_time)[:16] if inval_time else '-'} | prof={f'{inval_profit*100:+.2f}%' if inval_profit else '-'}")
