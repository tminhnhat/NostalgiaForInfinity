import pandas as pd
import numpy as np
import talib.abstract as ta

data_path = "user_data/data/binance/futures"
df_dot = pd.read_feather(f"{data_path}/DOT_USDT_USDT-5m-futures.feather")

c = df_dot['close'].to_numpy()
h = df_dot['high'].to_numpy()
l = df_dot['low'].to_numpy()
o = df_dot['open'].to_numpy()
v = df_dot['volume'].to_numpy()

ema_9 = ta.EMA(c, timeperiod=9)
ema_21 = ta.EMA(c, timeperiod=21)
ema_50 = ta.EMA(c, timeperiod=50)
ema_200 = ta.EMA(c, timeperiod=200)
rsi_14 = ta.RSI(c, timeperiod=14)
macd, macdsignal, macdhist = ta.MACD(c, fastperiod=12, slowperiod=26, signalperiod=9)

vol_sma_20 = ta.SMA(v, timeperiod=20)
vol_spike_ratio = v / np.where(vol_sma_20 == 0, 1e-9, vol_sma_20)

hl_range = h - l
upper_wick_ratio = (h - np.maximum(c, o)) / np.where(hl_range == 0, 1e-9, hl_range)

df_dot['date_str'] = df_dot['date'].astype(str)
row = df_dot[df_dot['date_str'].str.contains("2026-08-31 13:15")]
idx = row.index[0]

shift_ema_9 = ema_9[idx-1]
shift_ema_21 = ema_21[idx-1]
ribbon_spread = (ema_21[idx] - ema_9[idx]) / ema_21[idx]

prev_candle_green = c[idx-1] > o[idx-1]

cond_721 = (
    (v[idx] > 0)
    & (ema_50[idx] < ema_200[idx])
    & prev_candle_green
    & (h[idx] >= ema_21[idx] * 0.998)
    & (c[idx] < ema_21[idx])
    & (c[idx] < o[idx])
    & (upper_wick_ratio[idx] >= 0.40)
    & (vol_spike_ratio[idx] >= 1.20)
    & (rsi_14[idx] >= 42.0) & (rsi_14[idx] <= 58.0)
)

cond_703 = (
    (v[idx] > 0)
    & (ema_9[idx] < ema_21[idx])
    & (ema_21[idx] < ema_50[idx])
    & (ema_50[idx] < ema_200[idx])
    & (ema_9[idx] < shift_ema_9)
    & (ema_21[idx] < shift_ema_21)
    & (ribbon_spread >= 0.0006)
    & (c[idx] < ema_9[idx])
    & (c[idx] < o[idx])
    & (vol_spike_ratio[idx] >= 1.25)
    & (rsi_14[idx] > 30.0) & (rsi_14[idx] < 46.0)
)

retest_confirmed = (h[idx] >= ema_9[idx] * 0.997) & (c[idx] < ema_9[idx])

# Check MACD cond_702
shift_macdhist = macdhist[idx-1]
cond_702 = (
    (v[idx] > 0)
    & (ema_50[idx] < ema_200[idx])
    & (macd[idx] < 0) & (macdhist[idx] < 0)
    & (macdhist[idx] < shift_macdhist)
    & (c[idx] < ema_21[idx]) & (c[idx] < ema_50[idx])
    & (c[idx] < o[idx])
    & (vol_spike_ratio[idx] >= 1.20)
    & (rsi_14[idx] > 28.0) & (rsi_14[idx] < 48.0)
)

print(f"DOT at 13:15:")
print(f"cond_721: {cond_721}")
print(f"cond_703: {cond_703}")
print(f"cond_702: {cond_702}")
print(f"retest_confirmed: {retest_confirmed}")

# Check Setups
print(f"Setup 2 (trigger_breakdown): cond_703 & (cond_702 | cond_701) & retest_confirmed = {cond_703 & cond_702 & retest_confirmed}")
print(f"Setup 3 (trigger_rejection): cond_721 & (cond_703 | cond_702) = {cond_721 & (cond_703 | cond_702)}")
