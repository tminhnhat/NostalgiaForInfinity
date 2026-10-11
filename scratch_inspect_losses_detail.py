import zipfile
import json
import pandas as pd
import numpy as np
import sys

sys.stdout.reconfigure(encoding='utf-8')

latest_zip = 'user_data/backtest_results/backtest-result-2026-10-11_12-11-43.zip'

with zipfile.ZipFile(latest_zip, 'r') as z:
    for name in z.namelist():
        if name.endswith('.json') and not name.endswith('.meta.json'):
            data = json.loads(z.read(name).decode('utf-8'))
            strat = list(data['strategy'].keys())[0]
            trades = data['strategy'][strat]['trades']
            losses = [t for t in trades if t.get('enter_tag') == '702 703 731' and t.get('profit_abs', 0) <= 0]
            
            print("=== PHAN TICH CHI TIET TUNG LENH THUA ===")
            for i, t in enumerate(losses, 1):
                p = t['pair']
                o_d = t['open_date']
                c_d = t['close_date']
                dur = t.get('trade_duration', 0) / 60.0
                pnl = t['profit_abs']
                pct = t['profit_ratio'] * 100
                reason = t.get('exit_reason', '')
                o_rate = t['open_rate']
                c_rate = t['close_rate']
                min_rate = t.get('min_rate', o_rate)
                max_rate = t.get('max_rate', o_rate)
                
                # Check price movement
                favorable_price_pct = (o_rate - min_rate) / o_rate * 100 # % gia giam toi da (co loi)
                adverse_price_pct = (max_rate - o_rate) / o_rate * 100   # % gia tang toi da (bat loi)
                
                print(f"Lệnh #{i}: {p} | Vào: {o_d} | Ra: {c_d} ({dur:.1f}h)")
                print(f"   Giá vào: {o_rate:.4f} | Giá thấp nhất: {min_rate:.4f} (-{favorable_price_pct:.2f}% giá) | Giá cao nhất: {max_rate:.4f} (+{adverse_price_pct:.2f}% giá)")
                print(f"   PnL: {pnl:.2f}$ ({pct:.1f}%) | Lý do thoát: {reason}\n")
