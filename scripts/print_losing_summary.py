import json
import pandas as pd
import sys

sys.stdout.reconfigure(encoding="utf-8")

with open("user_data/deep_dive_losing_trades.json", "r", encoding="utf-8") as f:
    trades = json.load(f)

rows = []
for t in trades:
    tid = t['id']
    pair = t['pair']
    is_short = bool(t['is_short'])
    pos_str = "SHORT" if is_short else "LONG"
    is_open = bool(t['is_open'])
    tag = t['enter_tag']
    exit_reason = t['exit_reason'] if not is_open else "STILL OPEN"
    open_date = t['open_date'][:16]
    close_date = t['close_date'][:16] if not is_open else "OPEN"
    
    stake = float(t['stake_amount'] or 0)
    max_stake = float(t['max_stake_amount'] or 0)
    open_rate = float(t['open_rate'] or 0)
    close_rate = float(t['close_rate'] or 0)
    stop_loss = float(t['stop_loss'] or 0)
    liq_price = float(t['liquidation_price'] or 0)
    leverage = float(t['leverage'] or 1)
    profit_pct = float(t['close_profit'] or 0) * 100
    profit_abs = float(t['close_profit_abs'] or 0)
    funding_fees = float(t['funding_fees'] or 0)
    
    orders = t.get('orders', [])
    buy_orders = [o for o in orders if o['side'] == 'buy' and o['status'] == 'closed']
    sell_orders = [o for o in orders if o['side'] == 'sell' and o['status'] == 'closed']
    
    initial_buy = buy_orders[0] if (not is_short and buy_orders) else (sell_orders[0] if is_short and sell_orders else None)
    initial_price = float(initial_buy['average'] or initial_buy['price'] or open_rate) if initial_buy else open_rate
    
    if initial_price > 0 and close_rate > 0:
        price_drop = ((close_rate - initial_price) / initial_price) * 100 if not is_short else ((initial_price - close_rate) / initial_price) * 100
    else:
        price_drop = 0.0

    # Loss with 5% SL on initial stake:
    sl5_loss_abs = -0.25 * stake if not is_open else 0 # 5% price drop * 5x leverage = 25% on stake
    no_dca_loss_abs = stake * (price_drop * leverage / 100.0) if not is_open else 0
    
    rows.append({
        "id": tid,
        "pair": pair.split(":")[0],
        "pos": pos_str,
        "tag": tag.strip() if tag else "",
        "open": open_date,
        "close": close_date,
        "init_stake": round(stake, 2),
        "max_stake": round(max_stake, 2),
        "orders": len(orders),
        "asset_drop%": round(price_drop, 2),
        "exit_rate": round(close_rate, 4),
        "liq_price": round(liq_price, 4),
        "bot_sl": round(stop_loss, 4),
        "profit_abs": round(profit_abs, 2),
        "profit%": round(profit_pct, 2),
        "sl5_loss": round(sl5_loss_abs, 2),
        "saved_with_sl5": round(abs(profit_abs) - abs(sl5_loss_abs), 2) if profit_abs < 0 else 0,
        "exit_reason": exit_reason
    })

df = pd.DataFrame(rows)
print(df.to_string())

print("\n=== TOTAL LOSSES AGGREGATE ===")
closed_losses = df[df['profit_abs'] < 0]
print(f"Total Closed Losing Trades: {len(closed_losses)}")
print(f"Total Actual Loss: {closed_losses['profit_abs'].sum():.2f} USDT")
print(f"Total Loss if 5% Hard SL was used: {closed_losses['sl5_loss'].sum():.2f} USDT")
print(f"Capital Saved with 5% Hard SL: {closed_losses['saved_with_sl5'].sum():.2f} USDT")
print(f"Percentage of Loss Avoided: {closed_losses['saved_with_sl5'].sum() / abs(closed_losses['profit_abs'].sum()) * 100:.1f}%")

