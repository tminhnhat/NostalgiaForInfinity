import zipfile
import json
import pandas as pd
import glob
import talib.abstract as ta

zp = 'user_data/backtest_results/backtest-result-2026-10-11_17-30-07.zip'
with zipfile.ZipFile(zp) as z:
    for n in z.namelist():
        if n.endswith('.json') and not n.endswith('.meta.json'):
            d = json.loads(z.read(n).decode('utf-8'))
            strat = list(d['strategy'].keys())[0]
            trades = d['strategy'][strat]['trades']
            break

t_702 = [t for t in trades if t.get('enter_tag') == '702 703 731']

rows = []
for t in t_702:
    pair = t['pair']
    base = pair.split('/')[0]
    open_date = t['open_date']
    f_files = glob.glob(f"user_data/data/binance/futures/{base}_USDT_USDT-5m-futures.feather")
    if not f_files:
        continue
    df = pd.read_feather(f_files[0])
    df['date'] = pd.to_datetime(df['date'], utc=True)
    open_t = pd.to_datetime(open_date)
    row = df[df['date'] == open_t]
    if len(row) == 0:
        continue
    idx = row.index[0]
    # signal candle is the candle BEFORE open_date (idx-1)
    sig_idx = idx - 1
    sub = df.iloc[max(0, sig_idx-200):sig_idx+1].copy()
    c = sub['close'].to_numpy()
    h = sub['high'].to_numpy()
    l = sub['low'].to_numpy()
    o = sub['open'].to_numpy()
    v = sub['volume'].to_numpy()
    
    rsi14 = ta.RSI(c, timeperiod=14)[-1]
    hl = h[-1] - l[-1] if h[-1] > l[-1] else 1e-9
    l_wick = (min(c[-1], o[-1]) - l[-1]) / hl
    u_wick = (h[-1] - max(c[-1], o[-1])) / hl
    body = abs(c[-1] - o[-1]) / hl
    ema200 = ta.EMA(c, timeperiod=200)[-1]
    dist_ema200 = (c[-1] - ema200) / ema200 * 100
    
    macd, macdsig, macdhist = ta.MACD(c, fastperiod=12, slowperiod=26, signalperiod=9)
    macd_accel = macdhist[-1] < macdhist[-2] if len(macdhist) >= 2 else True
    
    is_win = t['profit_abs'] > 0
    rows.append({
        'pair': pair,
        'open_date': open_date,
        'day': open_t.weekday(), # 0: Mon, ..., 6: Sun
        'is_sunday': open_t.weekday() == 6,
        'win': is_win,
        'profit': t['profit_abs'],
        'rsi14': rsi14,
        'l_wick': l_wick,
        'u_wick': u_wick,
        'body': body,
        'dist_ema200': dist_ema200,
        'macd_accel': macd_accel,
        'exit_reason': t['exit_reason']
    })

df = pd.DataFrame(rows)
total_trades = len(df)
base_wins = df['win'].sum()
base_pnl = df['profit'].sum()
print(f"BASELINE 702 703 731: Trades={total_trades}, Wins={base_wins}, Winrate={base_wins/total_trades*100:.1f}%, PnL={base_pnl:.2f}$")

# Test 1: lower_wick_ratio <= 0.30 (Reject pinbar rút chân)
f1 = df['l_wick'] <= 0.30
print(f"\nFilter 1 (lower_wick <= 0.30): Trades={f1.sum()}, Wins={df[f1]['win'].sum()}, Winrate={df[f1]['win'].mean()*100:.1f}%, PnL={df[f1]['profit'].sum():.2f}$")

# Test 2: lower_wick_ratio <= 0.28
f2 = df['l_wick'] <= 0.28
print(f"Filter 2 (lower_wick <= 0.28): Trades={f2.sum()}, Wins={df[f2]['win'].sum()}, Winrate={df[f2]['win'].mean()*100:.1f}%, PnL={df[f2]['profit'].sum():.2f}$")

# Test 3: lower_wick <= 0.30 AND not Sunday (hoặc Sunday filter)
f3 = (df['l_wick'] <= 0.30) & (~df['is_sunday'])
print(f"Filter 3 (lower_wick <= 0.30 & No Sunday): Trades={f3.sum()}, Wins={df[f3]['win'].sum()}, Winrate={df[f3]['win'].mean()*100:.1f}%, PnL={df[f3]['profit'].sum():.2f}$")

# Test 4: lower_wick <= 0.30 AND body >= 0.35 (thân nến dứt khoát)
f4 = (df['l_wick'] <= 0.30) & (df['body'] >= 0.35)
print(f"Filter 4 (lower_wick <= 0.30 & body >= 0.35): Trades={f4.sum()}, Wins={df[f4]['win'].sum()}, Winrate={df[f4]['win'].mean()*100:.1f}%, PnL={df[f4]['profit'].sum():.2f}$")

# Test 5: lower_wick <= 0.30 & dist_ema200 >= -3.5% (không short khi đã rơi quá sâu xa EMA 200)
f5 = (df['l_wick'] <= 0.30) & (df['dist_ema200'] >= -3.5)
print(f"Filter 5 (lower_wick <= 0.30 & dist_ema200 >= -3.5%): Trades={f5.sum()}, Wins={df[f5]['win'].sum()}, Winrate={df[f5]['win'].mean()*100:.1f}%, PnL={df[f5]['profit'].sum():.2f}$")

# Test 6: lower_wick <= 0.30 & dist_ema200 >= -3.5% & macd_accel
f6 = (df['l_wick'] <= 0.30) & (df['dist_ema200'] >= -3.5) & (df['macd_accel'])
print(f"Filter 6 (lower_wick <= 0.30 & dist_ema200 >= -3.5% & macd_accel): Trades={f6.sum()}, Wins={df[f6]['win'].sum()}, Winrate={df[f6]['win'].mean()*100:.1f}%, PnL={df[f6]['profit'].sum():.2f}$")
