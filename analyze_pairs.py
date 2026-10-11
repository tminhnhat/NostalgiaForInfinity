import zipfile
import json

with zipfile.ZipFile('user_data/backtest_results/backtest-result-2026-10-10_22-28-13.zip') as z:
    for name in z.namelist():
        if name.endswith('.json') and not name.endswith('.meta.json'):
            d = json.loads(z.read(name))
            strat_data = d['strategy']['NostalgiaForInfinityX8_Combined'] if 'strategy' in d else d
            pairs = strat_data.get('results_per_pair', [])
            print('=== PAIRS (BEST TO WORST) ===')
            for p in sorted(pairs, key=lambda x: x.get('profit_total_abs', 0), reverse=True):
                if p['key'] == 'TOTAL': continue
                wr = p.get('winrate', 0) * 100
                print(f"{p['key']:20}: {p['trades']:3} trades | WR: {wr:5.1f}% | PnL: {p.get('profit_total_abs', 0):7.2f} USDT")
