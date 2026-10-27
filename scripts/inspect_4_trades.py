import json
import zipfile
import glob

zip_files = sorted(glob.glob('user_data/backtest_results/backtest-result-*.zip'))
latest_zip = zip_files[-1]
with zipfile.ZipFile(latest_zip, 'r') as z:
    for name in z.namelist():
        if name.endswith('.json') and not name.endswith('.meta.json'):
            data = json.loads(z.read(name))
            trades = data.get('strategy', {}).get('NostalgiaForInfinityX8_Combined_AI', {}).get('trades', [])
            target_trades = [t for t in trades if t.get('enter_tag') == '702 703 731_AI_PASS' and any(p in t.get('pair') for p in ['PUMP', 'PYTH', 'STRK', 'MSTR'])]
            for t in target_trades:
                print(f"{t['pair']} | open={t['open_date']} | close={t['close_date']} | profit_ratio={t['profit_ratio']*100:.2f}% | exit={t['exit_reason']}")
