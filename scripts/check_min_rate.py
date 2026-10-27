# In Freqtrade:
# During backtest, Trade.adjust_min_max_rates(current_rate, current_rate) is called on each candle.
# But if a candle has low lower than current_rate:
# Trade.min_rate is updated with current_rate (which is open or close of the candle, or high/low depending on detail_data).
print("Checking trade rates...")
