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

all_trades = pd.DataFrame(trades)
all_trades['open_dt'] = pd.to_datetime(all_trades['open_date'])
all_trades['is_sunday'] = all_trades['open_dt'].dt.dayofweek == 6

# Extract candle indicators for all trades
rows = []
for idx_t, t in all_trades.iterrows():
    pair = t['pair']
    base = pair.split('/')[0]
    open_date = t['open_date']
    f_files = glob.glob(f"user_data/data/binance/futures/{base}_USDT_USDT-5m-futures.feather")
    if not f_files:
        continue
    df_f = pd.read_feather(f_files[0])
    df_f['date'] = pd.to_datetime(df_f['date'], utc=True)
    open_t = pd.to_datetime(open_date)
    r_idx = df_f[df_f['date'] == open_t]
    if len(r_idx) == 0:
        continue
    idx = r_idx.index[0]
    # signal candle
    sig = df_f.iloc[idx-1]
    sub = df_f.iloc[max(0, idx-201):idx].copy()
    c = sub['close'].to_numpy()
    h = sub['high'].to_numpy()
    l = sub['low'].to_numpy()
    o = sub['open'].to_numpy()
    
    hl = h[-1] - l[-1] if h[-1] > l[-1] else 1e-9
    l_wick = (min(c[-1], o[-1]) - l[-1]) / hl
    ema200 = ta.EMA(c, timeperiod=200)[-1]
    dist_ema200 = (c[-1] - ema200) / ema200 * 100
    
    rows.append({
        'index': idx_t,
        'pair': pair,
        'open_date': open_date,
        'is_short': t['is_short'],
        'enter_tag': t['enter_tag'],
        'profit_abs': t['profit_abs'],
        'is_win': t['profit_abs'] > 0,
        'is_sunday': t['open_dt'].weekday() == 6,
        'l_wick': l_wick,
        'dist_ema200': dist_ema200
    })

df_sim = pd.DataFrame(rows)

print("=== BASELINE (HIỆN TẠI) ===")
print(f"Tổng lệnh: {len(df_sim)} | Thắng: {df_sim['is_win'].sum()} ({df_sim['is_win'].mean()*100:.1f}%) | PnL: {df_sim['profit_abs'].sum():.2f}$")

# Test 1: Only block 702 703 731 on Sunday
mask_test1 = ~((df_sim['is_sunday']) & (df_sim['is_short']) & (df_sim['enter_tag'].str.contains('702|703|731')))
sub1 = df_sim[mask_test1]
print(f"\nĐỀ XUẤT 1: Không Short vào Chủ Nhật (No Sunday Short):")
print(f"Tổng lệnh: {len(sub1)} | Thắng: {sub1['is_win'].sum()} ({sub1['is_win'].mean()*100:.1f}%) | PnL: {sub1['profit_abs'].sum():.2f}$ (Cải thiện +{sub1['profit_abs'].sum() - df_sim['profit_abs'].sum():.2f}$)")

# Test 2: Reject lower_wick > 0.35 on 702 703 731
mask_test2 = ~( (df_sim['enter_tag'].str.contains('702|703|731')) & (df_sim['l_wick'] > 0.35) )
sub2 = df_sim[mask_test2]
print(f"\nĐỀ XUẤT 2: Chặn nến rút chân (lower_wick_ratio <= 0.35):")
print(f"Tổng lệnh: {len(sub2)} | Thắng: {sub2['is_win'].sum()} ({sub2['is_win'].mean()*100:.1f}%) | PnL: {sub2['profit_abs'].sum():.2f}$ (Cải thiện +{sub2['profit_abs'].sum() - df_sim['profit_abs'].sum():.2f}$)")

# Test 3: Reject overextended dump (dist_ema200 < -3.5%)
mask_test3 = ~( (df_sim['enter_tag'].str.contains('702|703|731')) & (df_sim['dist_ema200'] < -3.5) )
sub3 = df_sim[mask_test3]
print(f"\nĐỀ XUẤT 3: Chặn Short đuổi khi giá đã cách xa EMA200 > 3.5%:")
print(f"Tổng lệnh: {len(sub3)} | Thắng: {sub3['is_win'].sum()} ({sub3['is_win'].mean()*100:.1f}%) | PnL: {sub3['profit_abs'].sum():.2f}$ (Cải thiện +{sub3['profit_abs'].sum() - df_sim['profit_abs'].sum():.2f}$)")

# Test 4: Combined 1 + 2 + 3
mask_test4 = mask_test1 & mask_test2 & mask_test3
sub4 = df_sim[mask_test4]
print(f"\nĐỀ XUẤT 4 (TỔ HỢP 1 + 2 + 3):")
print(f"Tổng lệnh: {len(sub4)} | Thắng: {sub4['is_win'].sum()} ({sub4['is_win'].mean()*100:.1f}%) | PnL: {sub4['profit_abs'].sum():.2f}$ (Cải thiện +{sub4['profit_abs'].sum() - df_sim['profit_abs'].sum():.2f}$)")
