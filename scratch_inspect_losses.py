import json, glob, zipfile, os

zfiles = sorted(glob.glob('user_data/backtest_results/*.zip'), key=os.path.getmtime)
latest_zip = zfiles[-1]
print('Latest zip:', latest_zip)

with zipfile.ZipFile(latest_zip) as z:
    for name in z.namelist():
        if name.endswith('.json') and not name.endswith('_config.json'):
            try:
                data = json.loads(z.read(name))
                if 'strategy' in data and 'NostalgiaForInfinityX8_Combined' in data['strategy']:
                    strat_data = data['strategy']['NostalgiaForInfinityX8_Combined']
                    trades = strat_data['trades']
                    print(f"Total trades: {len(trades)}")
                    wins = [t for t in trades if t['profit_abs'] > 0]
                    losses = [t for t in trades if t['profit_abs'] <= 0]
                    total_pnl = sum(t['profit_abs'] for t in trades)
                    winrate = len(wins) / len(trades) * 100 if trades else 0
                    print(f"Total: {len(trades)} | Wins: {len(wins)} | Losses: {len(losses)} | Winrate: {winrate:.1f}% | Total Profit: {total_pnl:.2f} USDT")
                    
                    print("\n--- ALL LOSSES ---")
                    for t in losses:
                        p_ratio = t['profit_ratio'] * 100
                        print(f"{t['pair']:<15} {t['open_date']} tag: {t['enter_tag']:<25} profit: {t['profit_abs']:>8.2f} USDT ({p_ratio:>6.2f}%) exit: {t.get('exit_reason')}")
            except Exception as e:
                pass
