import json
import glob
import zipfile

zips = sorted(glob.glob('user_data/backtest_results/backtest-result-*.zip'))
latest = zips[-1]
with zipfile.ZipFile(latest, 'r') as z:
    for n in z.namelist():
        if n.endswith('.json') and not n.endswith('.meta.json'):
            d = json.loads(z.read(n))
            if 'strategy' in d and isinstance(d['strategy'], dict):
                strat_data = d['strategy'].get('NostalgiaForInfinityX8_Combined_AI', {})
                if 'trades' in strat_data:
                    for t in strat_data['trades']:
                        if t.get('enter_tag') == '702 703 731_AI_PASS' and any(p in t['pair'] for p in ['PYTH', 'PUMP', 'STRK', 'MSTR']):
                            print(f"{t['pair']} | open={t['open_rate']} | close={t['close_rate']} | profit_ratio={t['profit_ratio']*100:.2f}% | profit_abs={t['profit_abs']:.2f} | exit_reason={t['exit_reason']} | open_date={t['open_date']} | close_date={t['close_date']}")
