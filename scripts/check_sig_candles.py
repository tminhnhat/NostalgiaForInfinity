import pandas as pd
import numpy as np
import glob
import zipfile
import json
import os

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

print(f"Checking signal candles for {len(trades_702)} trades...")
for t in trades_702:
    pair_clean = t['pair'].replace('/', '_').replace(':', '_')
    fpath = os.path.join(data_dir, f"{pair_clean}-5m-futures.feather")
    df = pd.read_feather(fpath)
    df['date'] = pd.to_datetime(df['date'])
    op_dt = pd.to_datetime(t['open_date'])
    idx = df[df['date'] == op_dt].index[0]
    # Nến sinh tín hiệu là nến trước đó (idx - 1)
    sig_c = df.iloc[idx - 1]
    
    # Check BTC at that candle
    df_btc = pd.read_feather(os.path.join(data_dir, "BTC_USDT_USDT-5m-futures.feather"))
    df_btc['date'] = pd.to_datetime(df_btc['date'])
    btc_idx = df_btc[df_btc['date'] == sig_c['date']].index[0]
    btc_c = df_btc.iloc[btc_idx]
    btc_ret3 = (btc_c['close'] - df_btc.iloc[btc_idx-3]['close']) / df_btc.iloc[btc_idx-3]['close'] * 100
    
    print(f"{t['pair'].split('/')[0]:<5} | sig_dt={str(sig_c['date'])[:16]} | profit={t['profit_ratio']*100:+.2f}% | pair_v={sig_c['volume']:<10.1f} | btc_ret3={btc_ret3:+.2f}%")
