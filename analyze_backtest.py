import zipfile
import json

with zipfile.ZipFile('user_data/backtest_results/backtest-result-2026-10-11_07-43-47.zip') as z:
    for name in z.namelist():
        if name.endswith('.json') and not name.endswith('.meta.json'):
            d = json.loads(z.read(name))
            strat_data = d['strategy']['NostalgiaForInfinityX8_Combined'] if 'strategy' in d else d
            tags = strat_data.get('results_per_enter_tag', [])
            
            print('=== ENTER TAGS (BY PROFIT) ===')
            for t in sorted(tags, key=lambda x: x.get('profit_total_abs', 0), reverse=True)[:15]:
                wr = t.get('winrate', 0) * 100
                p = t.get('profit_total_abs', 0)
                tot = t.get('trades', 0)
                wins = t.get('wins', 0)
                losses = t.get('losses', 0)
                print(f"{t['key']:30}: {tot:4} trades | Win: {wins:4} | Loss: {losses:4} ({wr:5.1f}%) | pnl: {p:7.2f} USDT")

            print('\n=== PAIRS ===')
            pairs = strat_data.get('results_per_pair', [])
            for p in sorted(pairs, key=lambda x: x.get('profit_total_abs', 0), reverse=True):
                if p['key'] == 'TOTAL': continue
                wr = p.get('winrate', 0) * 100
                print(f"{p['key']:20}: {p['trades']:3} trades | WR: {wr:5.1f}% | PnL: {p.get('profit_total_abs', 0):7.2f} USDT")

            print('\n=== EXIT REASONS ===')
            exits = strat_data.get('exit_reason_summary', [])
            for r in sorted(exits, key=lambda x: x.get('profit_total_abs', 0), reverse=True)[:10]:
                tot = r.get('trades', 0)
                wins = r.get('wins', 0)
                losses = r.get('losses', 0)
                p_abs = r.get('profit_total_abs', 0)
                print(f"{r['key']:45}: {tot:4} trades | Win: {wins:4} | Loss: {losses:4} | Profit: {p_abs:8.2f} USDT")

            print('\n=== WORST EXIT REASONS ===')
            for r in sorted(exits, key=lambda x: x.get('profit_total_abs', 0))[:10]:
                tot = r.get('trades', 0)
                wins = r.get('wins', 0)
                losses = r.get('losses', 0)
                p_abs = r.get('profit_total_abs', 0)
                print(f"{r['key']:45}: {tot:4} trades | Win: {wins:4} | Loss: {losses:4} | Profit: {p_abs:8.2f} USDT")
