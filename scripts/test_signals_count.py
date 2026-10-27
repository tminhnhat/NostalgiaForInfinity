import pandas as pd
import numpy as np
import os
import talib.abstract as ta
import sys
sys.path.append('.')
sys.path.append('user_data/strategies')

from NostalgiaForInfinityX8_ShortSignals import NostalgiaForInfinityX8_ShortSignals

strat = NostalgiaForInfinityX8_ShortSignals()
data_dir = 'user_data/data/binance/futures'

# Lấy danh sách pair trong pair_whitelist từ config
import json
with open('configs/backtest_config.json', 'r') as f:
    cfg = json.load(f)
pair_list = cfg.get('exchange', {}).get('pair_whitelist', [])

print(f"Analyzing {len(pair_list)} pairs from whitelist...")

# Test running populate_indicators and entry_trend on 5 pairs
results = []
for p in pair_list[:5]:
    pair_clean = p.replace('/', '_').replace(':', '_')
    fpath = os.path.join(data_dir, f"{pair_clean}-5m-futures.feather")
    if not os.path.exists(fpath):
        continue
    df = pd.read_feather(fpath)
    df['date'] = pd.to_datetime(df['date'])
    df = strat.populate_indicators(df, {'pair': p})
    df = strat.populate_entry_trend(df, {'pair': p})
    
    c_entries = df[df['enter_short_custom'] == 1]
    tags = c_entries['enter_tag_custom'].value_counts()
    print(f"\nPair {p}: {len(c_entries)} short entries")
    for t, cnt in tags.items():
        print(f"  Tag '{t}': {cnt}")
