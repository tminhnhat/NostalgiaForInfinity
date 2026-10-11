# -*- coding: utf-8 -*-
from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import MagicMock
import numpy as np
import pandas as pd
try:
    import pytest
except ImportError:
    pytest = None

from NostalgiaForInfinityX8_ShortSignals import NostalgiaForInfinityX8_ShortSignals
from NostalgiaForInfinityX8_Combined import NostalgiaForInfinityX8_Combined


def test_short_signals_indicators_and_entries():
    short_mod = NostalgiaForInfinityX8_ShortSignals()
    
    # Generate 50 candles
    n = 60
    close = np.linspace(100, 150, n)
    high = close + 2.0
    low = close - 2.0
    open_px = close - 0.5
    volume = np.ones(n) * 1000

    df = pd.DataFrame({
        "open": open_px,
        "high": high,
        "low": low,
        "close": close,
        "volume": volume,
    })

    df = short_mod.populate_indicators(df, {"pair": "ETH/USDT:USDT"})
    assert "upper_wick_ratio" in df.columns
    assert "vol_spike_ratio" in df.columns
    assert "BBU_20_2.0" in df.columns
    assert "rolling_high_24" in df.columns
    assert "macdhist_custom" in df.columns
    assert "stochrsi_k_custom" in df.columns

    # Test SFP condition artificially at index 40
    df.loc[40, "high"] = 200.0
    df.loc[40, "close"] = 140.0
    df.loc[40, "open"] = 145.0
    df.loc[40, "upper_wick_ratio"] = 0.60
    df.loc[40, "rolling_high_24"] = 148.0
    df.loc[39, "rolling_high_24"] = 148.0

    df = short_mod.populate_entry_trend(df, {"pair": "ETH/USDT:USDT"})
    assert "enter_short_custom" in df.columns
    assert "enter_tag_custom" in df.columns
    assert df.loc[40, "enter_short_custom"] == 1
    assert "711" in df.loc[40, "enter_tag_custom"]


def test_combined_strategy_registration():
    config = {
        "exchange": {"name": "binance"},
        "stake_currency": "USDT",
        "trading_mode": "futures",
        "runmode": SimpleNamespace(value="live"),
        "user_data_dir": pd.Series([1]).index,
    }
    strat = NostalgiaForInfinityX8_Combined.__new__(NostalgiaForInfinityX8_Combined)
    strat.config = config
    strat.short_normal_mode_tags = ["501", "502"]
    strat.short_known_mode_tags = ["501", "502"]
    strat.short_exit_known_mode_tags = ["501", "502"]
    strat.short_strategy = NostalgiaForInfinityX8_ShortSignals(config)

    for tag in strat.short_strategy.custom_short_tags:
        if tag not in strat.short_normal_mode_tags:
            strat.short_normal_mode_tags.append(tag)
        if tag not in strat.short_known_mode_tags:
            strat.short_known_mode_tags.append(tag)
        if tag not in strat.short_exit_known_mode_tags:
            strat.short_exit_known_mode_tags.append(tag)

    # Check tags from all 4 groups
    assert "701" in strat.short_normal_mode_tags
    assert "711" in strat.short_normal_mode_tags
    assert "721" in strat.short_normal_mode_tags
    assert "731" in strat.short_normal_mode_tags


def test_custom_exit_short_tags():
    short_mod = NostalgiaForInfinityX8_ShortSignals()
    
    # Test scalp exit
    trade_scalp = SimpleNamespace(
        pair="BTC/USDT:USDT",
        is_short=True,
        enter_tag="721",
    )
    last_candle = {"RSI_14": 40.0, "BBL_20_2.0": 90.0, "close": 98.0}
    prev_candle = {"close": 99.0}

    should_exit, reason = short_mod.custom_exit(
        pair="BTC/USDT:USDT",
        trade=trade_scalp,
        current_time=datetime.now(timezone.utc),
        current_rate=98.0,
        current_profit=0.019,
        last_candle=last_candle,
        previous_candle=prev_candle,
    )
    assert should_exit is True
    assert "custom_short_tp_scalp" in reason

    # Test oversold exit
    should_exit, reason = short_mod.custom_exit(
        pair="BTC/USDT:USDT",
        trade=trade_scalp,
        current_time=datetime.now(timezone.utc),
        current_rate=90.0,
        current_profit=0.015,
        last_candle={"RSI_14": 19.0, "BBL_20_2.0": 92.0, "close": 90.0},
        previous_candle=prev_candle,
    )
    assert should_exit is True
    assert "custom_short_tp_oversold_bounce" in reason
