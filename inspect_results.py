import zipfile
import json
import glob

for zp in sorted(glob.glob('user_data/backtest_results/*.zip'))[-4:]:
    with zipfile.ZipFile(zp) as z:
        for n in z.namelist():
            if n.endswith('.json') and not n.endswith('.meta.json'):
                try:
                    d = json.loads(z.read(n).decode('utf-8'))
                    if 'strategy' in d:
                        for s, val in d['strategy'].items():
                            print(f"{zp} | {s}:")
                            print(f"  Trades: {val.get('total_trades')}, Wins: {val.get('wins')}, Losses: {val.get('losses')}, Winrate: {val.get('winrate', 0)*100:.1f}%")
                            print(f"  Profit: {val.get('profit_total_abs'):.2f} USDT ({val.get('profit_total', 0)*100:.2f}%), Max DD: {val.get('max_drawdown_account', 0)*100:.2f}%")
                            # Count exit reasons
                            reasons = {}
                            for t in val.get('trades', []):
                                r = t.get('exit_reason', 'unknown')
                                reasons[r] = reasons.get(r, 0) + 1
                            print(f"  Exit reasons: {reasons}")
                except Exception as e:
                    print(f"Error {zp}: {e}")
