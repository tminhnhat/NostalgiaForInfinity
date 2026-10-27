import pandas as pd
import numpy as np

# Let's inspect which conditions are True for MSTR at 12:35
import sys
sys.path.append('.')
sys.path.append('user_data/strategies')
from NostalgiaForInfinityX8_ShortSignals import NostalgiaForInfinityX8_ShortSignals

strat = NostalgiaForInfinityX8_ShortSignals()
df = pd.read_feather('user_data/data/binance/futures/MSTR_USDT_USDT-5m-futures.feather')
df_btc = pd.read_feather('user_data/data/binance/futures/BTC_USDT_USDT-5m-futures.feather')

# We can run populate_indicators and entry_trend if possible, or just evaluate
print("ShortSignals loaded.")
