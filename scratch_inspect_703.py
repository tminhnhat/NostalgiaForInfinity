import json
import zipfile
import os

with open('user_data/backtest_results/.last_result.json') as f:
    last_file = json.load(f)['latest_backtest']

zip_path = os.path.join('user_data/backtest_results', last_file)
with zipfile.ZipFile(zip_path, 'r') as z:
    for name in z.namelist():
        if name.endswith('.json'):
            with z.open(name) as jf:
                data = json.load(jf)
            break

strat = list(data['strategy'].keys())[0]
trades = data['strategy'][strat]['trades']

trades_703 = [t for t in trades if '703' in t.get('enter_tag', '').split()]
print(f"Total 703 trades: {len(trades_703)}")
wins_703 = [t for t in trades_703 if t['profit_abs'] >= 0]
loss_703 = [t for t in trades_703 if t['profit_abs'] < 0]
print(f"Wins: {len(wins_703)}, Losses: {len(loss_703)}")

print("\n--- ALL 703 LOSS TRADES ---")
for t in loss_703:
    print(f"{t['pair']:<16} | opened: {t['open_date']} | closed: {t['close_date']} | pnl: {t['profit_abs']:7.2f} USDT ({t['profit_ratio']*100:6.2f}%) | exit: {t.get('exit_reason')}")
