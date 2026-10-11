import zipfile
import json

zp = 'user_data/backtest_results/backtest-result-2026-10-11_17-09-19.zip'
with zipfile.ZipFile(zp) as z:
    for n in z.namelist():
        if n.endswith('.json') and not n.endswith('.meta.json'):
            d = json.loads(z.read(n).decode('utf-8'))
            if 'strategy' in d:
                trades = d['strategy']['NostalgiaForInfinityX8_Combined']['trades']
                break

stale_trades = [t for t in trades if 'custom_short_time_stale_36h' in t.get('exit_reason', '')]
print(f"Stale trades exited: {len(stale_trades)}")
for t in stale_trades:
    print(f"Pair: {t['pair']:<14} | Open: {t['open_date']} | Close: {t['close_date']} | Dur: {t['trade_duration']/60:.1f}h | Profit: {t['profit_abs']:.2f}$ ({t['profit_ratio']*100:.2f}%)")
