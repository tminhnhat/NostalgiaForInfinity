import pandas as pd

data_path = "user_data/data/binance/futures"
df_btc_1h = pd.read_feather(f"{data_path}/BTC_USDT_USDT-1h-futures.feather")
df_arb_1h = pd.read_feather(f"{data_path}/ARB_USDT_USDT-1h-futures.feather")
df_tia_1h = pd.read_feather(f"{data_path}/TIA_USDT_USDT-1h-futures.feather")

for name, df in [("BTC", df_btc_1h), ("ARB", df_arb_1h), ("TIA", df_tia_1h)]:
    df['date_str'] = df['date'].astype(str)
    sub = df[df['date_str'].str.contains("2026-08-31")]
    print(f"\n=== {name} 1h on 2026-08-31 ===")
    print(sub[['date', 'open', 'high', 'low', 'close', 'volume']])
