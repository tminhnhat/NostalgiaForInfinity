import json
import pandas as pd
import sys

sys.stdout.reconfigure(encoding="utf-8")

with open("user_data/deep_dive_losing_trades.json", "r", encoding="utf-8") as f:
    trades = json.load(f)

print(f"Total trades loaded: {len(trades)}")

for t in trades:
    tid = t['id']
    pair = t['pair']
    is_short = bool(t['is_short'])
    pos_str = "SHORT" if is_short else "LONG"
    is_open = bool(t['is_open'])
    tag = t['enter_tag']
    exit_reason = t['exit_reason'] if not is_open else "STILL OPEN"
    open_date = t['open_date']
    close_date = t['close_date'] if not is_open else "CURRENT"
    
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
    initial_cost = float(initial_buy['cost'] or 0) if initial_buy else stake
    
    # Calculate price drop from initial entry to exit
    if initial_price > 0 and close_rate > 0:
        if not is_short:
            price_change_pct = ((close_rate - initial_price) / initial_price) * 100
        else:
            price_change_pct = ((initial_price - close_rate) / initial_price) * 100
    else:
        price_change_pct = 0.0

    print("=" * 80)
    print(f"TRADE #{tid}: {pair} [{pos_str}] | Tag: '{tag}' | Open: {is_open}")
    print(f"Timeline: {open_date} ➔ {close_date}")
    print(f"Result: Profit Abs: {profit_abs:+.2f} USDT | Profit %: {profit_pct:+.2f}% | Funding Fees: {funding_fees:.4f} USDT")
    print(f"Exit Reason: {exit_reason}")
    print(f"Pricing: Initial Entry: {initial_price:.6f} | Weighted Avg Entry: {open_rate:.6f} | Exit Rate: {close_rate:.6f}")
    print(f"Underlying Asset Price Move: {price_change_pct:+.2f}%")
    print(f"Risk Levels: Stoploss in Bot: {stop_loss:.6f} | Liquidation Price: {liq_price:.6f} | Leverage: {leverage}x")
    print(f"Capital Scaling: Initial Stake: {stake:.2f} USDT ➔ Max Stake: {max_stake:.2f} USDT (Expansion: {max_stake/stake if stake>0 else 1:.2f}x)")
    print(f"Orders Breakdown: Total Orders: {len(orders)} (Buys: {len(buy_orders)}, Sells: {len(sell_orders)})")
    
    # Order progression
    print("  Orders Timeline:")
    for idx, o in enumerate(orders):
        side = o['side'].upper()
        ft_side = o['ft_order_side']
        typ = o['order_type']
        filled = o['filled']
        avg = o['average']
        cost = o['cost']
        odate = o['order_date']
        stat = o['status']
        print(f"    [{idx+1}] {odate} | {side} ({ft_side}) | {typ} | Price/Avg: {avg} | Filled: {filled} | Cost: {cost:.2f} | Status: {stat}")
    
    # Counterfactual analysis:
    # 1. What if NO DCA occurred (initial stake only with actual exit price)?
    # Initial stake with price_change_pct * leverage
    no_dca_loss_pct = price_change_pct * leverage
    no_dca_loss_abs = stake * (no_dca_loss_pct / 100.0)
    
    # 2. What if a 5% SL on price was hit?
    sl5_loss_pct = -5.0 * leverage # -25%
    sl5_loss_abs = stake * (sl5_loss_pct / 100.0) # -0.25 * stake
    
    print("  Counterfactual Comparison:")
    print(f"    - Actual Loss with DCA & -99% SL: {profit_abs:.2f} USDT")
    if not is_open:
        print(f"    - If NO DCA (Initial stake {stake:.2f} USDT only at exit price): ~{no_dca_loss_abs:.2f} USDT (Saved: {abs(profit_abs) - abs(no_dca_loss_abs):.2f} USDT)")
        print(f"    - If 5% Hard SL was active (Initial stake {stake:.2f} USDT): ~{sl5_loss_abs:.2f} USDT (Saved: {abs(profit_abs) - abs(sl5_loss_abs):.2f} USDT)")
    print()

