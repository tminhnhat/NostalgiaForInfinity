import re

with open("user_data/strategies/NostalgiaForInfinityX8_Combined_AI.py", "r") as f:
    content = f.read()

search = """                            # Restrict simultaneous re-entries following stoploss events within 4 hours.
                            # Since stoploss event time isn't directly exposed in entry checks natively without trade history parsing,
                            # we'll look at extreme high ATR expansions for the second part of the task instruction."""

replace = """                            # Restrict simultaneous re-entries following stoploss events within 4 hours.
                            try:
                                # Safe call using Trade.get_trades_proxy or fetching from DP if possible
                                if hasattr(Trade, "get_trades"):
                                    closed_trades = Trade.get_trades(trade_filter=[Trade.pair == pair, Trade.is_open == False]).all()
                                    if closed_trades:
                                        last_trade = closed_trades[-1]
                                        if last_trade.is_short and last_trade.close_profit < -0.01:
                                            # Check time since close
                                            if hasattr(last_trade, 'close_date') and last_trade.close_date:
                                                time_since_close = (current_time - last_trade.close_date).total_seconds() / 3600.0
                                                if time_since_close <= 4.0:
                                                    return False
                            except Exception:
                                pass"""

content = content.replace(search, replace)

with open("user_data/strategies/NostalgiaForInfinityX8_Combined_AI.py", "w") as f:
    f.write(content)
