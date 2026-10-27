import pandas as pd
import numpy as np
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

df_btc_1h = pd.read_feather(os.path.join(data_dir, "BTC_USDT_USDT-1h-futures.feather"))
df_btc_1h['date'] = pd.to_datetime(df_btc_1h['date'])
df_btc_5m = pd.read_feather(os.path.join(data_dir, "BTC_USDT_USDT-5m-futures.feather"))
df_btc_5m['date'] = pd.to_datetime(df_btc_5m['date'])

for t in trades_702:
    pair_clean = t['pair'].replace('/', '_').replace(':', '_')
    df_5m = pd.read_feather(os.path.join(data_dir, f"{pair_clean}-5m-futures.feather"))
    df_5m['date'] = pd.to_datetime(df_5m['date'])
    op_dt = pd.to_datetime(t['open_date'])
    idx = df_5m[df_5m['date'] == op_dt].index[0]
    sig_c = df_5m.iloc[idx - 1]
    
    # BTC 5m return in last 3 candles (15m)
    b_idx = df_btc_5m[df_btc_5m['date'] == sig_c['date']].index[0]
    b_ret_3 = (df_btc_5m.iloc[b_idx]['close'] - df_btc_5m.iloc[b_idx-3]['close']) / df_btc_5m.iloc[b_idx-3]['close'] * 100
    b_ret_6 = (df_btc_5m.iloc[b_idx]['close'] - df_btc_5m.iloc[b_idx-6]['close']) / df_btc_5m.iloc[b_idx-6]['close'] * 100
    
    # Pair vol vs 10-period SMA
    vol_sma10 = df_5m.loc[max(0, idx-11):idx-2, 'volume'].mean()
    vol_ratio = sig_c['volume'] / vol_sma10 if vol_sma10 > 0 else 1.0
    
    print(f"{t['pair'].split('/')[0]:<5} | date={str(sig_c['date'])[:16]} | ROE={t['profit_ratio']*100:+.2f}% | btc_ret3={b_ret_3:+.2f}% | btc_ret6={b_ret_6:+.2f}% | pair_v_ratio={vol_ratio:.2f}")
