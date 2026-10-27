import pandas as pd
import numpy as np

df_btc = pd.read_feather('user_data/data/binance/futures/BTC_USDT_USDT-5m-futures.feather')
df_btc['date'] = pd.to_datetime(df_btc['date'])

sub = df_btc[(df_btc['date'] >= '2026-07-01 11:30:00') & (df_btc['date'] <= '2026-07-01 14:00:00')].copy()
sub['ema21'] = sub['close'].ewm(span=21).mean()
sub['ema50'] = sub['close'].ewm(span=50).mean()
sub['ret_3'] = sub['close'].pct_change(3) * 100
sub['ret_6'] = sub['close'].pct_change(6) * 100

print(sub[['date', 'open', 'close', 'volume', 'ret_3', 'ret_6']].to_string())
