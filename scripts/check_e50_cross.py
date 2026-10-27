import pandas as pd
import numpy as np
from pathlib import Path
import csv

def main():
    with open('reports/latest_trades.csv', mode='r', encoding='utf-8') as f:
        trades = [r for r in csv.DictReader(f) if '702 703 731_AI_PASS' == r['enter_tag'].strip()]

    print("Checking whether trades crossed above 1H EMA 50 during trade:")
    for t in trades:
        pair = t['pair']
        open_d = t['open_date']
        close_d = t['close_date']
        p_pct = float(t['profit_pct'])
        
        f5 = Path(f"user_data/data/binance/futures/{pair}_USDT_USDT-5m-futures.feather")
        f15 = Path(f"user_data/data/binance/futures/{pair}_USDT_USDT-15m-futures.feather")
        if f5.exists() and f15.exists():
            df5 = pd.read_feather(f5)
            df15 = pd.read_feather(f15)
            # 1h EMA50 is approx 48 on 15m or 120 on 5m
            df5['e50_1h'] = df5['close'].ewm(span=600).mean() # 50 hours = 600 5m bars
            # actual 1h EMA50 is 50 hours = 50 * 12 = 600 bars on 5m
            sub = df5[(df5['date'] >= f"{open_d}:00+00:00") & (df5['date'] <= f"{close_d}:00+00:00")]
            if len(sub) > 0:
                open_px = sub.iloc[0]['open']
                sub['profit_roe'] = (open_px - sub['close']) / open_px * 5.0
                sub['above_e50'] = sub['close'] > sub['e50_1h']
                bad_sub = sub[sub['above_e50'] & (sub['profit_roe'] <= -0.06)]
                print(f"{pair:<8} | PnL: {p_pct:>+6.2f}% | Bad bars: {len(bad_sub)}")

if __name__ == '__main__':
    main()
