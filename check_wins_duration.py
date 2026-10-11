import zipfile
import json

zp = 'user_data/backtest_results/backtest-result-2026-10-11_12-11-43.zip'
with zipfile.ZipFile(zp) as z:
    for n in z.namelist():
        if n.endswith('.json') and not n.endswith('.meta.json'):
            d = json.loads(z.read(n).decode('utf-8'))
            if 'strategy' in d:
                trades = d['strategy']['NostalgiaForInfinityX8_Combined']['trades']
                break

wins = [t for t in trades if t.get('profit_abs', 0) > 0 and t.get('is_short', False)]
wins_gt_36 = [t for t in wins if t['trade_duration']/60 > 36]
print(f"Total wins in 1382: {len(wins)}")
print(f"Wins taking > 36h: {len(wins_gt_36)} ({len(wins_gt_36)/len(wins)*100:.1f}%)")
print(f"Profit of wins taking > 36h: {sum(t['profit_abs'] for t in wins_gt_36):.2f}$")

# Also check how many trades had current_profit < -0.02 at 36h and then went on to WIN
