import json, glob, zipfile, os

zfiles = sorted(glob.glob('user_data/backtest_results/*.zip'), key=os.path.getmtime)
latest_zip = zfiles[-1]
print('Latest zip:', latest_zip)

with zipfile.ZipFile(latest_zip) as z:
    for name in z.namelist():
        if name.endswith('.json'):
            data = json.loads(z.read(name))
            trades = data['strategy']['NostalgiaForInfinityX8_Combined']['trades']
            t721 = [t for t in trades if '721' in str(t.get('enter_tag'))]
            print(f'Total trades with 721: {len(t721)}')
            wins = [t for t in t721 if t['profit_abs'] > 0]
            losses = [t for t in t721 if t['profit_abs'] <= 0]
            pnl = sum(t['profit_abs'] for t in t721)
            winrate = (len(wins) / len(t721) * 100) if t721 else 0
            print(f'Wins: {len(wins)}, Losses: {len(losses)}, Winrate: {winrate:.1f}%, Total PnL: {pnl:.2f}')
            for t in t721:
                p_ratio = t['profit_ratio'] * 100
                print(f"{t['pair']:<15} {t['open_date']} tag: {t['enter_tag']:<20} profit: {t['profit_abs']:>8.2f} USDT ({p_ratio:>6.2f}%) exit: {t.get('exit_reason')}")
