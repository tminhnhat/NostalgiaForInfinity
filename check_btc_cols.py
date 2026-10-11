import glob
import pandas as pd

# check columns in one feather file
df = pd.read_feather("user_data/data/binance/futures/BTC_USDT_USDT-5m-futures.feather")
print("Base columns:", df.columns.tolist()[:10])

# check if informative 4h exists
f4h = glob.glob("user_data/data/binance/futures/BTC_USDT_USDT-4h-futures.feather")
print("4h feather exists:", bool(f4h))
