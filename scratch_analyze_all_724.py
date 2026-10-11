import pandas as pd
import numpy as np
import talib.abstract as ta

trades_724 = [
    {"pair": "OP/USDT:USDT", "open_date": "2026-08-15 15:00:00+00:00", "pnl": 8.42},
    {"pair": "DOT/USDT:USDT", "open_date": "2026-08-28 21:05:00+00:00", "pnl": 17.74},
    {"pair": "ARB/USDT:USDT", "open_date": "2026-08-31 04:50:00+00:00", "pnl": -92.31},
    {"pair": "INJ/USDT:USDT", "open_date": "2026-09-01 12:20:00+00:00", "pnl": 1.28},
    {"pair": "TIA/USDT:USDT", "open_date": "2026-08-31 04:50:00+00:00", "pnl": -91.52},
    {"pair": "BNB/USDT:USDT", "open_date": "2026-09-07 11:30:00+00:00", "pnl": 21.27},
    {"pair": "ARB/USDT:USDT", "open_date": "2026-09-12 03:10:00+00:00", "pnl": 22.62},
]

data_path = "user_data/data/binance/futures"

for t in trades_724:
    sym = t['pair'].split('/')[0]
    df_5m = pd.read_feather(f"{data_path}/{sym}_USDT_USDT-5m-futures.feather")
    df_1h = pd.read_feather(f"{data_path}/{sym}_USDT_USDT-1h-futures.feather")
    df_btc_1h = pd.read_feather(f"{data_path}/BTC_USDT_USDT-1h-futures.feather")
    
    # Calculate 5m indicators
    c = df_5m['close'].to_numpy()
    h = df_5m['high'].to_numpy()
    l = df_5m['low'].to_numpy()
    o = df_5m['open'].to_numpy()
    v = df_5m['volume'].to_numpy()
    
    df_5m['ema_50'] = ta.EMA(c, timeperiod=50)
    df_5m['ema_200'] = ta.EMA(c, timeperiod=200)
    df_5m['ema_21'] = ta.EMA(c, timeperiod=21)
    df_5m['rsi_14'] = ta.RSI(c, timeperiod=14)
    df_5m['upper_wick_ratio'] = (h - np.maximum(c, o)) / np.where(h - l == 0, 1e-9, h - l)
    
    # 1h indicators
    c_1h = df_1h['close'].to_numpy()
    df_1h['rsi_1h'] = ta.RSI(c_1h, timeperiod=14)
    df_1h['ema_21_1h'] = ta.EMA(c_1h, timeperiod=21)
    df_1h['ema_50_1h'] = ta.EMA(c_1h, timeperiod=50)
    df_1h['ema_200_1h'] = ta.EMA(c_1h, timeperiod=200)
    
    # BTC 1h
    c_btc = df_btc_1h['close'].to_numpy()
    df_btc_1h['btc_rsi_1h'] = ta.RSI(c_btc, timeperiod=14)
    df_btc_1h['btc_ema_21_1h'] = ta.EMA(c_btc, timeperiod=21)
    
    # Find entry candle (candle immediately before open_date)
    dt_target = pd.to_datetime(t['open_date'])
    sub_5m = df_5m[df_5m['date'] < dt_target]
    last_5m = sub_5m.iloc[-1]
    
    sub_1h = df_1h[df_1h['date'] <= dt_target]
    last_1h = sub_1h.iloc[-1]
    
    sub_btc = df_btc_1h[df_btc_1h['date'] <= dt_target]
    last_btc = sub_btc.iloc[-1]
    
    print(f"\n==================================================")
    print(f"{t['pair']} | PnL: {t['pnl']} USDT | Entry Time: {t['open_date']}")
    print(f"5m candle: close={last_5m['close']}, EMA50={last_5m['ema_50']:.4f}, EMA200={last_5m['ema_200']:.4f}")
    print(f"5m RSI: {last_5m['rsi_14']:.2f}, WickRatio: {last_5m['upper_wick_ratio']:.2f}")
    print(f"1h RSI: {last_1h['rsi_1h']:.2f}, 1h close={last_1h['close']}, 1h EMA50={last_1h['ema_50_1h']:.4f}, 1h EMA200={last_1h['ema_200_1h']:.4f}")
    print(f"1h Trend (close < EMA50_1h): {last_1h['close'] < last_1h['ema_50_1h']}")
    print(f"1h Trend (EMA50_1h < EMA200_1h): {last_1h['ema_50_1h'] < last_1h['ema_200_1h']}")
    print(f"BTC 1h RSI: {last_btc['btc_rsi_1h']:.2f}, BTC 1h close > EMA21: {last_btc['close'] > last_btc['btc_ema_21_1h']}")
