import pandas as pd
import numpy as np

# Load feather of MSTR and STRK
df_mstr = pd.read_feather('user_data/data/binance/futures/MSTR_USDT_USDT-5m-futures.feather')
df_mstr['date'] = pd.to_datetime(df_mstr['date'])
r_mstr = df_mstr[df_mstr['date'] == '2026-07-01 12:35:00+00:00']
print("MSTR at 12:35 cols:", [c for c in df_mstr.columns if 'prob' in c or 'ai_' in c])
