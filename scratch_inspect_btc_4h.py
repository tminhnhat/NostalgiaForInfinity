import pandas as pd
import talib.abstract as ta

data_path = "user_data/data/binance/futures"
df_btc_4h = pd.read_feather(f"{data_path}/BTC_USDT_USDT-4h-futures.feather")
df_btc_4h['date_str'] = df_btc_4h['date'].astype(str)
df_btc_4h['ROC_9'] = ta.ROC(df_btc_4h, timeperiod=9)
df_btc_4h['RSI_14'] = ta.RSI(df_btc_4h, timeperiod=14)

sub_btc = df_btc_4h[df_btc_4h['date_str'].str.contains("2026-08-30|2026-08-31")]
print("BTC 4h on 2026-08-30 and 2026-08-31:")
print(sub_btc[['date', 'open', 'high', 'low', 'close', 'ROC_9', 'RSI_14']])
