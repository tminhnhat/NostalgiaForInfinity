import pandas as pd
import pandas_ta as pta

def main():
    df = pd.read_feather('user_data/data/binance/futures/MSTR_USDT_USDT-5m-futures.feather')
    df['rsi_14'] = pta.rsi(df['close'], length=14)
    idx = df[df['date'] == '2026-07-01 12:40:00+00:00'].index[0]
    print("MSTR rsi_14 at 12:40:", df.loc[idx, 'rsi_14'])
    print("MSTR rsi_14 at 12:35:", df.loc[idx-1, 'rsi_14'])
    print("MSTR rsi_14 at 12:30:", df.loc[idx-2, 'rsi_14'])

if __name__ == '__main__':
    main()
