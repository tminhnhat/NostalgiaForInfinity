import pandas as pd

# Let's inspect columns created by NostalgiaForInfinityX8 base strategy on 5m
data_path = "user_data/data/binance/futures"
df_arb = pd.read_feather(f"{data_path}/ARB_USDT_USDT-5m-futures.feather")

from NostalgiaForInfinityX8 import NostalgiaForInfinityX8
nfix8 = NostalgiaForInfinityX8(config={
    "exchange": {"name": "binance", "pair_whitelist": ["ARB/USDT:USDT", "BTC/USDT:USDT"]},
    "stake_currency": "USDT",
    "trading_mode": "futures",
    "margin_mode": "isolated"
})

# Let's see what informative indicators NFIX8 computes for BTC
for pair in ["BTC/USDT:USDT", "BTC/USDT"]:
    print("Informative for BTC in nfix8:")
    break
