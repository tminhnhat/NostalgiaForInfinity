import pandas as pd
import talib.abstract as ta

df_btc = pd.read_feather("user_data/data/binance/futures/BTC_USDT_USDT-5m-futures.feather")
df_btc['date'] = pd.to_datetime(df_btc['date'], utc=True)

df_btc_1h = pd.read_feather("user_data/data/binance/futures/BTC_USDT_USDT-1h-futures.feather")
df_btc_1h['date'] = pd.to_datetime(df_btc_1h['date'], utc=True)
df_btc_1h['ema50'] = ta.EMA(df_btc_1h['close'].to_numpy(), timeperiod=50)
df_btc_1h['ema200'] = ta.EMA(df_btc_1h['close'].to_numpy(), timeperiod=200)
df_btc_1h['rsi14'] = ta.RSI(df_btc_1h['close'].to_numpy(), timeperiod=14)

check_times = [
    '2026-09-15 21:05:00+00:00',
    '2026-09-16 04:20:00+00:00',
    '2026-09-16 12:25:00+00:00',
    '2026-09-16 19:45:00+00:00',
    '2026-10-03 04:05:00+00:00'
]

for t_str in check_times:
    t = pd.to_datetime(t_str)
    # find latest 1h candle before t
    sub_1h = df_btc_1h[df_btc_1h['date'] <= t]
    if len(sub_1h) > 0:
        last_1h = sub_1h.iloc[-1]
        print(f"BTC at {t_str}: 1h close={last_1h['close']:.1f}, 1h EMA50={last_1h['ema50']:.1f}, 1h EMA200={last_1h['ema200']:.1f}, 1h RSI={last_1h['rsi14']:.1f}, Above EMA200={last_1h['close'] > last_1h['ema200']}")
