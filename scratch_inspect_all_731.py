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
                trades = data['strategy']['NostalgiaForInfinityX8_Combined'].get('trades', [])
                trades_with_731 = [t for t in trades if '731' in str(t.get('enter_tag'))]
                print(f"Total trades containing 731: {len(trades_with_731)}")
                for t in trades_with_731:
                    print(f"{t['pair']} | open: {t['open_date']} | tag: {t['enter_tag']} | pnl: {t['profit_abs']:.2f} | exit: {t['exit_reason']}")
