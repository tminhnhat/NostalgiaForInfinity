import zipfile
import json
import pandas as pd
import glob
import talib.abstract as ta
import numpy as np

zp = 'user_data/backtest_results/backtest-result-2026-10-11_17-30-07.zip'
with zipfile.ZipFile(zp) as z:
    for n in z.namelist():
        if n.endswith('.json') and not n.endswith('.meta.json'):
            d = json.loads(z.read(n).decode('utf-8'))
            strat = list(d['strategy'].keys())[0]
            trades = d['strategy'][strat]['trades']
            break

t_702_703_731 = [t for t in trades if t.get('enter_tag') == '702 703 731']
print(f"Total trades with exact tag '702 703 731': {len(t_702_703_731)}")

rows = []
for t in t_702_703_731:
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
    sub = df.iloc[max(0, idx-300):idx+1].copy()
    c = sub['close'].to_numpy()
    h = sub['high'].to_numpy()
    l = sub['low'].to_numpy()
    o = sub['open'].to_numpy()
    v = sub['volume'].to_numpy()
    
    rsi14 = ta.RSI(c, timeperiod=14)[-1]
    fastk, fastd = ta.STOCHRSI(c, timeperiod=14, fastk_period=3, fastd_period=3)
    k = fastk[-1]
    d_val = fastd[-1]
    ema9 = ta.EMA(c, timeperiod=9)[-1]
    ema21 = ta.EMA(c, timeperiod=21)[-1]
    ema50 = ta.EMA(c, timeperiod=50)[-1]
    ema200 = ta.EMA(c, timeperiod=200)[-1]
    macd, macdsig, macdhist = ta.MACD(c, fastperiod=12, slowperiod=26, signalperiod=9)
    vol_sma = ta.SMA(v, timeperiod=20)[-1]
    vol_spike = v[-1] / (vol_sma if vol_sma > 0 else 1)
    
    # Distance to EMA 200
    dist_ema200 = (c[-1] - ema200) / ema200 * 100
    # Distance to EMA 50
    dist_ema50 = (c[-1] - ema50) / ema50 * 100
    
    # Candle upper wick ratio
    hl = h[-1] - l[-1] if h[-1] > l[-1] else 1e-9
    u_wick = (h[-1] - max(c[-1], o[-1])) / hl
    l_wick = (min(c[-1], o[-1]) - l[-1]) / hl
    body = abs(c[-1] - o[-1]) / hl
    
    is_win = t['profit_abs'] > 0
    rows.append({
        'pair': pair,
        'open_date': open_date,
        'day_of_week': open_t.strftime('%A'),
        'hour_utc': open_t.hour,
        'win': is_win,
        'profit_abs': t['profit_abs'],
        'profit_ratio': t['profit_ratio'],
        'exit_reason': t['exit_reason'],
        'duration_h': t['trade_duration']/60,
        'rsi14': rsi14,
        'stoch_k': k,
        'stoch_d': d_val,
        'dist_ema200': dist_ema200,
        'dist_ema50': dist_ema50,
        'vol_spike': vol_spike,
        'u_wick': u_wick,
        'l_wick': l_wick,
        'body': body,
        'macdhist': macdhist[-1]
    })

df_analysis = pd.DataFrame(rows)
print("\n=== THỐNG KÊ TRUNG BÌNH: WINS vs LOSSES ===")
print(df_analysis.groupby('win')[['rsi14', 'stoch_k', 'dist_ema200', 'dist_ema50', 'vol_spike', 'u_wick', 'l_wick', 'body', 'macdhist']].mean().to_string())

print("\n=== PHÂN BỐ THEO THỨ TRONG TUẦN (DAY OF WEEK) ===")
print(df_analysis.groupby(['day_of_week', 'win'])['profit_abs'].count().unstack().fillna(0))

print("\n=== TẤT CẢ 11 LỆNH THUA CỦA 702 703 731 ===")
losses = df_analysis[~df_analysis['win']]
for _, r in losses.iterrows():
    print(f"{r['pair']:<14} | {r['open_date']} ({r['day_of_week']:<9}) | Dur: {r['duration_h']:4.1f}h | PnL: {r['profit_abs']:6.2f}$ | RSI: {r['rsi14']:.1f} | StochK: {r['stoch_k']:.1f} | DistEMA200: {r['dist_ema200']:.2f}% | DistEMA50: {r['dist_ema50']:.2f}% | VolSpike: {r['vol_spike']:.2f} | Exit: {r['exit_reason']}")
