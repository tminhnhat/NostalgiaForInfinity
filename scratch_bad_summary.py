import zipfile
import json
import glob
import pandas as pd

# Load ohlcv feather data to check indicators at the time of entry
zips = sorted(glob.glob('user_data/backtest_results/*.zip'))
latest_zip = zips[-1]

with zipfile.ZipFile(latest_zip, 'r') as z:
    for name in z.namelist():
        if name.endswith('.json') and not name.endswith('.meta.json'):
            data = json.loads(z.read(name).decode('utf-8'))
            strat = list(data['strategy'].keys())[0]
            trades = data['strategy'][strat]['trades']
            for t in trades:
                if t.get('profit_abs', 0) < -80:
                    pair = t['pair']
                    open_d = t['open_date']
                    tag = t.get('enter_tag')
                    print(f"Bad trade: {pair:16} | Enter: {open_d} | PnL: {t['profit_abs']:.2f} | Tag: {tag}")
