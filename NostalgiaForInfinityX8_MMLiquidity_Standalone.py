# -*- coding: utf-8 -*-
"""
NostalgiaForInfinityX8_MMLiquidity_Standalone (v5.0 — MM Liquidity + LightGBM AI Gatekeeper)
Combines v4.0 high-precision Market Maker / Order Flow / Synthetic Liquidation Heatmap signals
(Long 801-803 & Short 851-853) with trained LightGBM AI Gatekeepers (mm_long_gatekeeper_v1.pkl
& mm_short_gatekeeper_v1.pkl) at 6.0x leverage.
"""
from __future__ import annotations

import logging
import pickle
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple

import numpy as np
import pandas as pd
from pandas import DataFrame

from freqtrade.persistence import Trade
from freqtrade.strategy import IStrategy
from NostalgiaForInfinityX8_MMLiquiditySignals import NostalgiaForInfinityX8_MMLiquiditySignals

log = logging.getLogger(__name__)


class NostalgiaForInfinityX8_MMLiquidity_Standalone(IStrategy):
    INTERFACE_VERSION = 3

    timeframe = "5m"
    can_short = True
    startup_candle_count = 300

    stoploss = -0.80
    minimal_roi = {"0": 10.0}
    use_exit_signal = True
    process_only_new_candles = True

    futures_mode_leverage: float = 6.0
    ai_long_threshold: float = 0.78
    ai_short_threshold: float = 0.78

    def __init__(self, config: dict) -> None:
        super().__init__(config)
        self.mm_signals = NostalgiaForInfinityX8_MMLiquiditySignals(config)
        self.long_ai = self._load_model("user_data/models/mm_long_gatekeeper_v1.pkl")
        self.short_ai = self._load_model("user_data/models/mm_short_gatekeeper_v1.pkl")

    @staticmethod
    def _load_model(path_str: str) -> Optional[dict]:
        p = Path(path_str)
        if not p.exists():
            log.warning("AI model not found: %s", p)
            return None
        with open(p, "rb") as f:
            return pickle.load(f)

    def informative_pairs(self) -> List[Tuple[str, str]]:
        pairs = self.dp.current_whitelist() if self.dp else []
        inf: List[Tuple[str, str]] = []
        for p in pairs:
            inf.append((p, "15m"))
            inf.append((p, "1h"))
        if any(":USDT" in p for p in pairs):
            inf.append(("BTC/USDT:USDT", "5m"))
        else:
            inf.append(("BTC/USDT", "5m"))
        return list(dict.fromkeys(inf))

    def leverage(
        self,
        pair: str,
        current_time: datetime,
        current_rate: float,
        proposed_leverage: float,
        max_leverage: float,
        entry_tag: Optional[str],
        side: str,
        **kwargs,
    ) -> float:
        return min(float(self.futures_mode_leverage), float(max_leverage))

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        df = self.mm_signals.populate_indicators(dataframe, metadata, dp=self.dp)
        eps = 1e-10
        # Add derived normalized features expected by LightGBM Gatekeepers
        vol_ma_48 = df["volume"].rolling(48, min_periods=10).mean().clip(lower=eps)
        df["mm_log_qvol_1h"] = np.log1p(df["mm_quote_vol_1h"].clip(lower=0.0))
        df["mm_bar_delta_norm"] = df["mm_bar_delta"] / vol_ma_48
        df["mm_cvd_12_norm"] = df["mm_cvd_12"] / (vol_ma_48 * 12.0)
        df["mm_cvd_48_norm"] = df["mm_cvd_48"] / (vol_ma_48 * 48.0)
        df["mm_cvd_div_long"] = (df["mm_cvd_48"] - df["mm_prev_cvd_low_48"]) / (vol_ma_48 * 48.0)
        df["mm_cvd_div_short"] = (df["mm_prev_cvd_high_48"] - df["mm_cvd_48"]) / (vol_ma_48 * 48.0)
        df["mm_dist_vwap_24h"] = (df["close"] - df["mm_vwap_24h"]) / df["mm_vwap_24h"].clip(lower=eps)
        df["mm_dist_swing_low_24h"] = (df["close"] - df["mm_swing_low_24h"]) / df["close"].clip(lower=eps)
        df["mm_dist_swing_high_24h"] = (df["mm_swing_high_24h"] - df["close"]) / df["close"].clip(lower=eps)
        df["mm_dist_ema200_1h"] = (df["close"] - df["mm_ema200_1h"]) / df["mm_ema200_1h"].clip(lower=eps)
        return df

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        df = self.mm_signals.populate_entry_trend(dataframe, metadata)

        # Apply LightGBM AI Gatekeeper to candidate Long rows
        if self.long_ai is not None:
            l_idx = df.index[df["enter_long"] == 1]
            if len(l_idx) > 0:
                feats = self.long_ai["features"]
                probs = self.long_ai["model"].predict_proba(df.loc[l_idx, feats])[:, 1]
                veto = l_idx[probs < self.ai_long_threshold]
                keep = l_idx[probs >= self.ai_long_threshold]
                df.loc[veto, "enter_long"] = 0
                df.loc[veto, "enter_tag"] = ""
                df.loc[keep, "enter_tag"] = df.loc[keep, "enter_tag"].astype(str) + "_AI"

        # Apply LightGBM AI Gatekeeper to candidate Short rows
        if self.short_ai is not None:
            s_idx = df.index[df["enter_short"] == 1]
            if len(s_idx) > 0:
                feats = self.short_ai["features"]
                probs = self.short_ai["model"].predict_proba(df.loc[s_idx, feats])[:, 1]
                veto = s_idx[probs < self.ai_short_threshold]
                keep = s_idx[probs >= self.ai_short_threshold]
                df.loc[veto, "enter_short"] = 0
                df.loc[veto, "enter_tag"] = ""
                df.loc[keep, "enter_tag"] = df.loc[keep, "enter_tag"].astype(str) + "_AI"

        return df

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe["exit_long"] = 0
        dataframe["exit_short"] = 0
        return dataframe

    def custom_exit(
        self,
        pair: str,
        trade: Trade,
        current_time: datetime,
        current_rate: float,
        current_profit: float,
        **kwargs,
    ) -> Optional[str]:
        orig_tag = trade.enter_tag or "mm"
        leverage = float(trade.leverage or self.futures_mode_leverage)
        open_rate = float(trade.open_rate)
        dur_hours = (current_time - trade.open_date_utc).total_seconds() / 3600.0

        if trade.is_short:
            best_rate = float(trade.min_rate) if trade.min_rate is not None else open_rate
            mfe_roe = (open_rate - best_rate) / open_rate * leverage
        else:
            best_rate = float(trade.max_rate) if trade.max_rate is not None else open_rate
            mfe_roe = (best_rate - open_rate) / open_rate * leverage

        # Adaptive Trailing Profit Lock (calibrated for AvgWin >= +8% ROE at 6x)
        if mfe_roe >= 0.30 and current_profit <= mfe_roe - 0.06 and current_profit >= 0.22:
            return f"exit_mm_trail_t4 ({orig_tag})"
        if mfe_roe >= 0.20 and current_profit <= mfe_roe - 0.05 and current_profit >= 0.14:
            return f"exit_mm_trail_t3 ({orig_tag})"
        if mfe_roe >= 0.13 and current_profit <= 0.095 and current_profit >= 0.075:
            return f"exit_mm_trail_t2 ({orig_tag})"
        if mfe_roe >= 0.088 and current_profit <= 0.062 and current_profit >= 0.052:
            return f"exit_mm_trail_t1 ({orig_tag})"
        if mfe_roe >= 0.068 and current_profit <= 0.038 and current_profit >= 0.025:
            return f"exit_mm_mfe_protect ({orig_tag})"

        # Mean-Reversion VWAP Harvest
        if current_profit >= 0.078 and self.dp is not None:
            df_pair, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
            if len(df_pair) > 0:
                rows = df_pair.loc[df_pair["date"] <= current_time]
                if len(rows) > 0:
                    vwap_4h = rows.iloc[-1].get("mm_vwap_4h", np.nan)
                    if vwap_4h is not None and not np.isnan(float(vwap_4h)):
                        if (not trade.is_short) and current_rate >= float(vwap_4h):
                            return f"exit_mm_vwap_reversion ({orig_tag})"
                        if trade.is_short and current_rate <= float(vwap_4h):
                            return f"exit_mm_vwap_reversion ({orig_tag})"

        # Structural Early Cut for Short
        if trade.is_short and current_profit <= -0.20 and self.dp is not None:
            df_pair, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
            if len(df_pair) > 0:
                rows = df_pair.loc[df_pair["date"] <= current_time]
                if len(rows) > 0:
                    e200 = rows.iloc[-1].get("mm_ema200_1h", np.nan)
                    if e200 is not None and not np.isnan(float(e200)) and current_rate > float(e200) * 1.005:
                        return f"exit_mm_short_struct_cut ({orig_tag})"

        if trade.is_short:
            if current_profit <= -0.36:
                return f"exit_mm_short_hard_sl ({orig_tag})"
            if dur_hours >= 72.0:
                return f"exit_mm_short_max_72h ({orig_tag})"
        else:
            if current_profit <= -0.45:
                return f"exit_mm_long_hard_sl ({orig_tag})"
            if dur_hours >= 144.0:
                return f"exit_mm_long_max_144h ({orig_tag})"

        return None
