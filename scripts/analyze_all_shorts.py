import zipfile, json
from pathlib import Path
from collections import Counter

def main():
    backtest_dir = Path('user_data/backtest_results')
    zip_files = sorted(list(backtest_dir.glob('backtest-result-*.zip')), key=lambda p: p.stat().st_mtime, reverse=True)
    result_zip = zip_files[0]
    print('Using zip:', result_zip.name)

    with zipfile.ZipFile(result_zip) as z:
        for name in z.namelist():
            if name.endswith('.json') and not name.endswith('.meta.json') and not name.endswith('_config.json'):
                data = json.loads(z.read(name).decode('utf-8'))
                strat_key = list(data.get('strategy', data).keys())[0]
                trades = data.get('strategy', data)[strat_key].get('trades', [])
                break

    short_trades = [t for t in trades if t.get('is_short', False)]
    print(f'Total Short Trades: {len(short_trades)}')

    tag_stats = {}
    for t in short_trades:
        tag = (t.get('enter_tag') or 'UNKNOWN').strip()
        if tag not in tag_stats:
            tag_stats[tag] = {
                'count': 0, 'wins': 0, 'losses': 0,
                'profit': 0.0, 'roe_sum': 0.0,
                'mfe_sum': 0.0, 'mae_sum': 0.0,
                'dur_sum': 0.0
            }
        tag_stats[tag]['count'] += 1
        p = float(t.get('profit_abs', 0.0))
        roe = float(t.get('profit_ratio', 0.0)) * 100
        tag_stats[tag]['profit'] += p
        tag_stats[tag]['roe_sum'] += roe
        tag_stats[tag]['dur_sum'] += float(t.get('trade_duration', 0))
        
        open_r = t['open_rate']
        min_r = t.get('min_rate', open_r)
        max_r = t.get('max_rate', open_r)
        lev = float(t.get('leverage') or 5.0)
        mfe_lev = (open_r - min_r) / open_r * 100 * lev
        mae_lev = (max_r - open_r) / open_r * 100 * lev
        tag_stats[tag]['mfe_sum'] += mfe_lev
        tag_stats[tag]['mae_sum'] += mae_lev

        if p > 0:
            tag_stats[tag]['wins'] += 1
        else:
            tag_stats[tag]['losses'] += 1

    print(f"{'Enter Tag':<35} | {'Count':<5} | {'Wins':<4} | {'Loss':<4} | {'WR%':<6} | {'Profit USDT':<12} | {'Avg ROE%':<8} | {'Avg MFE%':<8} | {'Avg MAE%':<8} | {'Avg Dur':<7}")
    print('-' * 115)
    for tag, s in sorted(tag_stats.items(), key=lambda x: x[1]['profit'], reverse=True):
        wr = s['wins'] / s['count'] * 100
        avg_roe = s['roe_sum'] / s['count']
        avg_mfe = s['mfe_sum'] / s['count']
        avg_mae = s['mae_sum'] / s['count']
        avg_dur = f"{int(s['dur_sum'] / s['count'])}m"
        print(f"{tag:<35} | {s['count']:>5} | {s['wins']:>4} | {s['losses']:>4} | {wr:>5.1f}% | {s['profit']:>+10.2f} $ | {avg_roe:>+7.2f}% | {avg_mfe:>+7.2f}% | -{avg_mae:>6.2f}% | {avg_dur:>7}")

    print("\n--- EXIT REASONS SUMMARY ---")
    reasons = Counter(t.get('exit_reason') for t in short_trades)
    for r, c in reasons.most_common():
        p = sum(t['profit_abs'] for t in short_trades if t.get('exit_reason') == r)
        print(f"{r:<35}: {c:>3} trades | Profit: {p:>+8.2f} USDT")

    print("\n--- LOSING SHORT TRADES ---")
    for t in short_trades:
        if t['profit_abs'] < 0:
            print(f"{t['pair']:<12} | {t.get('enter_tag'):<32} | {t.get('exit_reason'):<30} | dur: {t['trade_duration']:>4}m | profit: {t['profit_abs']:>+7.2f}$ ({t['profit_ratio']*100:>+5.1f}%)")

if __name__ == '__main__':
    main()
