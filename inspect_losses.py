import zipfile
import json
import glob

zps = sorted(glob.glob('user_data/backtest_results/*.zip'))
latest_zp = zps[-1]
print("Latest zip:", latest_zp)
with zipfile.ZipFile(latest_zp) as z:
    for n in z.namelist():
        if n.endswith('.json') and not n.endswith('.meta.json'):
            d = json.loads(z.read(n).decode('utf-8'))
            if 'strategy' in d:
                trades = d['strategy']['NostalgiaForInfinityX8_Combined']['trades']
                losses = [t for t in trades if t.get('profit_abs', 0) < 0]
                print(f"Total trades: {len(trades)}, Losses: {len(losses)}")
                for l in losses:
                    print(f"Pair: {l['pair']:<14} | Open: {l['open_date']} | Close: {l['close_date']} | Dur: {l['trade_duration']/60:.1f}h | Tag: {l.get('enter_tag')} | Exit: {l.get('exit_reason')} | Profit: {l.get('profit_abs'):.2f}$ ({l.get('profit_ratio')*100:.2f}%)")
