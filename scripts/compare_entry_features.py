import pandas as pd
import numpy as np
import glob
import zipfile
import json
import os

data_dir = 'user_data/data/binance/futures'

# Lấy 16 trade của tag 702
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

print(f"Found {len(trades_702)} trades for Tag 702.")

# Bây giờ load nến 5m tại thời điểm open_date của từng trade
rows = []
for t in trades_702:
    pair_clean = t['pair'].replace('/', '_').replace(':', '_')
    fpath = os.path.join(data_dir, f"{pair_clean}-5m-futures.feather")
    if not os.path.exists(fpath):
        continue
    df = pd.read_feather(fpath)
    df['date'] = pd.to_datetime(df['date'])
    op_dt = pd.to_datetime(t['open_date'])
    sub = df[df['date'] == op_dt]
    if len(sub) == 0:
        continue
    c = sub.iloc[0]
    
    # Calculate some metrics: volume ratio vs prev 3 candles, rsi, etc.
    idx = sub.index[0]
    prev3_vol = df.loc[max(0, idx-3):idx-1, 'volume'].mean() if idx >= 3 else c['volume']
    vol_ratio = c['volume'] / prev3_vol if prev3_vol > 0 else 1.0
    
    rows.append({
        'pair': t['pair'].split('/')[0],
        'open_date': str(t['open_date'])[:16],
        'profit_ratio': f"{t['profit_ratio']*100:+.2f}%",
        'vol': c['volume'],
        'vol_vs_prev3': f"{vol_ratio:.2f}",
        'close': c['close'],
        'exit_reason': t['exit_reason'].split()[0]
    })

res_df = pd.DataFrame(rows)
print(res_df.to_string())
