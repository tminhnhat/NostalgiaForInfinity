import pandas as pd
from freqtrade.configuration import Configuration
from NostalgiaForInfinityX8_Combined import NostalgiaForInfinityX8_Combined

config = Configuration.from_files(['configs/backtest_config.json'])
strat = NostalgiaForInfinityX8_Combined(config)

df = pd.read_feather("user_data/data/binance/futures/ETH_USDT_USDT-5m-futures.feather")
df = strat.populate_indicators(df, {'pair': 'ETH/USDT:USDT'})

print("Total columns:", len(df.columns))
print("Any 4h columns?:", [c for c in df.columns if '4h' in c])
print("Any btc columns?:", [c for c in df.columns if 'btc' in c.lower()])
print("Any roc columns?:", [c for c in df.columns if 'roc' in c.lower()])
print("Any rsi columns?:", [c for c in df.columns if 'rsi' in c.lower()])
print("btc_dumping values:", df['btc_dumping'].value_counts() if 'btc_dumping' in df.columns else "Not in df")
