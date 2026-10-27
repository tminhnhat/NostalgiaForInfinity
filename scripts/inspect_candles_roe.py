import pandas as pd
from pathlib import Path

def main():
    for pair in ['PUMP', 'ZRO', 'TAO', 'PYTH']:
        p = Path(f'user_data/data/binance/futures/{pair}_USDT_USDT-5m-futures.feather')
        if p.exists():
            df = pd.read_feather(p)
            print(f"=== {pair} ===")
            if pair == 'PUMP':
                sub = df[(df['date'] >= '2026-05-27 04:15') & (df['date'] <= '2026-05-27 04:40')]
            elif pair == 'ZRO':
                sub = df[(df['date'] >= '2026-06-02 01:30') & (df['date'] <= '2026-06-02 02:35')]
            elif pair == 'TAO':
                sub = df[(df['date'] >= '2026-06-02 07:55') & (df['date'] <= '2026-06-02 10:20')]
            elif pair == 'PYTH':
                sub = df[(df['date'] >= '2026-06-02 12:15') & (df['date'] <= '2026-06-02 14:30')]
            open_px = sub.iloc[1]['open']
            for idx, r in sub.iterrows():
                # For short: roe at close, roe at low
                roe_close = (open_px - r['close']) / open_px * 500
                roe_max = (open_px - r['low']) / open_px * 500
                print(f"{r['date']} | C: {r['close']} | L: {r['low']} | ROE Close: {roe_close:+5.2f}% | ROE Low: {roe_max:+5.2f}%")

if __name__ == '__main__':
    main()
