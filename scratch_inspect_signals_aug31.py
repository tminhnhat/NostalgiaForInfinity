import sys
import pandas as pd
import numpy as np

data_path = "user_data/data/binance/futures"
df_arb = pd.read_feather(f"{data_path}/ARB_USDT_USDT-5m-futures.feather")
df_tia = pd.read_feather(f"{data_path}/TIA_USDT_USDT-5m-futures.feather")

# Add talib RSI_14 and informative if missing
import talib.abstract as ta
for df in [df_arb, df_tia]:
    df['RSI_14'] = ta.RSI(df, timeperiod=14)

from NostalgiaForInfinityX8_ShortSignals import NostalgiaForInfinityX8_ShortSignals
signals = NostalgiaForInfinityX8_ShortSignals()

for pair_name, df in [("ARB", df_arb), ("TIA", df_tia)]:
    df = signals.populate_indicators(df, {'pair': f'{pair_name}/USDT:USDT'})
    df = signals.populate_entry_trend(df, {'pair': f'{pair_name}/USDT:USDT'})
    
    df['date_str'] = df['date'].astype(str)
    row = df[df['date_str'].str.contains("2026-08-31 04:45|2026-08-31 04:50")]
    print(f"\n=================== {pair_name} ===================")
    for idx, r in row.iterrows():
        print(f"Date: {r['date']} | close: {r['close']} | open: {r['open']} | high: {r['high']} | low: {r['low']}")
        print(f"EMA9: {r['EMA_9']:.5f} | EMA21: {r['EMA_21']:.5f} | EMA50: {r['EMA_50']:.5f} | EMA200: {r['EMA_200']:.5f}")
        print(f"RSI: {r['RSI_14']:.2f} | WickRatio: {r['upper_wick_ratio']:.2f} | VolSpike: {r['vol_spike_ratio']:.2f}")
        print(f"enter_short: {r.get('enter_short')} | enter_tag_custom: {r.get('enter_tag_custom')}")
        print(f"high >= EMA50 * 0.998: {r['high'] >= r['EMA_50'] * 0.998}")
        print(f"close < EMA50: {r['close'] < r['EMA_50']}")
        print(f"close < open: {r['close'] < r['open']}")
        print(f"EMA50 < EMA200: {r['EMA_50'] < r['EMA_200']}")
