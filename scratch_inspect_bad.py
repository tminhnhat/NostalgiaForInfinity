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
                    bad_trades = [t for t in trades if t.get('enter_tag') in ['712 713', '712'] and t.get('profit_abs', 0) < 0]
                    print(f"Total bad 712 trades: {len(bad_trades)}")
                    for t in bad_trades[:8]:
                        print(f"Pair: {t['pair']} | Enter: {t['open_date']} | Exit: {t['close_date']} | Profit%: {t['profit_ratio']*100:.2f}% | PnL: {t['profit_abs']:.2f} | Tag: {t['enter_tag']} | Exit reason: {t['exit_reason']}")
            except Exception as e:
                pass
