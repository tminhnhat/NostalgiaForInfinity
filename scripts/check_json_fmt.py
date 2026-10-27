import json
import glob
import zipfile

zips = sorted(glob.glob('user_data/backtest_results/backtest-result-*.zip'))
latest = zips[-1]
with zipfile.ZipFile(latest, 'r') as z:
    for n in z.namelist():
        if n.endswith('.json') and not n.endswith('.meta.json'):
            d = json.loads(z.read(n))
            print("Keys:", d.keys())
            strat = d.get('strategy', {})
            if not strat:
                # maybe d['strategy_comparison']
                for k, v in d.items():
                    if isinstance(v, dict) and 'trades' in v:
                        print(f"Found trades in {k}")
            else:
                strat_name = list(strat.keys())[0] if isinstance(strat, dict) else "unknown"
                print("Strat name:", strat_name)
