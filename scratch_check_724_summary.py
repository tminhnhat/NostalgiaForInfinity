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
                
                # Check trades on 2026-08-31
                print("All trades on 2026-08-31:")
                for t in trades:
                    if '2026-08-31' in t['open_date']:
                        print(f"{t['pair']} | open: {t['open_date']} | tag: {t['enter_tag']} | pnl: {t['profit_abs']:.2f} | exit: {t['exit_reason']}")
                
                # Summary of all trades with 724
                trades_724 = [t for t in trades if '724' in str(t.get('enter_tag'))]
                total_pnl_724 = sum(t['profit_abs'] for t in trades_724)
                print(f"\nTotal 724 trades: {len(trades_724)} | Total PnL: {total_pnl_724:.2f} USDT")
