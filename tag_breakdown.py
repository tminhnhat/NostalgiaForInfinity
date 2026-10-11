import zipfile
import json
import pandas as pd
import glob
import talib.abstract as ta

zp = 'user_data/backtest_results/backtest-result-2026-10-11_12-11-43.zip'
with zipfile.ZipFile(zp) as z:
    for n in z.namelist():
        if n.endswith('.json') and not n.endswith('.meta.json'):
            d = json.loads(z.read(n).decode('utf-8'))
            if 'strategy' in d:
                trades = d['strategy']['NostalgiaForInfinityX8_Combined']['trades']
                break

for check_tag in ['701', '702', '703', '731', '711', '712', '721', '722']:
    t_list = [t for t in trades if t.get('is_short', False) and check_tag in t.get('enter_tag', '')]
    if not t_list:
        continue
    wins = [t for t in t_list if t.get('profit_abs', 0) > 0]
    losses = [t for t in t_list if t.get('profit_abs', 0) < 0]
    pnl = sum(t.get('profit_abs', 0) for t in t_list)
    print(f"TAG {check_tag}: Total: {len(t_list):2d} | Win: {len(wins):2d} | Loss: {len(losses):2d} | Winrate: {len(wins)/len(t_list)*100:5.1f}% | PnL: {pnl:7.2f}$")
