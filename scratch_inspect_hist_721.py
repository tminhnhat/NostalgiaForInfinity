import json
import zipfile
import glob
import os
import pandas as pd
import numpy as np

# Let's inspect all trades that have ever had 721 in all backtests
zip_files = glob.glob('user_data/backtest_results/backtest-result-*.zip')
zip_files.sort(key=os.path.getmtime, reverse=True)

all_721_trades = []
for zpath in zip_files[:5]:
    with zipfile.ZipFile(zpath) as z:
        for n in z.namelist():
            if n.endswith('.json') and not n.endswith('.meta.json') and not n.endswith('_config.json'):
                with z.open(n) as f:
                    data = json.load(f)
                    trades = data['strategy']['NostalgiaForInfinityX8_Combined']['trades']
                    t721 = [t for t in trades if '721' in str(t.get('enter_tag'))]
                    print(f"\n{os.path.basename(zpath)}: {len(t721)} trades with 721:")
                    for t in t721:
                        print(f"  {t['pair']} | open: {t['open_date']} | tag: {t.get('enter_tag')} | pnl: {t['profit_abs']:.2f} | exit: {t['exit_reason']}")
                    break
