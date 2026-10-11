import json
import zipfile
import glob
import os

zip_files = glob.glob('user_data/backtest_results/backtest-result-*.zip')
zip_files.sort(key=os.path.getmtime, reverse=True)
latest_zip = zip_files[0]
print(f"Reading: {latest_zip}")

with zipfile.ZipFile(latest_zip) as z:
    for name in z.namelist():
        if name.endswith('.json') and not name.endswith('.meta.json') and not name.endswith('_config.json'):
            with z.open(name) as f:
                data = json.load(f)
                trades = data['strategy']['NostalgiaForInfinityX8_Combined']['trades']
                
                # Tag stats
                tag_stats = {}
                for t in trades:
                    tags = str(t.get('enter_tag', '')).strip().split()
                    for tag in tags:
                        if tag not in tag_stats:
                            tag_stats[tag] = {'trades': 0, 'wins': 0, 'losses': 0, 'profit': 0.0}
                        tag_stats[tag]['trades'] += 1
                        if t['profit_abs'] > 0:
                            tag_stats[tag]['wins'] += 1
                        else:
                            tag_stats[tag]['losses'] += 1
                        tag_stats[tag]['profit'] += t['profit_abs']
                
                print("\n=== TAG PERFORMANCE SUMMARY ===")
                print(f"{'Tag':<10} | {'Trades':<7} | {'Wins':<5} | {'Losses':<7} | {'Winrate':<8} | {'PnL (USDT)':<10}")
                print("-" * 60)
                for tag, s in sorted(tag_stats.items(), key=lambda x: x[1]['profit'], reverse=True):
                    wr = (s['wins'] / s['trades']) * 100 if s['trades'] > 0 else 0
                    print(f"{tag:<10} | {s['trades']:<7} | {s['wins']:<5} | {s['losses']:<7} | {wr:<7.1f}% | {s['profit']:<10.2f}")
