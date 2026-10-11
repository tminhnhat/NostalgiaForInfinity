import pandas as pd
import numpy as np
from NostalgiaForInfinityX8_ShortSignals import NostalgiaForInfinityX8_ShortSignals

data_path = "user_data/data/binance/futures"
df_dot = pd.read_feather(f"{data_path}/DOT_USDT_USDT-5m-futures.feather")

engine = NostalgiaForInfinityX8_ShortSignals()
df_dot = engine.populate_indicators(df_dot, {'pair': 'DOT/USDT:USDT'})
df_dot = engine.populate_entry_trend(df_dot, {'pair': 'DOT/USDT:USDT'})

row = df_dot[df_dot['date'].astype(str).str.contains("2026-08-31 13:15")]
if len(row) > 0:
    idx = row.index[0]
    print(f"enter_short: {df_dot.loc[idx, 'enter_short_custom']}")
    print(f"enter_tag: {df_dot.loc[idx, 'enter_tag_custom']}")
