import pandas as pd
import pandas_ta as pta
from pathlib import Path
import csv

def main():
    with open('reports/latest_trades.csv', mode='r', encoding='utf-8') as f:
        trades = [r for r in csv.DictReader(f) if '702 703 731_AI_PASS' == r['enter_tag'].strip()]

    print(f"Inspecting RSI_14 at entry for {len(trades)} trades:")
    for t in trades:
        pair = t['pair']
        open_d = t['open_date']
        feather_path = Path(f"user_data/data/binance/futures/{pair}_USDT_USDT-5m-futures.feather")
        if feather_path.exists():
            df = pd.read_feather(feather_path)
            df['rsi_14'] = pta.rsi(df['close'], length=14)
            df['vol_ma20'] = df['volume'].rolling(20).mean()
            df['vol_ratio'] = df['volume'] / df['vol_ma20']
            matches = df[df['date'] == f"{open_d}:00+00:00"]
            if len(matches) > 0:
                row = matches.iloc[0]
                rsi = row['rsi_14']
                vol_r = row['vol_ratio']
                print(f"{pair:<8} | Open: {open_d} | RSI_14: {rsi:5.2f} | Vol Ratio: {vol_r:5.2f} | ROE: {t['profit_pct']:>6}%")

if __name__ == '__main__':
    main()
