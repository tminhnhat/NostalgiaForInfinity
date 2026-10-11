import pandas as pd

# Load 5m and 1h data for ARB, TIA, BTC
data_path = "user_data/data/binance/futures"
df_btc_5m = pd.read_feather(f"{data_path}/BTC_USDT_USDT-5m-futures.feather")
df_arb_5m = pd.read_feather(f"{data_path}/ARB_USDT_USDT-5m-futures.feather")
df_tia_5m = pd.read_feather(f"{data_path}/TIA_USDT_USDT-5m-futures.feather")

df_btc_1h = pd.read_feather(f"{data_path}/BTC_USDT_USDT-1h-futures.feather")
df_arb_1h = pd.read_feather(f"{data_path}/ARB_USDT_USDT-1h-futures.feather")
df_tia_1h = pd.read_feather(f"{data_path}/TIA_USDT_USDT-1h-futures.feather")

print("BTC 5m date dtype:", df_btc_5m['date'].dtype)

# Convert to UTC string or compare
target_time = "2026-08-31 04:50:00"

for name, df in [("BTC 5m", df_btc_5m), ("ARB 5m", df_arb_5m), ("TIA 5m", df_tia_5m)]:
    df['date_str'] = df['date'].astype(str)
    row = df[df['date_str'].str.contains("2026-08-31 04:50")]
    if not row.empty:
        idx = row.index[0]
        sub = df.loc[idx-5:idx+5, ['date', 'open', 'high', 'low', 'close', 'volume']]
        print(f"\n--- {name} around 04:50 ---")
        print(sub)

for name, df in [("BTC 1h", df_btc_1h), ("ARB 1h", df_arb_1h), ("TIA 1h", df_tia_1h)]:
    df['date_str'] = df['date'].astype(str)
    row = df[df['date_str'].str.contains("2026-08-31 04:00")]
    if not row.empty:
        idx = row.index[0]
        sub = df.loc[idx-3:idx+3, ['date', 'open', 'high', 'low', 'close', 'volume']]
        print(f"\n--- {name} around 04:00 ---")
        print(sub)
