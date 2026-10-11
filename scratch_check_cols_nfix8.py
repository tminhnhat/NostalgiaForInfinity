import pandas as pd
import json

with open("user_data/nfix8-profit_max-binance-USDT-(backtest).json") as f:
    config = json.load(f)

# Mock exchange config if needed
if "exchange" not in config:
    config["exchange"] = {"name": "binance", "pair_whitelist": ["ARB/USDT:USDT", "BTC/USDT:USDT"]}

from NostalgiaForInfinityX8 import NostalgiaForInfinityX8
nfix8 = NostalgiaForInfinityX8(config=config)

data_path = "user_data/data/binance/futures"
df_arb = pd.read_feather(f"{data_path}/ARB_USDT_USDT-5m-futures.feather")

df_arb = nfix8.populate_indicators(df_arb, {'pair': 'ARB/USDT:USDT'})
cols_1h = [c for c in df_arb.columns if '1h' in c]
print(f"Total columns: {len(df_arb.columns)}")
print("1h columns:", cols_1h[:20])
cols_btc = [c for c in df_arb.columns if 'btc' in c.lower()]
print("BTC columns:", cols_btc)
