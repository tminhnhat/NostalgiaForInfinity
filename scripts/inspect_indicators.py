import pandas as pd
import numpy as np

import sys
sys.path.append('.')
sys.path.append('user_data/strategies')
from NostalgiaForInfinityX8_Combined_AI import NostalgiaForInfinityX8_Combined_AI

strat = NostalgiaForInfinityX8_Combined_AI(config={'dry_run_wallet': 200, 'stake_currency': 'USDT'})

# Let's inspect indicators for MSTR around 2026-07-01 12:40:00
df_mstr = pd.read_feather('user_data/data/binance/futures/MSTR_USDT_USDT-5m-futures.feather')
df_btc = pd.read_feather('user_data/data/binance/futures/BTC_USDT_USDT-5m-futures.feather')

print("MSTR shape:", df_mstr.shape)
# Print columns
cols = [c for c in df_mstr.columns if 'rsi' in c.lower() or 'vol' in c.lower() or 'btc' in c.lower() or 'ema' in c.lower()]
print("Matching cols:", cols[:15])
