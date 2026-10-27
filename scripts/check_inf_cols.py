import pandas as pd
import glob
import zipfile
import json

# Let's inspect column names in dataframe during backtest
# In Freqtrade Nostalgia informative timeframe is 1h and 4h
# Usually columns are: 'rsi_14_1h' or 'rsi_1h' or 'RSI_14_1h' or 'btc_rsi_14_1h'
# Let's check user_data/strategies/NostalgiaForInfinityX8_Combined_AI.py informative_pairs
