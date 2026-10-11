import zipfile
import json
import glob
import sys

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

latest_zip = 'user_data/backtest_results/backtest-result-2026-10-11_12-11-43.zip'

with zipfile.ZipFile(latest_zip, 'r') as z:
    for name in z.namelist():
        if name.endswith('.json') and not name.endswith('.meta.json'):
            data = json.loads(z.read(name).decode('utf-8'))
            strat = list(data['strategy'].keys())[0]
            trades = data['strategy'][strat]['trades']
            t_702 = [t for t in trades if t.get('enter_tag') == '702 703 731']
            print(f"Total 702 703 731 trades: {len(t_702)}")
            wins = [t for t in t_702 if t.get('profit_abs', 0) > 0]
            losses = [t for t in t_702 if t.get('profit_abs', 0) <= 0]
            print(f"Wins: {len(wins)}, Losses: {len(losses)}, Winrate: {len(wins)/len(t_702)*100:.1f}%")
            print("\n=== DETAILS OF 11 LOSSES of 702 703 731 ===")
            for i, t in enumerate(losses, 1):
                open_d = t['open_date']
                close_d = t['close_date']
                dur_h = t.get('trade_duration', 0) / 60.0
                pnl = t['profit_abs']
                pct = t['profit_ratio'] * 100
                reason = t.get('exit_reason', 'N/A')
                pair = t['pair']
                min_rate = t.get('min_rate', 0)
                max_rate = t.get('max_rate', 0)
                open_rate = t.get('open_rate', 0)
                # max favorable excursion (highest profit reached during trade)
                max_profit_reached = (open_rate - min_rate) / open_rate * 5.0 * 100 if open_rate > 0 else 0
                print(f"#{i:2d} | Pair: {pair:16} | Enter: {open_d} | Exit: {close_d} | Hold: {dur_h:5.1f}h | PeakProfit: {max_profit_reached:5.1f}% | PnL: {pnl:7.2f}$ ({pct:6.2f}%) | ExitReason: {reason}")
