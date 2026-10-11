import json
import zipfile
import glob
import os

zip_files = glob.glob('user_data/backtest_results/backtest-result-*.zip')
zip_files.sort(key=os.path.getmtime, reverse=True)
latest_zip = zip_files[0]
prev_zip = zip_files[1]
print(f"Comparing New ({latest_zip}) vs Prev ({prev_zip})")

def get_trades(zpath):
    with zipfile.ZipFile(zpath) as z:
        for n in z.namelist():
            if n.endswith('.json') and not n.endswith('.meta.json') and not n.endswith('_config.json'):
                with z.open(n) as f:
                    return json.load(f)['strategy']['NostalgiaForInfinityX8_Combined']['trades']

t_new = get_trades(latest_zip)
t_prev = get_trades(prev_zip)

print(f"New total trades: {len(t_new)} | Prev total trades: {len(t_prev)}")

# Find new trades not in prev
prev_keys = set((t['pair'], t['open_date']) for t in t_prev)
new_trades_added = [t for t in t_new if (t['pair'], t['open_date']) not in prev_keys]

print(f"\n--- TRADES ADDED WHEN ETH WAS REMOVED ({len(new_trades_added)}) ---")
for t in new_trades_added:
    print(f"{t['pair']} | open: {t['open_date']} | tag: {t.get('enter_tag')} | pnl: {t['profit_abs']:.2f} | exit: {t['exit_reason']}")

# Find trades removed
new_keys = set((t['pair'], t['open_date']) for t in t_new)
trades_removed = [t for t in t_prev if (t['pair'], t['open_date']) not in new_keys]
print(f"\n--- TRADES REMOVED ({len(trades_removed)}) ---")
for t in trades_removed:
    print(f"{t['pair']} | open: {t['open_date']} | tag: {t.get('enter_tag')} | pnl: {t['profit_abs']:.2f} | exit: {t['exit_reason']}")
