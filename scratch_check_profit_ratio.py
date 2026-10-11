import zipfile
import json
import glob

zips = sorted(glob.glob('user_data/backtest_results/*.zip'))
latest_zip = zips[-1]

with zipfile.ZipFile(latest_zip, 'r') as z:
    for name in z.namelist():
        if name.endswith('.json') and not name.endswith('.meta.json'):
            data = json.loads(z.read(name).decode('utf-8'))
            strat = list(data['strategy'].keys())[0]
            trades = data['strategy'][strat]['trades']
            for t in trades[:5]:
                print(f"Pair: {t['pair']} | profit_ratio: {t['profit_ratio']} | profit_pct: {t['profit_ratio']*100:.2f}% | profit_abs: {t['profit_abs']} | stake: {t['stake_amount']} | lev: {t.get('leverage')}")
