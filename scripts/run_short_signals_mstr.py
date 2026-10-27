import pandas as pd
import numpy as np
import talib.abstract as ta

df = pd.read_feather('user_data/data/binance/futures/MSTR_USDT_USDT-5m-futures.feather')
df['date'] = pd.to_datetime(df['date'])

# Load 1h
df_1h = pd.read_feather('user_data/data/binance/futures/MSTR_USDT_USDT-1h-futures.feather')
df_1h['date'] = pd.to_datetime(df_1h['date'])
df_1h['EMA_200_1h'] = ta.EMA(df_1h['close'], timeperiod=200)
df_1h['EMA_50_1h'] = ta.EMA(df_1h['close'], timeperiod=50)
df_1h['RSI_14_1h'] = ta.RSI(df_1h['close'], timeperiod=14)

# Load BTC 4h
df_btc_4h = pd.read_feather('user_data/data/binance/futures/BTC_USDT_USDT-4h-futures.feather')
df_btc_4h['date'] = pd.to_datetime(df_btc_4h['date'])
df_btc_4h['ROC_9_4h'] = ta.ROC(df_btc_4h['close'], timeperiod=9)

# Merge
df = pd.merge_asof(df.sort_values('date'), df_1h[['date', 'EMA_200_1h', 'EMA_50_1h', 'RSI_14_1h']].sort_values('date'), on='date')
df = pd.merge_asof(df.sort_values('date'), df_btc_4h[['date', 'ROC_9_4h']].sort_values('date'), on='date')

import sys
sys.path.append('.')
sys.path.append('user_data/strategies')
from NostalgiaForInfinityX8_ShortSignals import NostalgiaForInfinityX8_ShortSignals

s = NostalgiaForInfinityX8_ShortSignals()
df = s.populate_indicators(df, {'pair': 'MSTR/USDT:USDT'})
df = s.populate_entry_trend(df, {'pair': 'MSTR/USDT:USDT'})

target_row = df[df['date'] == '2026-07-01 12:35:00+00:00']
print("Target row at 12:35:")
if len(target_row) > 0:
    r = target_row.iloc[0]
    print("enter_short_custom:", r.get('enter_short_custom'))
    print("enter_tag_custom:", repr(r.get('enter_tag_custom')))
    print("stochrsi_k_custom:", r.get('stochrsi_k_custom'))
