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
                    sfp_trades = [t for t in trades if '711' in t.get('enter_tag', '')]
                    print(f"Total 711 trades: {len(sfp_trades)}")
                    for t in sfp_trades:
                        print(f"Pair: {t['pair']:16} | Enter: {t['open_date']} | Exit: {t['close_date']} | Profit%: {t['profit_ratio']*100:6.2f}% | PnL: {t['profit_abs']:7.2f} | Tag: {t['enter_tag']} | Exit: {t['exit_reason']}")
            except Exception as e:
                pass
