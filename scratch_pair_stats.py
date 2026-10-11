import json
import zipfile
import glob
import os

zip_files = glob.glob('user_data/backtest_results/backtest-result-*.zip')
zip_files.sort(key=os.path.getmtime, reverse=True)
latest_zip = zip_files[0]

with zipfile.ZipFile(latest_zip) as z:
    for name in z.namelist():
        if name.endswith('.json') and not name.endswith('.meta.json') and not name.endswith('_config.json'):
            with z.open(name) as f:
                data = json.load(f)
                trades = data['strategy']['NostalgiaForInfinityX8_Combined']['trades']
                pair_stats = {}
                for t in trades:
                    pair = t['pair']
                    if pair not in pair_stats:
                        pair_stats[pair] = {'trades': 0, 'wins': 0, 'losses': 0, 'pnl': 0.0}
                    pair_stats[pair]['trades'] += 1
                    if t['profit_abs'] > 0:
                        pair_stats[pair]['wins'] += 1
                    else:
                        pair_stats[pair]['losses'] += 1
                    pair_stats[pair]['pnl'] += t['profit_abs']
                    
                print("\n=== PERFORMANCE BY PAIR ===")
                print(f"{'Pair':<20} | {'Trades':<7} | {'Wins':<5} | {'Losses':<7} | {'Winrate':<8} | {'PnL (USDT)':<10}")
                print("-" * 65)
                for pair, s in sorted(pair_stats.items(), key=lambda x: x[1]['pnl'], reverse=True):
                    wr = s['wins'] / s['trades'] * 100 if s['trades'] > 0 else 0
                    print(f"{pair:<20} | {s['trades']:<7} | {s['wins']:<5} | {s['losses']:<7} | {wr:<7.1f}% | {s['pnl']:<10.2f}")
