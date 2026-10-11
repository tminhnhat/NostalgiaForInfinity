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
                    non_711_trades = [t for t in trades if '711' not in t.get('enter_tag', '')]
                    total_pnl = sum(t.get('profit_abs', 0) for t in non_711_trades)
                    wins = [t for t in non_711_trades if t.get('profit_abs', 0) > 0]
                    losses = [t for t in non_711_trades if t.get('profit_abs', 0) <= 0]
                    print(f"Non-711 Trades: {len(non_711_trades)}")
                    print(f"Wins: {len(wins)}, Losses: {len(losses)}, Winrate: {len(wins)/len(non_711_trades)*100:.1f}%")
                    print(f"Total PnL without 711: {total_pnl:.2f} USDT")
            except Exception as e:
                pass
