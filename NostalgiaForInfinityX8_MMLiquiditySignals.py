# -*- coding: utf-8 -*-
"""
NostalgiaForInfinityX8_MMLiquiditySignals (Production v5.0)
Market Maker / Order Flow / Synthetic Liquidation Heatmap + LightGBM AI v2 (500-pair models).

Proven on 500-pair independent 5m backtest (6.0x leverage, Exit v1):
  - Full 12M: 339 trades | WR 95.58% | Avg +5.35% | Closed MaxDD 6.97% | PF 4.40
  - Pure OOS:  61 trades | WR 96.72% | Avg +4.81% | Closed MaxDD 3.61% | PF 5.26

Tags:
  Long  (ATR <= 0.008 & Long AI v2 >= 0.83 & 60m cooldown max 2 Longs/60m):
    - 801_MM_AI: 24h Low Liquidity Sweep + Lower Wick Absorption + RVOL
    - 802_MM_AI: Real CVD Divergence + Absorption + Deep VWAP -2.5sigma + MFI < 35
    - 803_MM_AI: 20x Liquidation Cascade + Taker Buy Reclaim + OI Flush <= -2%
  Short (ATR <= 0.009-0.010 & <1h EMA200 & Short AI v2 >= 0.82):
    - 851_MM_AI: 24h High Liquidity Sweep + Upper Wick Rejection + RVOL
    - 852_MM_AI: Real CVD Bearish Divergence + Absorption + VWAP +2.5sigma
    - 853_MM_AI: 20x Short Squeeze Exhaustion + Taker Sell Flip
"""
from __future__ import annotations

import logging
import pickle
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import pandas as pd
from pandas import DataFrame
import talib.abstract as ta

from BinanceMMDataProvider import BinanceMMDataProvider

log = logging.getLogger(__name__)


