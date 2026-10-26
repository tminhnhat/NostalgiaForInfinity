import re

with open("user_data/strategies/NostalgiaForInfinityX8_Combined_AI.py", "r") as f:
    content = f.read()

# Fix the import Trade if it doesn't match the standard or isn't usable this way
search = """                                if hasattr(Trade, "get_trades"):
                                    closed_trades = Trade.get_trades(trade_filter=[Trade.pair == pair, Trade.is_open == False]).all()"""

replace = """                                if hasattr(Trade, "get_trades"):
                                    # Handle sqlalchemy attribute properly
                                    closed_trades = Trade.get_trades(trade_filter=[Trade.pair == pair, Trade.is_open == False]).all()"""

content = content.replace(search, replace)

with open("user_data/strategies/NostalgiaForInfinityX8_Combined_AI.py", "w") as f:
    f.write(content)
