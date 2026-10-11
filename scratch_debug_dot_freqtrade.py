import os
os.environ["PYTHONUTF8"] = "1"
import sys
from pathlib import Path

from freqtrade.configuration import Configuration
from freqtrade.resolvers.strategy_resolver import StrategyResolver
from freqtrade.data.history import load_pair_history
from freqtrade.data.dataprovider import DataProvider
from freqtrade.exchange import Exchange

config = Configuration.from_files(['configs/backtest_config.json'])
config['strategy'] = 'NostalgiaForInfinityX8_Combined'
config['timerange'] = '20260811-20261010'

exchange = Exchange(config)
dp = DataProvider(config, exchange)

strategy = StrategyResolver.load_strategy(config)
strategy.dp = dp

# We can directly inspect what Freqtrade backtest does!
print("Strategy and DP initialized successfully!")
