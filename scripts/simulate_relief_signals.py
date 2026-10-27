import pandas as pd
import numpy as np
import os
import json

# Check signals for trigger_relief_rejection
with open('configs/backtest_config.json', 'r') as f:
    cfg = json.load(f)
pair_list = cfg.get('exchange', {}).get('pair_whitelist', [])

data_dir = 'user_data/data/binance/futures'
print(f"Testing on {len(pair_list)} pairs...")
