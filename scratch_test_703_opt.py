import pandas as pd
import numpy as np
import talib.abstract as ta
import os
import glob

# Test proposed cond_703 variations on historical 5m data of all 25 active pairs
pairs_files = glob.glob('user_data/data/binance/futures/*-5m-futures.feather')
print(f"Testing on {len(pairs_files)} pair files...")

# Let's inspect how many signals are generated and what happens to them
# We can load the existing backtest trade timestamps