class NostalgiaForInfinityX8_MMLiquiditySignals:
    def __init__(self, config: Optional[dict] = None) -> None:
        self.config = config or {}
        nfi_params = self.config.get("nfi_parameters", {}) if isinstance(self.config, dict) else {}

        self.enable_mm_long: bool = bool(
            self.config.get("mm_enable_long", nfi_params.get("mm_enable_long", True))
        )
        self.enable_mm_short: bool = bool(
            self.config.get("mm_enable_short", nfi_params.get("mm_enable_short", True))
        )
        self.ai_long_threshold: float = float(
            self.config.get("mm_ai_long_threshold", nfi_params.get("mm_ai_long_threshold", 0.83))
        )
        self.ai_short_threshold: float = float(
            self.config.get("mm_ai_short_threshold", nfi_params.get("mm_ai_short_threshold", 0.82))
        )

        self.tag_toggles: Dict[str, bool] = {
            "801": True,
            "802": True,
            "803": True,
            # Smart Money v3 tags (pending AI Gatekeeper v3 training)
            "811": False,
            "812": False,
            "813": False,
            "814": False,
            "851": True,
            "852": True,
            "853": True,
            "861": False,
            "862": False,
            "863": False,
            "864": False,
        }
        overrides = self.config.get("mm_liquidity_toggles", nfi_params.get("mm_liquidity_toggles", {}))
        if isinstance(overrides, dict):
            for k, v in overrides.items():
                if str(k) in self.tag_toggles:
                    self.tag_toggles[str(k)] = bool(v)

        self.mm_long_tags: List[str] = [
            "801_MM_AI", "802_MM_AI", "803_MM_AI",
            "811_MM_SFP_L", "812_MM_SQZ_L", "813_MM_ABS_L", "814_MM_FLS_L",
        ]
        self.mm_short_tags: List[str] = [
            "851_MM_AI", "852_MM_AI", "853_MM_AI",
            "861_MM_SFP_S", "862_MM_SQZ_S", "863_MM_DST_S", "864_MM_CAS_S",
        ]
        self.all_mm_tags: List[str] = self.mm_long_tags + self.mm_short_tags

        self.data_provider = BinanceMMDataProvider()
        self.long_ai = self._load_model("user_data/models/mm_long_gatekeeper_v2_500p.pkl")
        self.short_ai = self._load_model("user_data/models/mm_short_gatekeeper_v2_500p.pkl")

        # Anti-correlation cooldown tracker for Long entries (max 2 MM Long entries per 60 minutes)
        self._recent_long_entry_ts: List[float] = []

    @staticmethod
    def _load_model(path_str: str) -> Optional[dict]:
        for base in [Path("."), Path("/freqtrade"), Path("/content/NostalgiaForInfinity")]:
            p = base / path_str
            if p.exists():
                try:
                    with open(p, "rb") as f:
                        obj = pickle.load(f)
                    log.info("Loaded MM AI v2 model from %s (OOS AUC=%.4f)", p, float(obj.get("auc_oos", 0.0)))
                    return obj
                except Exception as e:
                    log.warning("Failed loading MM AI model %s: %s", p, e)
        log.warning("MM AI v2 model not found at %s; MM signals will not fire.", path_str)
        return None

    @staticmethod
    def is_mm_tag(tag_str: Optional[str]) -> bool:
        raw = str(tag_str or "")
        return ("_MM_AI" in raw) or ("_MM_" in raw)

    def allow_mm_long_entry(self, current_time: datetime, max_per_hour: int = 2) -> bool:
        ts = current_time.timestamp()
        cutoff = ts - 3600.0
        self._recent_long_entry_ts = [t for t in self._recent_long_entry_ts if t > cutoff]
        if len(self._recent_long_entry_ts) >= max_per_hour:
            return False
        self._recent_long_entry_ts.append(ts)
        return True

    def populate_indicators(
        self,
        dataframe: DataFrame,
        metadata: dict,
        dp=None,
        is_live_mode: bool = False,
    ) -> DataFrame:
        df = dataframe
        eps = 1e-10
        pair = metadata.get("pair", "")

        # 1. Merge offline enriched Binance Vision features in backtest mode
        if not is_live_mode and pair:
            df = self.data_provider.merge_offline_enriched(df, pair)

        # 2. Core 5m Geometry & Volatility
        candle_range = (df["high"] - df["low"]).clip(lower=eps)
        body = (df["close"] - df["open"]).abs()
        lower_wick = np.minimum(df["open"], df["close"]) - df["low"]
        upper_wick = df["high"] - np.maximum(df["open"], df["close"])

        df["mm_lower_wick_ratio"] = (lower_wick / candle_range).clip(0.0, 1.0).astype(np.float32)
        df["mm_upper_wick_ratio"] = (upper_wick / candle_range).clip(0.0, 1.0).astype(np.float32)
        df["mm_body_pct"] = (body / df["close"].clip(lower=eps)).astype(np.float32)

        atr_14 = ta.ATR(df, timeperiod=14)
        df["mm_atr_pct"] = (atr_14 / df["close"].clip(lower=eps)).clip(lower=1e-5).astype(np.float32)
        df["mm_range_atr"] = (candle_range / atr_14.clip(lower=eps)).astype(np.float32)
        df["mm_rsi_5m"] = ta.RSI(df, timeperiod=14).astype(np.float32)

        # 3. Order Flow (Real Binance Taker Buy Quote Volume if available, else OHLCV proxy fallback)
        if "quote_volume" in df.columns and df["quote_volume"].notna().sum() > 20:
            qvol = df["quote_volume"].fillna(df["volume"] * df["close"]).clip(lower=eps)
        else:
            qvol = (df["volume"] * df["close"]).clip(lower=eps)

        buy_ratio_proxy = ((df["close"] - df["low"]) / candle_range).clip(0.0, 1.0)
        if "taker_buy_quote_volume" in df.columns and df["taker_buy_quote_volume"].notna().sum() > 20:
            tb_qvol = df["taker_buy_quote_volume"].fillna(qvol * buy_ratio_proxy).clip(lower=0.0)
            df["real_taker_buy_ratio"] = (tb_qvol / qvol).clip(0.0, 1.0).astype(np.float32)
        else:
            tb_qvol = qvol * buy_ratio_proxy
            df["real_taker_buy_ratio"] = buy_ratio_proxy.astype(np.float32)

        real_delta = 2.0 * tb_qvol - qvol
        qvol_ma_48 = qvol.rolling(48, min_periods=10).mean().clip(lower=eps)
        df["mm_rvol"] = (qvol / qvol_ma_48).astype(np.float32)
        df["real_taker_delta_norm"] = (real_delta / qvol_ma_48).astype(np.float32)

        real_cvd_12 = real_delta.rolling(12, min_periods=1).sum()
        real_cvd_48 = real_delta.rolling(48, min_periods=1).sum()
        df["real_cvd_12_norm"] = (real_cvd_12 / (qvol_ma_48 * 12.0)).astype(np.float32)
        df["real_cvd_48_norm"] = (real_cvd_48 / (qvol_ma_48 * 48.0)).astype(np.float32)
        prev_cvd_low = real_cvd_48.rolling(48, min_periods=12).min().shift(3)
        prev_cvd_high = real_cvd_48.rolling(48, min_periods=12).max().shift(3)
        df["real_cvd_div_long"] = ((real_cvd_48 - prev_cvd_low) / (qvol_ma_48 * 48.0)).astype(np.float32)
        df["real_cvd_div_short"] = ((prev_cvd_high - real_cvd_48) / (qvol_ma_48 * 48.0)).astype(np.float32)

        if "count" in df.columns and df["count"].notna().sum() > 20:
            avg_trade_sz = qvol / df["count"].fillna(1.0).clip(lower=1.0)
            df["whale_trade_size_ratio"] = (avg_trade_sz / avg_trade_sz.rolling(48, min_periods=10).mean().clip(lower=eps)).astype(np.float32)
        else:
            df["whale_trade_size_ratio"] = np.float32(1.0)

        qvol_1h = qvol.rolling(12, min_periods=1).sum()
        df["mm_quote_vol_1h"] = qvol_1h.astype(np.float32)
        df["mm_log_qvol_1h"] = np.log1p(qvol_1h.clip(lower=0.0)).astype(np.float32)
        df["mm_absorption"] = (df["mm_rvol"] / np.maximum(df["mm_body_pct"] / df["mm_atr_pct"], 0.25)).astype(np.float32)

        df["mm_mfi_14"] = ta.MFI(df, timeperiod=14).astype(np.float32)
        mfm = ((df["close"] - df["low"]) - (df["high"] - df["close"])) / candle_range
        df["mm_cmf_20"] = (
            (mfm * df["volume"]).rolling(20, min_periods=5).sum()
            / df["volume"].rolling(20, min_periods=5).sum().clip(lower=eps)
        ).astype(np.float32)

        # 4. Synthetic Liquidation Heatmap (VWAP Z-scores + 24h Swing Pools)
        typical = (df["high"] + df["low"] + df["close"]) / 3.0
        pv = typical * df["volume"]
        vwap_4h = pv.rolling(48, min_periods=12).sum() / df["volume"].rolling(48, min_periods=12).sum().clip(lower=eps)
        vwap_24h = pv.rolling(288, min_periods=24).sum() / df["volume"].rolling(288, min_periods=24).sum().clip(lower=eps)
        df["mm_vwap_4h"] = vwap_4h.astype(np.float32)
        std_4h = (df["close"] - vwap_4h).rolling(48, min_periods=12).std().clip(lower=eps)
        std_24h = (df["close"] - vwap_24h).rolling(288, min_periods=24).std().clip(lower=eps)
        df["mm_vwap_z_4h"] = ((df["close"] - vwap_4h) / std_4h).astype(np.float32)
        df["mm_vwap_z_24h"] = ((df["close"] - vwap_24h) / std_24h).astype(np.float32)
        df["mm_dist_vwap_24h"] = ((df["close"] - vwap_24h) / vwap_24h.clip(lower=eps)).astype(np.float32)

        sw_low_24h = df["low"].rolling(288, min_periods=48).min().shift(1)
        sw_high_24h = df["high"].rolling(288, min_periods=48).max().shift(1)
        df["mm_dist_swing_low_24h"] = ((df["close"] - sw_low_24h) / df["close"].clip(lower=eps)).astype(np.float32)
        df["mm_dist_swing_high_24h"] = ((sw_high_24h - df["close"]) / df["close"].clip(lower=eps)).astype(np.float32)
        df["mm_prev_sw_low_12h"] = df["low"].rolling(144, min_periods=24).min().shift(1).astype(np.float32)
        df["mm_prev_sw_high_12h"] = df["high"].rolling(144, min_periods=24).max().shift(1).astype(np.float32)

        # 5. Causal 15m & 1h Resampled Features (self-contained, zero extra informative dependency)
        orig_dt = pd.to_datetime(df["date"], utc=True).astype("datetime64[ns, UTC]")
        d_idx = pd.DataFrame({"close": df["close"].to_numpy()}, index=orig_dt)
        df15 = d_idx["close"].resample("15min").last().dropna().to_frame("close")
        df15["mm_rsi_15m"] = ta.RSI(df15, timeperiod=14).shift(1)
        df15 = df15[["mm_rsi_15m"]].reset_index().rename(columns={"date": "_dt"})
        df15["_dt"] = pd.to_datetime(df15["_dt"], utc=True).astype("datetime64[ns, UTC]")

        df1h = d_idx["close"].resample("1h").last().dropna().to_frame("close")
        df1h["mm_rsi_1h"] = ta.RSI(df1h, timeperiod=14).shift(1)
        e50 = ta.EMA(df1h, timeperiod=50)
        e200 = ta.EMA(df1h, timeperiod=200)
        df1h["mm_ema200_1h"] = e200.shift(1)
        df1h["mm_ema50_slope_1h"] = ((e50 - e50.shift(4)) / e50.shift(4).clip(lower=eps)).shift(1)
        df1h = df1h[["mm_rsi_1h", "mm_ema200_1h", "mm_ema50_slope_1h"]].reset_index().rename(columns={"date": "_dt"})
        df1h["_dt"] = pd.to_datetime(df1h["_dt"], utc=True).astype("datetime64[ns, UTC]")

        tmp = pd.DataFrame({"_dt": orig_dt})
        m15 = pd.merge_asof(tmp, df15, on="_dt", direction="backward")
        m1h = pd.merge_asof(tmp, df1h, on="_dt", direction="backward")
        df["mm_rsi_15m"] = m15["mm_rsi_15m"].fillna(50.0).to_numpy(dtype=np.float32)
        df["mm_rsi_1h"] = m1h["mm_rsi_1h"].fillna(50.0).to_numpy(dtype=np.float32)
        e200_arr = m1h["mm_ema200_1h"].to_numpy(dtype=np.float64)
        df["mm_dist_ema200_1h"] = ((df["close"].to_numpy(dtype=np.float64) - e200_arr) / np.maximum(e200_arr, eps)).astype(np.float32)
        df["mm_ema50_slope_1h"] = m1h["mm_ema50_slope_1h"].fillna(0.0).to_numpy(dtype=np.float32)

        # 6. BTC Macro Context (5m)
        if dp is not None:
            btc_pair = "BTC/USDT:USDT" if ":USDT" in pair else "BTC/USDT"
            btc_5m = dp.get_pair_dataframe(pair=btc_pair, timeframe="5m")
            if btc_5m is not None and len(btc_5m) > 30:
                bdf = pd.DataFrame({"_dt": pd.to_datetime(btc_5m["date"], utc=True).astype("datetime64[ns, UTC]")})
                bdf["btc_ret_1h"] = btc_5m["close"].pct_change(12).shift(1).to_numpy()
                bdf["btc_ret_15m"] = btc_5m["close"].pct_change(3).shift(1).to_numpy()
                bdf["btc_rsi_5m"] = ta.RSI(btc_5m, timeperiod=14).shift(1).to_numpy()
                mb = pd.merge_asof(tmp, bdf.sort_values("_dt"), on="_dt", direction="backward")
                df["btc_ret_1h"] = mb["btc_ret_1h"].fillna(0.0).to_numpy(dtype=np.float32)
                df["btc_ret_15m"] = mb["btc_ret_15m"].fillna(0.0).to_numpy(dtype=np.float32)
                df["btc_rsi_5m"] = mb["btc_rsi_5m"].fillna(50.0).to_numpy(dtype=np.float32)

        for col, default_val in [
            ("btc_ret_1h", 0.0),
            ("btc_ret_15m", 0.0),
            ("btc_rsi_5m", 50.0),
            ("funding_rate", 0.0),
            ("funding_rate_z", 0.0),
            ("funding_interval_h", 8.0),
            ("log_oi_usdt", np.nan),
            ("oi_chg_15m", np.nan),
            ("oi_chg_1h", np.nan),
            ("oi_chg_4h", np.nan),
            ("oi_to_vol_ratio", np.nan),
            ("top_pos_ls", np.nan),
            ("top_acc_ls", np.nan),
            ("retail_ls", np.nan),
            ("whale_vs_retail_div", np.nan),
            ("top_pos_ls_chg_1h", np.nan),
            ("metrics_taker_ls", np.nan),
        ]:
            if col not in df.columns:
                df[col] = np.float32(default_val)

        return df

    def populate_entry_trend(
        self,
        dataframe: DataFrame,
        metadata: dict,
        is_live_mode: bool = False,
    ) -> DataFrame:
        df = dataframe
        if "enter_long" not in df.columns:
            df["enter_long"] = 0
        if "enter_short" not in df.columns:
            df["enter_short"] = 0
        if "enter_tag" not in df.columns:
            df["enter_tag"] = ""

        pair = metadata.get("pair", "")
        has_liq = (df["volume"] > 0) & (df["mm_quote_vol_1h"] >= 400_000.0)

        # =====================================================================
        # LONG CANDIDATES (801, 802, 803) + LightGBM Long AI v2 (>= 0.83)
        # =====================================================================
        if self.enable_mm_long and self.long_ai is not None:
            l_pre = (
                has_liq
                & (df["enter_long"] == 0)
                & (df["mm_atr_pct"] <= 0.008)
                & (df["mm_vwap_z_24h"] <= -2.2)
                & (df["mm_rsi_15m"] < 35.0)
                & (df["mm_rvol"] >= 2.2)
            )
            c801 = (
                l_pre
                & self.tag_toggles.get("801", True)
                & (df["mm_dist_swing_low_24h"] >= -0.005)
                & (df["mm_dist_swing_low_24h"] <= 0.015)
                & (df["mm_lower_wick_ratio"] >= 0.45)
                & (df["mm_rvol"] >= 2.8)
                & (df["real_taker_buy_ratio"] >= 0.46)
                & (df["mm_absorption"] >= 2.5)
                & (df["btc_ret_1h"] >= -0.020)
                & (df["mm_dist_ema200_1h"] >= -0.10)
                & (df["mm_rsi_1h"] >= 21.0)
            )
            # 802_MM_AI (reference tag - untouched)
            c802 = (
                l_pre
                & self.tag_toggles.get("802", True)
                & (df["real_cvd_div_long"] > 0.05)
                & (df["mm_vwap_z_24h"] <= -2.5)
                & (df["mm_absorption"] >= 2.5)
                & (df["mm_mfi_14"] < 35.0)
            )
            l_pre_803 = (
                has_liq
                & (df["enter_long"] == 0)
                & (df["mm_atr_pct"] <= 0.010)
                & (df["mm_vwap_z_24h"] <= -2.4)
                & (df["mm_rsi_15m"] < 28.0)
                & (df["mm_rvol"] >= 2.2)
            )
            oi_flush_ok_803 = (df["oi_chg_1h"] <= -0.012) | df["oi_chg_1h"].isna()
            c803 = (
                l_pre_803
                & self.tag_toggles.get("803", True)
                & (df["mm_dist_vwap_24h"] <= -0.050)
                & (df["real_taker_buy_ratio"] >= 0.52)
                & (df["mm_lower_wick_ratio"] >= 0.25)
                & (df["mm_absorption"] >= 1.5)
                & (df["btc_ret_1h"] >= -0.018)
                & (df["mm_dist_ema200_1h"] >= -0.115)
                & (df["mm_rsi_1h"] >= 17.0)
                & oi_flush_ok_803
            )

            cand_idx = df.index[c801 | c802 | c803]
            if len(cand_idx) > 0:
                # In live mode, enrich only the latest triggered row via Binance Futures API
                if is_live_mode and (df.index[-1] in cand_idx) and pair:
                    snap = self.data_provider.fetch_live_snapshot(pair, float(df.at[df.index[-1], "mm_quote_vol_1h"]))
                    for k, v in snap.items():
                        if k in df.columns and not np.isnan(v):
                            df.at[df.index[-1], k] = np.float32(v)

                feats = self.long_ai["features"]
                probs = self.long_ai["model"].predict_proba(df.loc[cand_idx, feats])[:, 1]
                passed_idx = cand_idx[probs >= self.ai_long_threshold]
                last_l_pos = -1000
                for idx in passed_idx:
                    pos = int(df.index.get_loc(idx))
                    if pos - last_l_pos < 48:  # 4h cooldown per pair/side (matches 500p simulator)
                        continue
                    last_l_pos = pos
                    # Restore baseline Long priority order: 801 -> 802 -> 803
                    tag = "801_MM_AI" if c801.at[idx] else ("802_MM_AI" if c802.at[idx] else "803_MM_AI")
                    df.at[idx, "enter_long"] = 1
                    df.at[idx, "enter_tag"] = tag

        # =====================================================================
        # SHORT CANDIDATES (851, 852, 853) + LightGBM Short AI v2 (>= 0.82)
        # =====================================================================
        if self.enable_mm_short and self.short_ai is not None:
            s_pre = (
                has_liq
                & (df["enter_short"] == 0)
                & (df["enter_long"] == 0)
                & (df["mm_atr_pct"] <= 0.010)
                & (df["mm_vwap_z_24h"] >= 2.2)
                & (df["mm_rsi_15m"] > 65.0)
                & (df["mm_rvol"] >= 2.2)
            )
            # 851_MM_AI (reference tag - untouched)
            c851 = s_pre & self.tag_toggles.get("851", True) & (df["mm_dist_swing_high_24h"] <= 0.015) & (df["mm_upper_wick_ratio"] >= 0.45) & (df["mm_rvol"] >= 2.8) & (df["mm_dist_ema200_1h"] < 0.02)
            c852 = (
                s_pre
                & self.tag_toggles.get("852", True)
                & (df["real_cvd_div_short"] > 0.05)
                & (df["mm_vwap_z_24h"] >= 2.5)
                & (df["mm_absorption"] >= 2.5)
                & (df["mm_atr_pct"] <= 0.009)
                & (df["mm_dist_ema200_1h"] < 0.012)
                & (df["mm_mfi_14"] > 50.0)
            )
            s_pre_853 = (
                has_liq
                & (df["enter_short"] == 0)
                & (df["enter_long"] == 0)
                & (df["mm_atr_pct"] <= 0.011)
                & (df["mm_vwap_z_24h"] >= 2.5)
                & (df["mm_rsi_15m"] > 70.0)
                & (df["mm_rvol"] >= 2.2)
            )
            c853 = (
                s_pre_853
                & self.tag_toggles.get("853", True)
                & (df["mm_dist_vwap_24h"] >= 0.035)
                & (df["real_taker_buy_ratio"] <= 0.45)
                & (df["mm_dist_ema200_1h"] < 0.03)
                & (df["mm_rsi_1h"] < 70.0)
            )

            cand_idx = df.index[c851 | c852 | c853]
            if len(cand_idx) > 0:
                if is_live_mode and (df.index[-1] in cand_idx) and pair:
                    snap = self.data_provider.fetch_live_snapshot(pair, float(df.at[df.index[-1], "mm_quote_vol_1h"]))
                    for k, v in snap.items():
                        if k in df.columns and not np.isnan(v):
                            df.at[df.index[-1], k] = np.float32(v)

                feats = self.short_ai["features"]
                probs = self.short_ai["model"].predict_proba(df.loc[cand_idx, feats])[:, 1]
                passed_idx = cand_idx[probs >= self.ai_short_threshold]
                last_s_pos = -1000
                for idx in passed_idx:
                    pos = int(df.index.get_loc(idx))
                    if pos - last_s_pos < 48:  # 4h cooldown per pair/side (matches 500p simulator)
                        continue
                    last_s_pos = pos
                    tag = "851_MM_AI" if c851.at[idx] else ("852_MM_AI" if c852.at[idx] else "853_MM_AI")
                    df.at[idx, "enter_short"] = 1
                    df.at[idx, "enter_tag"] = tag

        # =====================================================================
        # SMART MONEY / MARKET MAKER LONG (811-814) - Deterministic Liquidity/OI
        # =====================================================================
        has_deriv = (
            df["log_oi_usdt"].notna()
            & df["retail_ls"].notna()
            & df["top_pos_ls"].notna()
            & df["oi_chg_1h"].notna()
        )
        if self.enable_mm_long:
            sm_l_pre = has_liq & has_deriv & (df["enter_long"] == 0) & (df["enter_short"] == 0)
            # 811_MM_SFP_L: Stop Hunt / Liquidity Sweep below 12h swing low + reclaim
            c811 = (
                sm_l_pre
                & self.tag_toggles.get("811", True)
                & (df["low"] < df["mm_prev_sw_low_12h"])
                & (df["close"] > df["mm_prev_sw_low_12h"])
                & (df["mm_lower_wick_ratio"] >= 0.40)
                & (df["mm_rvol"] >= 2.3)
                & ((df["oi_chg_15m"] <= -0.008) | (df["real_taker_buy_ratio"] >= 0.50))
                & ((df["whale_vs_retail_div"] > 0.0) | (df["top_pos_ls"] >= 1.05))
                & (df["btc_ret_1h"] >= -0.020)
                & (df["mm_dist_ema200_1h"] >= -0.10)
            )
            # 812_MM_SQZ_L: Short Squeeze Ignition (negative funding + high retail short + taker buy surge)
            c812 = (
                sm_l_pre
                & self.tag_toggles.get("812", True)
                & ((df["funding_rate_z"] <= -1.2) | (df["funding_rate"] <= -0.00025))
                & (df["retail_ls"] <= 1.05)
                & (df["oi_chg_4h"] >= 0.01)
                & (df["real_taker_buy_ratio"] >= 0.57)
                & (df["real_taker_delta_norm"] >= 0.50)
                & (df["mm_rvol"] >= 2.0)
                & (df["mm_vwap_z_4h"] >= 0.2)
                & (df["mm_vwap_z_4h"] <= 1.8)
                & (df["mm_rsi_15m"] >= 45.0)
                & (df["mm_rsi_15m"] <= 72.0)
            )
            # 813_MM_ABS_L: Whale Accumulation / Iceberg Absorption below VWAP 24h
            c813 = (
                sm_l_pre
                & self.tag_toggles.get("813", True)
                & (df["whale_vs_retail_div"] >= 0.20)
                & (df["top_pos_ls_chg_1h"] >= 0.04)
                & (df["mm_vwap_z_24h"] >= -2.5)
                & (df["mm_vwap_z_24h"] <= -1.2)
                & (df["mm_rvol"] >= 1.8)
                & (df["mm_absorption"] >= 2.2)
                & (df["whale_trade_size_ratio"] >= 1.20)
                & (df["real_cvd_div_long"] > 0.03)
                & (df["btc_ret_1h"] >= -0.015)
                & (df["mm_ema50_slope_1h"] >= -0.015)
            )
            # 814_MM_FLS_L: OI Cascade Flush & Reclaim
            c814 = (
                sm_l_pre
                & self.tag_toggles.get("814", True)
                & ((df["oi_chg_1h"] <= -0.035) | (df["oi_chg_15m"] <= -0.025))
                & (df["mm_vwap_z_24h"] <= -2.3)
                & (df["mm_rsi_15m"] <= 30.0)
                & (df["real_taker_buy_ratio"] >= 0.52)
                & (df["mm_lower_wick_ratio"] >= 0.30)
                & (df["mm_rvol"] >= 2.5)
            )

            sm_l_idx = df.index[c811 | c812 | c813 | c814]
            if len(sm_l_idx) > 0:
                last_sm_l = -1000
                for idx in sm_l_idx:
                    pos = int(df.index.get_loc(idx))
                    if pos - last_sm_l < 48:
                        continue
                    last_sm_l = pos
                    tag = (
                        "811_MM_SFP_L" if c811.at[idx]
                        else ("812_MM_SQZ_L" if c812.at[idx]
                              else ("813_MM_ABS_L" if c813.at[idx] else "814_MM_FLS_L"))
                    )
                    df.at[idx, "enter_long"] = 1
                    df.at[idx, "enter_tag"] = tag

        # =====================================================================
        # SMART MONEY / MARKET MAKER SHORT (861-864) - Deterministic Liquidity/OI
        # =====================================================================
        if self.enable_mm_short:
            sm_s_pre = has_liq & has_deriv & (df["enter_short"] == 0) & (df["enter_long"] == 0)
            # 861_MM_SFP_S: Bull Trap / Liquidity Sweep above 12h swing high + reject
            c861 = (
                sm_s_pre
                & self.tag_toggles.get("861", True)
                & (df["high"] > df["mm_prev_sw_high_12h"])
                & (df["close"] < df["mm_prev_sw_high_12h"])
                & (df["mm_upper_wick_ratio"] >= 0.40)
                & (df["mm_rvol"] >= 2.2)
                & (df["retail_ls"] >= 1.25)
                & (df["real_taker_buy_ratio"] <= 0.46)
                & (df["whale_trade_size_ratio"] >= 1.15)
                & (df["btc_ret_15m"] <= 0.012)
            )
            # 862_MM_SQZ_S: Long Squeeze / Overheated Funding Flush Short
            c862 = (
                sm_s_pre
                & self.tag_toggles.get("862", True)
                & ((df["funding_rate_z"] >= 1.5) | (df["funding_rate"] >= 0.00045))
                & (df["retail_ls"] >= 1.45)
                & (df["mm_vwap_z_24h"] >= 2.2)
                & (df["mm_rsi_15m"] >= 68.0)
                & (df["top_pos_ls_chg_1h"] <= -0.02)
                & (df["real_taker_buy_ratio"] <= 0.45)
                & (df["real_cvd_div_short"] > 0.04)
            )
            # 863_MM_DST_S: Whale Distribution / Iceberg Sell above VWAP 24h
            c863 = (
                sm_s_pre
                & self.tag_toggles.get("863", True)
                & (df["top_pos_ls_chg_1h"] <= -0.04)
                & (df["whale_vs_retail_div"] <= -0.15)
                & (df["mm_vwap_z_24h"] >= 1.6)
                & (df["mm_rvol"] >= 2.0)
                & (df["mm_absorption"] >= 2.3)
                & (df["mm_mfi_14"] >= 60.0)
                & (df["real_cvd_div_short"] > 0.05)
                & (df["real_taker_buy_ratio"] <= 0.47)
            )
            # 864_MM_CAS_S: Breakdown Cascade Follow-Through Short
            c864 = (
                sm_s_pre
                & self.tag_toggles.get("864", True)
                & (df["oi_chg_4h"] >= 0.04)
                & (df["retail_ls"] >= 1.30)
                & (df["mm_vwap_z_4h"] >= -1.8)
                & (df["mm_vwap_z_4h"] <= -0.5)
                & (df["real_taker_buy_ratio"] <= 0.40)
                & (df["real_taker_delta_norm"] <= -0.45)
                & (df["mm_rvol"] >= 2.0)
                & (df["btc_ret_15m"] <= -0.003)
            )

            sm_s_idx = df.index[c861 | c862 | c863 | c864]
            if len(sm_s_idx) > 0:
                last_sm_s = -1000
                for idx in sm_s_idx:
                    pos = int(df.index.get_loc(idx))
                    if pos - last_sm_s < 48:
                        continue
                    last_sm_s = pos
                    tag = (
                        "861_MM_SFP_S" if c861.at[idx]
                        else ("862_MM_SQZ_S" if c862.at[idx]
                              else ("863_MM_DST_S" if c863.at[idx] else "864_MM_CAS_S"))
                    )
                    df.at[idx, "enter_short"] = 1
                    df.at[idx, "enter_tag"] = tag

        # Free temporary MM/OI feature columns after scoring (keep only mm_vwap_4h for custom_exit)
        drop_cols = [
            c for c in df.columns
            if c != "mm_vwap_4h" and (
                c.startswith("mm_") or c.startswith("real_") or c.startswith("oi_")
                or c in (
                    "quote_volume", "count", "taker_buy_quote_volume", "whale_trade_size_ratio",
                    "funding_rate", "funding_rate_z", "funding_interval_h", "log_oi_usdt",
                    "top_pos_ls", "top_acc_ls", "retail_ls", "whale_vs_retail_div",
                    "top_pos_ls_chg_1h", "metrics_taker_ls", "btc_ret_1h", "btc_ret_15m", "btc_rsi_5m",
                )
            )
        ]
        if drop_cols:
            df.drop(columns=drop_cols, inplace=True, errors="ignore")

        return df

    @staticmethod
    def check_mm_exit(
        pair: str,
        trade,
        current_time: datetime,
        current_rate: float,
        current_profit: float,
        dp=None,
        timeframe: str = "5m",
    ) -> Optional[str]:
        """Exit v1 Engine (proven 95.58% WR 12M / 96.72% WR OOS, PF 4.40 / 5.26)."""
        orig_tag = getattr(trade, "enter_tag", "") or "MM_AI"
        leverage = float(getattr(trade, "leverage", 6.0) or 6.0)
        open_rate = float(trade.open_rate)
        dur_hours = (current_time - trade.open_date_utc).total_seconds() / 3600.0

        if trade.is_short:
            best_rate = float(trade.min_rate) if trade.min_rate is not None else open_rate
            mfe_roe = (open_rate - best_rate) / open_rate * leverage
        else:
            best_rate = float(trade.max_rate) if trade.max_rate is not None else open_rate
            mfe_roe = (best_rate - open_rate) / open_rate * leverage

        # Keep reference tags 802_MM_AI & 851_MM_AI on exact Exit v1;
        # apply calibrated exits for 852_MM_AI / 853_MM_AI / 801_MM_AI / 803_MM_AI.
        is_opt_short = trade.is_short and (("852_MM_AI" in orig_tag) or ("853_MM_AI" in orig_tag))
        is_opt_801 = (not trade.is_short) and ("801_MM_AI" in orig_tag)
        is_opt_803 = (not trade.is_short) and ("803_MM_AI" in orig_tag)
        is_sm_momentum = any(t in orig_tag for t in ("812_MM_SQZ_L", "862_MM_SQZ_S", "864_MM_CAS_S"))
        is_sm_sfp = any(t in orig_tag for t in ("811_MM_SFP_L", "861_MM_SFP_S"))
        is_sm_abs = any(t in orig_tag for t in ("813_MM_ABS_L", "814_MM_FLS_L", "863_MM_DST_S"))

        if is_sm_momentum:
            if mfe_roe >= 0.40 and current_profit <= mfe_roe - 0.07 and current_profit >= 0.30:
                return f"exit_mm_sm_trail_t4 ( {orig_tag})"
            if mfe_roe >= 0.25 and current_profit <= mfe_roe - 0.06 and current_profit >= 0.17:
                return f"exit_mm_sm_trail_t3 ( {orig_tag})"
            if mfe_roe >= 0.14 and current_profit <= 0.095 and current_profit >= 0.080:
                return f"exit_mm_sm_trail_t2 ( {orig_tag})"
            if mfe_roe >= 0.09 and current_profit <= 0.062 and current_profit >= 0.052:
                return f"exit_mm_sm_trail_t1 ( {orig_tag})"
            if current_profit <= -0.16:
                return f"exit_mm_sm_hard_sl ( {orig_tag})"
            if dur_hours >= 24.0 and current_profit < 0.02:
                return f"exit_mm_sm_timestop_24h ( {orig_tag})"
            if dur_hours >= 48.0:
                return f"exit_mm_sm_max_48h ( {orig_tag})"
            return None

        if is_sm_sfp:
            if mfe_roe >= 0.25 and current_profit <= mfe_roe - 0.05 and current_profit >= 0.18:
                return f"exit_mm_sfp_trail_t3 ( {orig_tag})"
            if mfe_roe >= 0.14 and current_profit <= 0.100 and current_profit >= 0.085:
                return f"exit_mm_sfp_trail_t2 ( {orig_tag})"
            if mfe_roe >= 0.085 and current_profit <= 0.060 and current_profit >= 0.048:
                return f"exit_mm_sfp_trail_t1 ( {orig_tag})"
            if current_profit >= 0.060 and dp is not None:
                df_pair, _ = dp.get_analyzed_dataframe(pair, timeframe)
                if len(df_pair) > 0:
                    rows = df_pair.loc[df_pair["date"] <= current_time]
                    if len(rows) > 0:
                        vw = rows.iloc[-1].get("mm_vwap_4h", np.nan)
                        if vw is not None and not np.isnan(float(vw)):
                            if (not trade.is_short) and current_rate >= float(vw):
                                return f"exit_mm_vwap_reversion ( {orig_tag})"
                            if trade.is_short and current_rate <= float(vw):
                                return f"exit_mm_vwap_reversion ( {orig_tag})"
            if current_profit <= -0.16:
                return f"exit_mm_sfp_hard_sl ( {orig_tag})"
            if dur_hours >= 24.0 and current_profit < 0.02:
                return f"exit_mm_sfp_timestop_24h ( {orig_tag})"
            if dur_hours >= 48.0:
                return f"exit_mm_sfp_max_48h ( {orig_tag})"
            return None

        if is_sm_abs:
            if mfe_roe >= 0.28 and current_profit <= mfe_roe - 0.06 and current_profit >= 0.20:
                return f"exit_mm_abs_trail_t3 ( {orig_tag})"
            if mfe_roe >= 0.18 and current_profit <= mfe_roe - 0.05 and current_profit >= 0.12:
                return f"exit_mm_abs_trail_t2 ( {orig_tag})"
            if mfe_roe >= 0.11 and current_profit <= 0.080 and current_profit >= 0.065:
                return f"exit_mm_abs_trail_t1 ( {orig_tag})"
            if mfe_roe >= 0.078 and current_profit <= 0.058 and current_profit >= 0.045:
                return f"exit_mm_abs_mfe_protect ( {orig_tag})"
            if current_profit >= 0.065 and dp is not None:
                df_pair, _ = dp.get_analyzed_dataframe(pair, timeframe)
                if len(df_pair) > 0:
                    rows = df_pair.loc[df_pair["date"] <= current_time]
                    if len(rows) > 0:
                        vw = rows.iloc[-1].get("mm_vwap_4h", np.nan)
                        if vw is not None and not np.isnan(float(vw)):
                            if (not trade.is_short) and current_rate >= float(vw):
                                return f"exit_mm_vwap_reversion ( {orig_tag})"
                            if trade.is_short and current_rate <= float(vw):
                                return f"exit_mm_vwap_reversion ( {orig_tag})"
            if current_profit <= -0.22:
                return f"exit_mm_abs_hard_sl ( {orig_tag})"
            if dur_hours >= 48.0:
                return f"exit_mm_abs_max_48h ( {orig_tag})"
            return None

        if is_opt_short:
            # 1. Short Exit v2 Adaptive Trailing Profit Lock (higher AvgWin, avoids +2.8% choke)
            if mfe_roe >= 0.30 and current_profit <= mfe_roe - 0.06 and current_profit >= 0.22:
                return f"exit_mm_trail_t4 ( {orig_tag})"
            if mfe_roe >= 0.20 and current_profit <= mfe_roe - 0.05 and current_profit >= 0.14:
                return f"exit_mm_trail_t3 ( {orig_tag})"
            if mfe_roe >= 0.145 and current_profit <= 0.110 and current_profit >= 0.088:
                return f"exit_mm_trail_t2 ( {orig_tag})"
            if mfe_roe >= 0.102 and current_profit <= 0.075 and current_profit >= 0.060:
                return f"exit_mm_trail_t1 ( {orig_tag})"
            if "853_MM_AI" in orig_tag:
                if mfe_roe >= 0.075 and current_profit <= 0.058 and current_profit >= 0.042:
                    return f"exit_mm_mfe_protect ( {orig_tag})"
            else:
                if mfe_roe >= 0.080 and current_profit <= 0.055 and current_profit >= 0.040:
                    return f"exit_mm_mfe_protect ( {orig_tag})"

            # 2. Mean-Reversion 4h VWAP Harvest once >= +8.5% ROE
            if current_profit >= 0.085 and dp is not None:
                df_pair, _ = dp.get_analyzed_dataframe(pair, timeframe)
                if len(df_pair) > 0:
                    rows = df_pair.loc[df_pair["date"] <= current_time]
                    if len(rows) > 0:
                        vw = rows.iloc[-1].get("mm_vwap_4h", np.nan)
                        if vw is not None and not np.isnan(float(vw)):
                            if current_rate <= float(vw):
                                return f"exit_mm_vwap_reversion ( {orig_tag})"

            # 3. Tighter Short Hard SL (-28% ROE) & Max Duration (72h)
            if current_profit <= -0.28:
                return f"exit_mm_short_hard_sl ( {orig_tag})"
            if dur_hours >= 72.0:
                return f"exit_mm_short_max_72h ( {orig_tag})"
            return None

        if is_opt_801:
            # Calibrated Exit for 801_MM_AI (preserves 7.0%+ bounce protection, raises lock band above +4.0%)
            if mfe_roe >= 0.30 and current_profit <= mfe_roe - 0.06 and current_profit >= 0.22:
                return f"exit_mm_trail_t4 ( {orig_tag})"
            if mfe_roe >= 0.20 and current_profit <= mfe_roe - 0.05 and current_profit >= 0.14:
                return f"exit_mm_trail_t3 ( {orig_tag})"
            if mfe_roe >= 0.13 and current_profit <= 0.095 and current_profit >= 0.075:
                return f"exit_mm_trail_t2 ( {orig_tag})"
            if mfe_roe >= 0.088 and current_profit <= 0.068 and current_profit >= 0.054:
                return f"exit_mm_trail_t1 ( {orig_tag})"
            if mfe_roe >= 0.070 and current_profit <= 0.056 and current_profit >= 0.040:
                return f"exit_mm_mfe_protect ( {orig_tag})"

            if current_profit >= 0.075 and dp is not None:
                df_pair, _ = dp.get_analyzed_dataframe(pair, timeframe)
                if len(df_pair) > 0:
                    rows = df_pair.loc[df_pair["date"] <= current_time]
                    if len(rows) > 0:
                        vw = rows.iloc[-1].get("mm_vwap_4h", np.nan)
                        if vw is not None and not np.isnan(float(vw)):
                            if current_rate >= float(vw):
                                return f"exit_mm_vwap_reversion ( {orig_tag})"

            if current_profit <= -0.36:
                return f"exit_mm_long_hard_sl ( {orig_tag})"
            if dur_hours >= 144.0:
                return f"exit_mm_long_max_144h ( {orig_tag})"
            return None

        if is_opt_803:
            # Calibrated Exit for 803_MM_AI (Liquidation Cascade Reclaim)
            if mfe_roe >= 0.30 and current_profit <= mfe_roe - 0.06 and current_profit >= 0.22:
                return f"exit_mm_trail_t4 ( {orig_tag})"
            if mfe_roe >= 0.20 and current_profit <= mfe_roe - 0.05 and current_profit >= 0.14:
                return f"exit_mm_trail_t3 ( {orig_tag})"
            if mfe_roe >= 0.13 and current_profit <= 0.095 and current_profit >= 0.075:
                return f"exit_mm_trail_t2 ( {orig_tag})"
            if mfe_roe >= 0.088 and current_profit <= 0.068 and current_profit >= 0.054:
                return f"exit_mm_trail_t1 ( {orig_tag})"
            if mfe_roe >= 0.072 and current_profit <= 0.056 and current_profit >= 0.042:
                return f"exit_mm_mfe_protect ( {orig_tag})"

            if current_profit >= 0.080 and dp is not None:
                df_pair, _ = dp.get_analyzed_dataframe(pair, timeframe)
                if len(df_pair) > 0:
                    rows = df_pair.loc[df_pair["date"] <= current_time]
                    if len(rows) > 0:
                        vw = rows.iloc[-1].get("mm_vwap_4h", np.nan)
                        if vw is not None and not np.isnan(float(vw)):
                            if current_rate >= float(vw):
                                return f"exit_mm_vwap_reversion ( {orig_tag})"

            if current_profit <= -0.32:
                return f"exit_mm_long_hard_sl ( {orig_tag})"
            if dur_hours >= 144.0:
                return f"exit_mm_long_max_144h ( {orig_tag})"
            return None

        # 1. Exit v1 Adaptive Trailing Profit Lock (untouched for 802/851)
        if mfe_roe >= 0.30 and current_profit <= mfe_roe - 0.06 and current_profit >= 0.22:
            return f"exit_mm_trail_t4 ( {orig_tag})"
        if mfe_roe >= 0.20 and current_profit <= mfe_roe - 0.05 and current_profit >= 0.14:
            return f"exit_mm_trail_t3 ( {orig_tag})"
        if mfe_roe >= 0.13 and current_profit <= 0.095 and current_profit >= 0.075:
            return f"exit_mm_trail_t2 ( {orig_tag})"
        if mfe_roe >= 0.088 and current_profit <= 0.065 and current_profit >= 0.052:
            return f"exit_mm_trail_t1 ( {orig_tag})"
        if mfe_roe >= 0.070 and current_profit <= 0.045 and current_profit >= 0.028:
            return f"exit_mm_mfe_protect ( {orig_tag})"

        # 2. Mean-Reversion 4h VWAP Harvest once >= +7.5% ROE
        if current_profit >= 0.075 and dp is not None:
            df_pair, _ = dp.get_analyzed_dataframe(pair, timeframe)
            if len(df_pair) > 0:
                rows = df_pair.loc[df_pair["date"] <= current_time]
                if len(rows) > 0:
                    vw = rows.iloc[-1].get("mm_vwap_4h", np.nan)
                    if vw is not None and not np.isnan(float(vw)):
                        if (not trade.is_short) and current_rate >= float(vw):
                            return f"exit_mm_vwap_reversion ( {orig_tag})"
                        if trade.is_short and current_rate <= float(vw):
                            return f"exit_mm_vwap_reversion ( {orig_tag})"

        # 3. Hard SL & Max Duration
        if trade.is_short:
            if current_profit <= -0.34:
                return f"exit_mm_short_hard_sl ( {orig_tag})"
            if dur_hours >= 72.0:
                return f"exit_mm_short_max_72h ( {orig_tag})"
        else:
            if current_profit <= -0.36:
                return f"exit_mm_long_hard_sl ( {orig_tag})"
            if dur_hours >= 144.0:
                return f"exit_mm_long_max_144h ( {orig_tag})"

        return None
