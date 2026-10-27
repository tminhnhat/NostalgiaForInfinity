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

df_btc_1h = pd.read_feather(os.path.join(data_dir, "BTC_USDT_USDT-1h-futures.feather"))
df_btc_1h['date'] = pd.to_datetime(df_btc_1h['date'])
df_btc_1h['btc_rsi_1h'] = ta.RSI(df_btc_1h['close'].to_numpy(), timeperiod=14)

print("Checking BTC 1H RSI for all 16 trades:")
for t in trades_702:
    op_dt = pd.to_datetime(t['open_date'])
    sub_b = df_btc_1h[df_btc_1h['date'] <= op_dt]
    r = sub_b.iloc[-1]
    print(f"{t['pair'].split('/')[0]:<5} | date={str(op_dt)[:16]} | ROE={t['profit_ratio']*100:+.2f}% | BTC_1h_RSI={r['btc_rsi_1h']:.2f}")
