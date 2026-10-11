import zipfile
import json
import glob

zips = sorted(glob.glob('user_data/backtest_results/*.zip'))
latest_zip = zips[-1]

with zipfile.ZipFile(latest_zip, 'r') as z:
    for name in z.namelist():
        if name.endswith('.json') and not name.endswith('.meta.json'):
            try:
                data = json.loads(z.read(name).decode('utf-8'))
                if 'strategy' in data:
                    strat = list(data['strategy'].keys())[0]
                    trades = data['strategy'][strat]['trades']
                    bad = [t for t in trades if '711' not in t.get('enter_tag', '') and t.get('profit_abs', 0) <= 0]
                    for t in bad:
                        print(f"Pair: {t['pair']:16} | Enter: {t['open_date']} | Exit: {t['close_date']} | PnL: {t['profit_abs']:7.2f} | Tag: {t['enter_tag']} | Exit: {t['exit_reason']}")
            except Exception as e:
                pass
