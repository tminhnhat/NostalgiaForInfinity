# -*- coding: utf-8 -*-
"""
BinanceMMDataProvider
Unified Market Maker / Order Flow / Liquidation-Flush Data Bridge for Freqtrade:
  - Offline Backtest mode: reads pre-synced Binance Vision enriched parquet files from
    `user_data/data/binance/mm_enriched/{SYMBOL}.parquet` (zero network latency).
  - Live / Dry-Run mode: fetches real-time Binance Futures API data with 5m TTL cache
    and safe fallbacks (never blocks or crashes trading loop on API timeout):
      * /fapi/v1/klines               -> real taker_buy_quote_volume, quote_volume, count
      * /fapi/v1/fundingRate          -> funding_rate, funding_rate_z, funding_interval_h
      * /futures/data/openInterestHist             -> log_oi_usdt, oi_chg_15m/1h/4h, oi_to_vol_ratio
      * /futures/data/topLongShortPositionRatio    -> top_pos_ls, top_pos_ls_chg_1h
      * /futures/data/topLongShortAccountRatio     -> top_acc_ls
      * /futures/data/globalLongShortAccountRatio  -> retail_ls, whale_vs_retail_div
      * /futures/data/takerlongshortRatio          -> metrics_taker_ls
"""
from __future__ import annotations

import logging
import time
from pathlib import Path
from typing import Dict, Optional, Tuple

import numpy as np
import pandas as pd
import requests
from requests.adapters import HTTPAdapter

log = logging.getLogger(__name__)

FAPI_BASE = "https://fapi.binance.com"

ENRICHED_COLS = [
    "quote_volume",
    "count",
    "taker_buy_quote_volume",
    "funding_rate",
    "funding_rate_z",
    "funding_interval_h",
    "log_oi_usdt",
    "oi_chg_15m",
    "oi_chg_1h",
    "oi_chg_4h",
    "oi_to_vol_ratio",
    "top_pos_ls",
    "top_acc_ls",
    "retail_ls",
    "whale_vs_retail_div",
    "top_pos_ls_chg_1h",
    "metrics_taker_ls",
]


def pair_to_binance_symbol(pair: str) -> str:
    """Convert Freqtrade futures pair (e.g. 'BTC/USDT:USDT') -> 'BTCUSDT'."""
    base = pair.split("/")[0].strip().upper()
    quote = pair.split("/")[1].split(":")[0].strip().upper() if "/" in pair else "USDT"
    return f"{base}{quote}"


