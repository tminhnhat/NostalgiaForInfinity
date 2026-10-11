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
            with_731 = [t for t in trades if '731' in str(t.get('enter_tag', ''))]
            without_731 = [t for t in trades if '731' not in str(t.get('enter_tag', '')) and t.get('is_short', False)]
            
            pnl_with = sum(t.get('profit_abs', 0) for t in with_731)
            w_with = sum(1 for t in with_731 if t.get('profit_abs', 0) > 0)
            
            pnl_without = sum(t.get('profit_abs', 0) for t in without_731)
            w_without = sum(1 for t in without_731 if t.get('profit_abs', 0) > 0)
            
            print(f"WITH 731 (BTC Alignment): Trades: {len(with_731)} | Win: {w_with} | Loss: {len(with_731)-w_with} | Winrate: {w_with/len(with_731)*100:.1f}% | PnL: {pnl_with:.2f} USDT")
            print(f"WITHOUT 731 (Isolated Short): Trades: {len(without_731)} | Win: {w_without} | Loss: {len(without_731)-w_without} | Winrate: {w_without/len(without_731)*100:.1f}% | PnL: {pnl_without:.2f} USDT")