class BinanceMMDataProvider:
    def __init__(self, enriched_dir: str = "user_data/data/binance/mm_enriched", ttl_sec: int = 240) -> None:
        self.enriched_dir = Path(enriched_dir)
        self.ttl_sec = ttl_sec
        self._live_cache: Dict[str, Tuple[float, Dict[str, float]]] = {}
        self._offline_cache: Dict[str, Optional[pd.DataFrame]] = {}
        self._session = requests.Session()
        self._session.mount("https://", HTTPAdapter(pool_connections=16, pool_maxsize=16, max_retries=1))
        self._session.headers.update({"User-Agent": "FreqtradeMMProvider/1.0"})

    # -------------------------------------------------------------------------
    # Offline Backtest Enrichment (from Binance Vision parquet cache)
    # -------------------------------------------------------------------------
    def merge_offline_enriched(self, df: pd.DataFrame, pair: str) -> pd.DataFrame:
        sym = pair_to_binance_symbol(pair)
        fp = self.enriched_dir / f"{sym}.parquet"
        if not fp.exists():
            return df
        try:
            edf = pd.read_parquet(fp)
            if len(edf) == 0:
                return df
            edf["_merge_dt"] = pd.to_datetime(edf["date"], utc=True).astype("datetime64[ns, UTC]")
            edf = edf.sort_values("_merge_dt").drop_duplicates(subset=["_merge_dt"]).reset_index(drop=True)
        except Exception as e:
            log.warning("Failed reading offline MM parquet %s: %s", fp, e)
            return df

        edf_cols = [c for c in ENRICHED_COLS if c in edf.columns]
        if not edf_cols:
            return df

        # Merge ONLY the 1-column date index to avoid copying the 600-column NFI DataFrame
        left_dt = pd.DataFrame({
            "_merge_dt": pd.to_datetime(df["date"], utc=True).astype("datetime64[ns, UTC]"),
            "_orig_pos": np.arange(len(df)),
        })
        merged = pd.merge_asof(
            left_dt.sort_values("_merge_dt"),
            edf[["_merge_dt"] + edf_cols],
            on="_merge_dt",
            direction="backward",
            tolerance=pd.Timedelta("15min"),
        ).sort_values("_orig_pos")

        for c in edf_cols:
            df[c] = merged[c].to_numpy(dtype=np.float32)
        return df

    # -------------------------------------------------------------------------
    # Live / Dry-Run Real-Time Fetch (5m TTL cached, non-fatal on errors)
    # -------------------------------------------------------------------------
    def _get_json(self, path: str, params: dict, timeout: float = 4.0):
        try:
            r = self._session.get(f"{FAPI_BASE}{path}", params=params, timeout=timeout)
            if r.status_code == 200:
                return r.json()
        except Exception:
            return None
        return None

    def fetch_live_snapshot(self, pair: str, qvol_1h: float = 1.0) -> Dict[str, float]:
        sym = pair_to_binance_symbol(pair)
        now = time.time()
        cached = self._live_cache.get(sym)
        if cached is not None and (now - cached[0]) < self.ttl_sec:
            return cached[1]

        snap: Dict[str, float] = {c: np.nan for c in ENRICHED_COLS}

        # 1. Recent 5m klines (real taker_buy_quote_volume & trade count)
        kl = self._get_json("/fapi/v1/klines", {"symbol": sym, "interval": "5m", "limit": 2})
        if isinstance(kl, list) and len(kl) >= 2:
            bar = kl[-2]  # last closed 5m candle
            snap["quote_volume"] = float(bar[7])
            snap["count"] = float(bar[8])
            snap["taker_buy_quote_volume"] = float(bar[10])

        # 2. Funding rate history (last 30 settlements for funding_rate_z)
        fr = self._get_json("/fapi/v1/fundingRate", {"symbol": sym, "limit": 30})
        if isinstance(fr, list) and len(fr) >= 2:
            rates = np.array([float(x["fundingRate"]) for x in fr], dtype=float)
            snap["funding_rate"] = float(rates[-1])
            std = float(np.std(rates))
            snap["funding_rate_z"] = float((rates[-1] - np.mean(rates)) / max(std, 1e-6))
            dt_h = (int(fr[-1]["fundingTime"]) - int(fr[-2]["fundingTime"])) / 3600000.0
            snap["funding_interval_h"] = float(round(dt_h)) if dt_h > 0 else 8.0

        # 3. Open Interest history (5m, last 50 bars -> 15m/1h/4h change)
        oi = self._get_json("/futures/data/openInterestHist", {"symbol": sym, "period": "5m", "limit": 50})
        if isinstance(oi, list) and len(oi) >= 13:
            vals = np.array([float(x["sumOpenInterestValue"]) for x in oi], dtype=float)
            cur_oi = max(vals[-1], 1.0)
            snap["log_oi_usdt"] = float(np.log1p(cur_oi))
            snap["oi_chg_15m"] = float((vals[-1] - vals[-4]) / max(vals[-4], 1.0)) if len(vals) >= 4 else 0.0
            snap["oi_chg_1h"] = float((vals[-1] - vals[-13]) / max(vals[-13], 1.0)) if len(vals) >= 13 else 0.0
            snap["oi_chg_4h"] = float((vals[-1] - vals[0]) / max(vals[0], 1.0))
            snap["oi_to_vol_ratio"] = float(cur_oi / max(qvol_1h, 1.0))

        # 4. Top Trader Position L/S Ratio (Smart Money)
        tp = self._get_json("/futures/data/topLongShortPositionRatio", {"symbol": sym, "period": "5m", "limit": 13})
        if isinstance(tp, list) and len(tp) >= 1:
            cur_tp = float(tp[-1]["longShortRatio"])
            snap["top_pos_ls"] = cur_tp
            if len(tp) >= 13:
                snap["top_pos_ls_chg_1h"] = cur_tp - float(tp[0]["longShortRatio"])

        # 5. Top Trader Account L/S Ratio
        ta_ls = self._get_json("/futures/data/topLongShortAccountRatio", {"symbol": sym, "period": "5m", "limit": 1})
        if isinstance(ta_ls, list) and len(ta_ls) >= 1:
            snap["top_acc_ls"] = float(ta_ls[-1]["longShortRatio"])

        # 6. Global Retail Account L/S Ratio
        gl = self._get_json("/futures/data/globalLongShortAccountRatio", {"symbol": sym, "period": "5m", "limit": 1})
        if isinstance(gl, list) and len(gl) >= 1:
            snap["retail_ls"] = float(gl[-1]["longShortRatio"])
            if not np.isnan(snap["top_pos_ls"]):
                snap["whale_vs_retail_div"] = snap["top_pos_ls"] - snap["retail_ls"]

        # 7. Taker Buy/Sell Volume Ratio
        tk = self._get_json("/futures/data/takerlongshortRatio", {"symbol": sym, "period": "5m", "limit": 1})
        if isinstance(tk, list) and len(tk) >= 1:
            snap["metrics_taker_ls"] = float(tk[-1]["buySellRatio"])

        self._live_cache[sym] = (now, snap)
        return snap
