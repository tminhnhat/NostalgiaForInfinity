# -*- coding: utf-8 -*-
"""
Direction B: Train AI Gatekeeper v2 (LightGBM) across 500 Binance USDT-M Perpetual Pairs
using REAL Market Maker / Order Flow / Liquidation-Flush Data from Binance Vision:
  1. Monthly 5m Klines (OHLCV + REAL taker_buy_volume + taker_buy_quote_volume + trade count)
  2. Monthly Funding Rate (last_funding_rate + funding_interval_hours)
  3. Event-driven 5m Metrics (sum_open_interest_value, sum_toptrader_long_short_ratio,
     count_toptrader_long_short_ratio, count_long_short_ratio, sum_taker_long_short_vol_ratio)

Strict Chronological Split (2025-11-01 -> 2026-10-31):
  - Train: 2025-11-01 -> 2026-06-30
  - Val:   2026-07-01 -> 2026-08-15
  - OOS:   2026-08-15 -> 2026-10-31 (Pure Out-of-Sample)
"""
from __future__ import annotations

import io
import json
import os
import pickle
import subprocess
import sys
import time
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

import numpy as np
import pandas as pd

def log(m: str) -> None:
    print(m, flush=True)

for mod, pkg in [("requests", "requests"), ("lightgbm", "lightgbm"), ("sklearn", "scikit-learn"), ("boto3", "boto3")]:
    try:
        __import__(mod)
    except ImportError:
        log(f"📦 Installing {pkg}...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", pkg], check=True)

import boto3
from botocore.config import Config
import lightgbm as lgb
import requests
from requests.adapters import HTTPAdapter
from sklearn.metrics import roc_auc_score
import talib.abstract as ta

WORK_DIR = Path("/content/mm_ai_500")
WORK_DIR.mkdir(parents=True, exist_ok=True)
MODELS_DIR = Path("/content/NostalgiaForInfinity/user_data/models")
MODELS_DIR.mkdir(parents=True, exist_ok=True)

MONTHS = [
    "2025-11", "2025-12", "2026-01", "2026-02", "2026-03", "2026-04",
    "2026-05", "2026-06", "2026-07", "2026-08", "2026-09", "2026-10",
]
VISION_BASE = "https://data.binance.vision/data/futures/um"

def make_session(pool_size: int = 64) -> requests.Session:
    s = requests.Session()
    adapter = HTTPAdapter(pool_connections=pool_size, pool_maxsize=pool_size, max_retries=2)
    s.mount("https://", adapter)
    s.headers.update({"User-Agent": "Mozilla/5.0"})
    return s

SESSION = make_session(64)

def fetch_top_500_usdt_perps() -> List[str]:
    info = SESSION.get("https://fapi.binance.com/fapi/v1/exchangeInfo", timeout=20).json()
    perps = {
        s["symbol"]
        for s in info["symbols"]
        if s.get("contractType") == "PERPETUAL" and s.get("quoteAsset") == "USDT" and s.get("status") == "TRADING"
    }
    tickers = SESSION.get("https://fapi.binance.com/fapi/v1/ticker/24hr", timeout=20).json()
    ranked = sorted(
        [(t["symbol"], float(t.get("quoteVolume", 0.0))) for t in tickers if t["symbol"] in perps],
        key=lambda x: x[1],
        reverse=True,
    )
    syms = [s for s, _ in ranked[:500]]
    if "BTCUSDT" not in syms:
        syms.insert(0, "BTCUSDT")
    return syms[:500]


def download_zip_csv(url: str, cols: Optional[List[str]] = None) -> Optional[pd.DataFrame]:
    try:
        r = SESSION.get(url, timeout=15)
        if r.status_code != 200:
            return None
        with zipfile.ZipFile(io.BytesIO(r.content)) as zf:
            name = zf.namelist()[0]
            raw = zf.read(name)
        # Detect header automatically
        first_line = raw[:120].decode("utf-8", errors="ignore").splitlines()[0]
        has_header = any(ch.isalpha() for ch in first_line)
        if has_header:
            return pd.read_csv(io.BytesIO(raw))
        else:
            return pd.read_csv(io.BytesIO(raw), header=None, names=cols)
    except Exception:
        return None


KLINE_COLS = [
    "open_time", "open", "high", "low", "close", "volume",
    "close_time", "quote_volume", "count", "taker_buy_volume", "taker_buy_quote_volume", "ignore",
]


def load_symbol_klines_and_funding(sym: str) -> Tuple[Optional[pd.DataFrame], Optional[pd.DataFrame]]:
    k_dfs = []
    f_dfs = []
    for ym in MONTHS:
        k_url = f"{VISION_BASE}/monthly/klines/{sym}/5m/{sym}-5m-{ym}.zip"
        kd = download_zip_csv(k_url, KLINE_COLS)
        if kd is not None and len(kd) > 0:
            k_dfs.append(kd[["open_time", "open", "high", "low", "close", "volume", "quote_volume", "count", "taker_buy_volume", "taker_buy_quote_volume"]])
        f_url = f"{VISION_BASE}/monthly/fundingRate/{sym}/{sym}-fundingRate-{ym}.zip"
        fd = download_zip_csv(f_url, ["calc_time", "funding_interval_hours", "last_funding_rate"])
        if fd is not None and len(fd) > 0:
            f_dfs.append(fd[["calc_time", "funding_interval_hours", "last_funding_rate"]])

    if not k_dfs:
        return None, None
    kdf = pd.concat(k_dfs, ignore_index=True)
    for c in ["open_time", "open", "high", "low", "close", "volume", "quote_volume", "count", "taker_buy_volume", "taker_buy_quote_volume"]:
        kdf[c] = pd.to_numeric(kdf[c], errors="coerce")
    kdf = kdf.dropna(subset=["open_time", "close"]).drop_duplicates(subset=["open_time"]).sort_values("open_time").reset_index(drop=True)
    kdf["date"] = pd.to_datetime(kdf["open_time"], unit="ms", utc=True)

    fdf = None
    if f_dfs:
        fdf = pd.concat(f_dfs, ignore_index=True)
        for c in ["calc_time", "funding_interval_hours", "last_funding_rate"]:
            fdf[c] = pd.to_numeric(fdf[c], errors="coerce")
        fdf = fdf.dropna(subset=["calc_time", "last_funding_rate"]).drop_duplicates(subset=["calc_time"]).sort_values("calc_time").reset_index(drop=True)
        fdf["date"] = pd.to_datetime(fdf["calc_time"], unit="ms", utc=True)
    return kdf, fdf


def triple_barrier_label(
    opens: np.ndarray, highs: np.ndarray, lows: np.ndarray, closes: np.ndarray,
    idx: int, is_short: bool, tp_spot: float = 0.0135, sl_spot: float = 0.055, horizon: int = 576,
) -> Tuple[int, float]:
    if idx + 1 >= len(opens):
        return -1, 0.0
    entry = opens[idx + 1]
    if entry <= 0 or np.isnan(entry):
        return -1, 0.0
    end = min(len(opens), idx + 1 + horizon)
    if not is_short:
        tp_px = entry * (1.0 + tp_spot)
        sl_px = entry * (1.0 - sl_spot)
        for j in range(idx + 1, end):
            if lows[j] <= sl_px:
                return 0, -sl_spot * 6.0 * 100.0
            if highs[j] >= tp_px:
                return 1, tp_spot * 6.0 * 100.0 - 0.5
        ret = (closes[end - 1] - entry) / entry * 6.0 * 100.0 - 0.5
        return (1 if ret >= 5.0 else 0), ret
    else:
        tp_px = entry * (1.0 - tp_spot)
        sl_px = entry * (1.0 + sl_spot)
        for j in range(idx + 1, end):
            if highs[j] >= sl_px:
                return 0, -sl_spot * 6.0 * 100.0
            if lows[j] <= tp_px:
                return 1, tp_spot * 6.0 * 100.0 - 0.5
        ret = (entry - closes[end - 1]) / entry * 6.0 * 100.0 - 0.5
        return (1 if ret >= 5.0 else 0), ret


BASE_FEATURES = [
    "mm_lower_wick_ratio", "mm_upper_wick_ratio", "mm_body_pct",
    "mm_atr_pct", "mm_range_atr", "mm_rvol", "mm_absorption", "mm_log_qvol_1h",
    "real_taker_buy_ratio", "real_taker_delta_norm", "real_cvd_12_norm", "real_cvd_48_norm",
    "real_cvd_div_long", "real_cvd_div_short", "whale_trade_size_ratio",
    "mm_mfi_14", "mm_cmf_20",
    "mm_vwap_z_4h", "mm_vwap_z_24h", "mm_dist_vwap_24h",
    "mm_dist_swing_low_24h", "mm_dist_swing_high_24h",
    "mm_rsi_5m", "mm_rsi_15m", "mm_rsi_1h",
    "mm_dist_ema200_1h", "mm_ema50_slope_1h",
    "funding_rate", "funding_rate_z", "funding_interval_h",
    "btc_ret_15m", "btc_ret_1h", "btc_rsi_5m",
]

METRICS_FEATURES = [
    "log_oi_usdt", "oi_chg_15m", "oi_chg_1h", "oi_chg_4h", "oi_to_vol_ratio",
    "top_pos_ls", "top_acc_ls", "retail_ls", "whale_vs_retail_div",
    "top_pos_ls_chg_1h", "metrics_taker_ls",
]

ALL_FEATURES = BASE_FEATURES + METRICS_FEATURES


def process_one_symbol(sym: str, btc_df: pd.DataFrame) -> Tuple[List[dict], List[dict]]:
    kdf, fdf = load_symbol_klines_and_funding(sym)
    if kdf is None or len(kdf) < 1000:
        return [], []

    eps = 1e-10
    df = kdf
    candle_range = (df["high"] - df["low"]).clip(lower=eps)
    body = (df["close"] - df["open"]).abs()
    lower_wick = np.minimum(df["open"], df["close"]) - df["low"]
    upper_wick = df["high"] - np.maximum(df["open"], df["close"])

    df["mm_lower_wick_ratio"] = (lower_wick / candle_range).clip(0.0, 1.0)
    df["mm_upper_wick_ratio"] = (upper_wick / candle_range).clip(0.0, 1.0)
    df["mm_body_pct"] = body / df["close"].clip(lower=eps)

    df["mm_atr_14"] = ta.ATR(df, timeperiod=14)
    df["mm_atr_pct"] = (df["mm_atr_14"] / df["close"].clip(lower=eps)).clip(lower=1e-5)
    df["mm_range_atr"] = candle_range / df["mm_atr_14"].clip(lower=eps)
    df["mm_rsi_5m"] = ta.RSI(df, timeperiod=14)

    # REAL Aggressive Order Flow from Binance klines (taker_buy_quote_volume & count)
    qvol = df["quote_volume"].clip(lower=eps)
    tb_qvol = df["taker_buy_quote_volume"].clip(lower=0.0)
    df["real_taker_buy_ratio"] = (tb_qvol / qvol).clip(0.0, 1.0)
    real_delta = 2.0 * tb_qvol - qvol  # taker buy USDT - taker sell USDT
    qvol_ma_48 = qvol.rolling(48, min_periods=10).mean().clip(lower=eps)
    df["mm_rvol"] = qvol / qvol_ma_48
    df["real_taker_delta_norm"] = real_delta / qvol_ma_48
    real_cvd_12 = real_delta.rolling(12, min_periods=1).sum()
    real_cvd_48 = real_delta.rolling(48, min_periods=1).sum()
    df["real_cvd_12_norm"] = real_cvd_12 / (qvol_ma_48 * 12.0)
    df["real_cvd_48_norm"] = real_cvd_48 / (qvol_ma_48 * 48.0)
    prev_cvd_low = real_cvd_48.rolling(48, min_periods=12).min().shift(3)
    prev_cvd_high = real_cvd_48.rolling(48, min_periods=12).max().shift(3)
    df["real_cvd_div_long"] = (real_cvd_48 - prev_cvd_low) / (qvol_ma_48 * 48.0)
    df["real_cvd_div_short"] = (prev_cvd_high - real_cvd_48) / (qvol_ma_48 * 48.0)

    # Whale average trade size burst
    avg_trade_sz = qvol / df["count"].clip(lower=1.0)
    df["whale_trade_size_ratio"] = avg_trade_sz / avg_trade_sz.rolling(48, min_periods=10).mean().clip(lower=eps)

    qvol_1h = qvol.rolling(12, min_periods=1).sum()
    df["mm_quote_vol_1h"] = qvol_1h
    df["mm_log_qvol_1h"] = np.log1p(qvol_1h.clip(lower=0.0))
    df["mm_absorption"] = df["mm_rvol"] / np.maximum(df["mm_body_pct"] / df["mm_atr_pct"], 0.25)

    df["mm_mfi_14"] = ta.MFI(df, timeperiod=14)
    mfm = ((df["close"] - df["low"]) - (df["high"] - df["close"])) / candle_range
    df["mm_cmf_20"] = (mfm * df["volume"]).rolling(20, min_periods=5).sum() / df["volume"].rolling(20, min_periods=5).sum().clip(lower=eps)

    # Synthetic Liquidation Heatmap (VWAP Z-scores + 24h Swing Pools)
    typical = (df["high"] + df["low"] + df["close"]) / 3.0
    pv = typical * df["volume"]
    vwap_4h = pv.rolling(48, min_periods=12).sum() / df["volume"].rolling(48, min_periods=12).sum().clip(lower=eps)
    vwap_24h = pv.rolling(288, min_periods=24).sum() / df["volume"].rolling(288, min_periods=24).sum().clip(lower=eps)
    std_4h = (df["close"] - vwap_4h).rolling(48, min_periods=12).std().clip(lower=eps)
    std_24h = (df["close"] - vwap_24h).rolling(288, min_periods=24).std().clip(lower=eps)
    df["mm_vwap_z_4h"] = (df["close"] - vwap_4h) / std_4h
    df["mm_vwap_z_24h"] = (df["close"] - vwap_24h) / std_24h
    df["mm_dist_vwap_24h"] = (df["close"] - vwap_24h) / vwap_24h.clip(lower=eps)

    sw_low_24h = df["low"].rolling(288, min_periods=48).min().shift(1)
    sw_high_24h = df["high"].rolling(288, min_periods=48).max().shift(1)
    df["mm_dist_swing_low_24h"] = (df["close"] - sw_low_24h) / df["close"].clip(lower=eps)
    df["mm_dist_swing_high_24h"] = (sw_high_24h - df["close"]) / df["close"].clip(lower=eps)

    # Resample 5m -> 15m and 1h in memory (fast & leak-free via shift(1))
    d_idx = df.set_index("date")
    df15 = d_idx["close"].resample("15min").last().dropna().to_frame("close")
    df15["mm_rsi_15m"] = ta.RSI(df15, timeperiod=14).shift(1)
    df15 = df15[["mm_rsi_15m"]].reset_index()

    df1h = d_idx["close"].resample("1h").last().dropna().to_frame("close")
    df1h["mm_rsi_1h"] = ta.RSI(df1h, timeperiod=14).shift(1)
    e50 = ta.EMA(df1h, timeperiod=50)
    e200 = ta.EMA(df1h, timeperiod=200)
    df1h["mm_ema200_1h"] = e200.shift(1)
    df1h["mm_ema50_slope_1h"] = ((e50 - e50.shift(4)) / e50.shift(4).clip(lower=eps)).shift(1)
    df1h = df1h[["mm_rsi_1h", "mm_ema200_1h", "mm_ema50_slope_1h"]].reset_index()

    df = pd.merge_asof(df, df15, on="date", direction="backward")
    df = pd.merge_asof(df, df1h, on="date", direction="backward")
    df["mm_dist_ema200_1h"] = (df["close"] - df["mm_ema200_1h"]) / df["mm_ema200_1h"].clip(lower=eps)

    # Merge REAL Funding Rate (backward asof = strictly causal)
    if fdf is not None and len(fdf) > 0:
        fdf_m = fdf[["date", "last_funding_rate", "funding_interval_hours"]].copy()
        f_mean = fdf_m["last_funding_rate"].rolling(90, min_periods=5).mean()
        f_std = fdf_m["last_funding_rate"].rolling(90, min_periods=5).std().clip(lower=1e-6)
        fdf_m["funding_rate_z"] = (fdf_m["last_funding_rate"] - f_mean) / f_std
        fdf_m = fdf_m.rename(columns={"last_funding_rate": "funding_rate", "funding_interval_hours": "funding_interval_h"})
        df = pd.merge_asof(df, fdf_m, on="date", direction="backward")
    else:
        df["funding_rate"] = 0.0
        df["funding_rate_z"] = 0.0
        df["funding_interval_h"] = 8.0

    # Merge BTC context
    df = pd.merge_asof(df, btc_df, on="date", direction="backward")

    # Select high-conviction Market Maker candidates (sweeps / overextensions)
    has_liq = (df["volume"] > 0) & (df["mm_quote_vol_1h"] >= 400_000.0)
    cand_long = (
        has_liq
        & (df["mm_vwap_z_24h"] <= -2.2)
        & (df["mm_rsi_15m"] < 35.0)
        & (df["mm_rvol"] >= 2.2)
        & ((df["mm_lower_wick_ratio"] >= 0.40) | (df["real_taker_buy_ratio"] >= 0.56))
    )
    cand_short = (
        has_liq
        & (df["mm_vwap_z_24h"] >= 2.2)
        & (df["mm_rsi_15m"] > 65.0)
        & (df["mm_rvol"] >= 2.2)
        & ((df["mm_upper_wick_ratio"] >= 0.40) | (df["real_taker_buy_ratio"] <= 0.44))
    )

    opens = df["open"].to_numpy()
    highs = df["high"].to_numpy()
    lows = df["low"].to_numpy()
    closes = df["close"].to_numpy()
    dates = df["date"].to_numpy()

    l_rows, s_rows = [], []
    last_l = -100
    for idx in np.flatnonzero(cand_long.to_numpy()):
        if idx - last_l < 48:  # 4h cooldown per symbol/side
            continue
        lbl, ret = triple_barrier_label(opens, highs, lows, closes, int(idx), is_short=False)
        if lbl < 0:
            continue
        last_l = int(idx)
        row = {f: float(df.at[idx, f]) if pd.notna(df.at[idx, f]) else np.nan for f in BASE_FEATURES}
        row["date"] = dates[idx]
        row["symbol"] = sym
        row["qvol_1h"] = float(df.at[idx, "mm_quote_vol_1h"])
        row["label"] = lbl
        row["ret_roe"] = ret
        l_rows.append(row)

    last_s = -100
    for idx in np.flatnonzero(cand_short.to_numpy()):
        if idx - last_s < 48:
            continue
        lbl, ret = triple_barrier_label(opens, highs, lows, closes, int(idx), is_short=True)
        if lbl < 0:
            continue
        last_s = int(idx)
        row = {f: float(df.at[idx, f]) if pd.notna(df.at[idx, f]) else np.nan for f in BASE_FEATURES}
        row["date"] = dates[idx]
        row["symbol"] = sym
        row["qvol_1h"] = float(df.at[idx, "mm_quote_vol_1h"])
        row["label"] = lbl
        row["ret_roe"] = ret
        s_rows.append(row)

    return l_rows, s_rows


def fetch_metrics_day(sym_date: Tuple[str, str]) -> Tuple[Tuple[str, str], Optional[pd.DataFrame]]:
    sym, dstr = sym_date
    url = f"{VISION_BASE}/daily/metrics/{sym}/{sym}-metrics-{dstr}.zip"
    df = download_zip_csv(url)
    if df is None or len(df) == 0 or "create_time" not in df.columns:
        return sym_date, None
    df["date"] = pd.to_datetime(df["create_time"], utc=True, errors="coerce")
    cols = [
        "sum_open_interest_value", "count_toptrader_long_short_ratio",
        "sum_toptrader_long_short_ratio", "count_long_short_ratio", "sum_taker_long_short_vol_ratio",
    ]
    for c in cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
        else:
            df[c] = np.nan
    return sym_date, df[["date"] + cols].dropna(subset=["date"])


def enrich_with_metrics(df_all: pd.DataFrame) -> pd.DataFrame:
    if len(df_all) == 0:
        return df_all
    df_all = df_all.copy()
    df_all["date"] = pd.to_datetime(df_all["date"], utc=True)

    # Collect unique (symbol, date) + previous date if hour < 5 UTC (needed for 4h OI change)
    needed: Set[Tuple[str, str]] = set()
    for sym, dt in zip(df_all["symbol"], df_all["date"]):
        d0 = dt.strftime("%Y-%m-%d")
        needed.add((sym, d0))
        if dt.hour < 5:
            d_prev = (dt - pd.Timedelta(days=1)).strftime("%Y-%m-%d")
            needed.add((sym, d_prev))

    log(f"🔄 Stage 2: Fetching {len(needed)} unique (symbol, date) 5m Binance Metrics files (OI + TopTrader L/S + Retail L/S)...")
    t0 = time.time()
    by_sym: Dict[str, List[pd.DataFrame]] = {}
    done = 0
    with ThreadPoolExecutor(max_workers=48) as ex:
        futs = [ex.submit(fetch_metrics_day, sd) for sd in needed]
        for fut in as_completed(futs):
            (sym, _), mdf = fut.result()
            if mdf is not None:
                by_sym.setdefault(sym, []).append(mdf)
            done += 1
            if done % 3000 == 0:
                log(f"   ... fetched {done}/{len(needed)} metrics files ({time.time()-t0:.0f}s)")

    log(f"✅ Metrics fetched for {len(by_sym)} symbols in {time.time()-t0:.1f}s")

    # Merge metrics per symbol strictly causally (merge_asof backward within 15m tolerance)
    out_parts = []
    for sym, grp in df_all.groupby("symbol", sort=False):
        grp = grp.sort_values("date").copy()
        if sym in by_sym:
            mdf = pd.concat(by_sym[sym], ignore_index=True).drop_duplicates(subset=["date"]).sort_values("date").reset_index(drop=True)
            oi = mdf["sum_open_interest_value"].clip(lower=1.0)
            mdf["log_oi_usdt"] = np.log1p(oi)
            mdf["oi_chg_15m"] = oi.pct_change(3)
            mdf["oi_chg_1h"] = oi.pct_change(12)
            mdf["oi_chg_4h"] = oi.pct_change(48)
            mdf["top_pos_ls"] = mdf["sum_toptrader_long_short_ratio"]
            mdf["top_acc_ls"] = mdf["count_toptrader_long_short_ratio"]
            mdf["retail_ls"] = mdf["count_long_short_ratio"]
            mdf["whale_vs_retail_div"] = mdf["top_pos_ls"] - mdf["retail_ls"]
            mdf["top_pos_ls_chg_1h"] = mdf["top_pos_ls"] - mdf["top_pos_ls"].shift(12)
            mdf["metrics_taker_ls"] = mdf["sum_taker_long_short_vol_ratio"]
            keep_cols = [
                "date", "sum_open_interest_value", "log_oi_usdt", "oi_chg_15m", "oi_chg_1h", "oi_chg_4h",
                "top_pos_ls", "top_acc_ls", "retail_ls", "whale_vs_retail_div", "top_pos_ls_chg_1h", "metrics_taker_ls",
            ]
            merged = pd.merge_asof(grp, mdf[keep_cols], on="date", direction="backward", tolerance=pd.Timedelta("15min"))
            merged["oi_to_vol_ratio"] = merged["sum_open_interest_value"] / merged["qvol_1h"].clip(lower=1.0)
            merged = merged.drop(columns=["sum_open_interest_value"])
            out_parts.append(merged)
        else:
            for c in METRICS_FEATURES:
                grp[c] = np.nan
            out_parts.append(grp)

    res = pd.concat(out_parts, ignore_index=True)
    cov = res["log_oi_usdt"].notna().mean() * 100
    log(f"📊 Real Open Interest / TopTrader L/S coverage across events: {cov:.1f}%")
    return res


def train_and_evaluate(df: pd.DataFrame, side_name: str, out_path: Path) -> None:
    df = df.sort_values("date").reset_index(drop=True)
    train = df[df["date"] < "2026-07-01"]
    val = df[(df["date"] >= "2026-07-01") & (df["date"] < "2026-08-15")]
    oos = df[df["date"] >= "2026-08-15"]

    # Compare Base (OHLCV+Taker+Funding) vs Full (+Real OI & TopTrader L/S)
    for tag, feats in [("BASE (Klines+Taker+Funding)", BASE_FEATURES), ("FULL (+Real OI +TopTrader L/S)", ALL_FEATURES)]:
        model = lgb.LGBMClassifier(
            n_estimators=500,
            learning_rate=0.03,
            max_depth=4,
            num_leaves=12,
            min_child_samples=40,
            subsample=0.8,
            subsample_freq=1,
            colsample_bytree=0.7,
            reg_alpha=2.0,
            reg_lambda=10.0,
            random_state=42,
            verbose=-1,
        )
        model.fit(
            train[feats], train["label"],
            eval_set=[(val[feats], val["label"])],
            callbacks=[lgb.early_stopping(40, verbose=False)],
        )
        p_va = model.predict_proba(val[feats])[:, 1]
        p_te = model.predict_proba(oos[feats])[:, 1]
        auc_va = roc_auc_score(val["label"], p_va)
        auc_te = roc_auc_score(oos["label"], p_te)
        log(f"\n================ {side_name.upper()} AI v2 [{tag}] ================")
        log(f"Split: Train={len(train)} | Val={len(val)} (AUC={auc_va:.4f}) | OOS={len(oos)} (AUC={auc_te:.4f}) | Base OOS WR={oos['label'].mean()*100:.2f}%")
        if tag.startswith("FULL"):
            for th in [0.75, 0.80, 0.85, 0.88, 0.90, 0.92, 0.94]:
                m_va = p_va >= th
                m_te = p_te >= th
                n_te = int(m_te.sum())
                if n_te == 0:
                    continue
                wr_va = float(val.loc[m_va, "label"].mean() * 100) if m_va.sum() > 0 else 0.0
                wr_te = float(oos.loc[m_te, "label"].mean() * 100)
                avg_te = float(oos.loc[m_te, "ret_roe"].mean())
                log(f"  th>={th:.2f} | Val N={int(m_va.sum()):<4} WR={wr_va:5.2f}% | OOS N={n_te:<4} WR={wr_te:5.2f}% | OOS AvgROE={avg_te:+6.2f}%")

            imp = pd.Series(model.feature_importances_, index=feats).sort_values(ascending=False)
            log("Top 12 Features: " + ", ".join(f"{k}({v})" for k, v in imp.head(12).items()))
            payload = {
                "model": model,
                "features": feats,
                "side": side_name,
                "auc_val": auc_va,
                "auc_oos": auc_te,
                "n_pairs": 500,
                "train_end": "2026-06-30",
            }
            with open(out_path, "wb") as f:
                pickle.dump(payload, f)
            log(f"💾 Saved model -> {out_path}")


if __name__ == "__main__":
    t_start = time.time()
    syms = fetch_top_500_usdt_perps()
    log(f"📋 Selected {len(syms)} active Binance USDT-M perpetual pairs (top by 24h volume)")

    log("⬇️ Stage 0: Loading BTCUSDT macro context (12 months)...")
    btc_k, _ = load_symbol_klines_and_funding("BTCUSDT")
    btc_df = btc_k[["date"]].copy()
    btc_df["btc_ret_1h"] = btc_k["close"].pct_change(12).shift(1)
    btc_df["btc_ret_15m"] = btc_k["close"].pct_change(3).shift(1)
    btc_df["btc_rsi_5m"] = ta.RSI(btc_k, timeperiod=14).shift(1)

    log(f"🚀 Stage 1: Downloading 12-month Klines (with real Taker Buy Vol & Count) + Funding Rate & scanning candidates for {len(syms)} pairs...")
    all_l, all_s = [], []
    done = 0
    with ThreadPoolExecutor(max_workers=24) as ex:
        futs = {ex.submit(process_one_symbol, s, btc_df): s for s in syms}
        for fut in as_completed(futs):
            lr, sr = fut.result()
            if lr:
                all_l.extend(lr)
            if sr:
                all_s.extend(sr)
            done += 1
            if done % 50 == 0:
                log(f"   ... processed {done}/{len(syms)} pairs ({time.time()-t_start:.0f}s) | Long={len(all_l)} Short={len(all_s)}")

    df_l = pd.DataFrame(all_l)
    df_s = pd.DataFrame(all_s)
    log(f"✅ Stage 1 done in {(time.time()-t_start)/60:.2f} min | Long={len(df_l)} (base WR={df_l['label'].mean()*100:.2f}%) | Short={len(df_s)} (base WR={df_s['label'].mean()*100:.2f}%)")

    # Combine for unified Stage 2 metrics fetch (deduplicated across Long & Short!)
    df_l["side"] = "long"
    df_s["side"] = "short"
    df_both = pd.concat([df_l, df_s], ignore_index=True)
    df_both = enrich_with_metrics(df_both)
    df_both.to_parquet(WORK_DIR / "mm_500pairs_dataset.parquet", index=False)

    df_l_enr = df_both[df_both["side"] == "long"].reset_index(drop=True)
    df_s_enr = df_both[df_both["side"] == "short"].reset_index(drop=True)

    train_and_evaluate(df_l_enr, "long", MODELS_DIR / "mm_long_gatekeeper_v2_500p.pkl")
    train_and_evaluate(df_s_enr, "short", MODELS_DIR / "mm_short_gatekeeper_v2_500p.pkl")

    # Upload trained v2 models to R2 for persistence
    R2 = boto3.client(
        "s3",
        endpoint_url="https://a52481108c8613c521b7670d797d8848.r2.cloudflarestorage.com",
        aws_access_key_id="0da5c6eb0ad37511c20061f4217197f0",
        aws_secret_access_key="aeb545c076f75b051be1128efd91fe7e47bd6d042fe9577e3b19fb0bf6e218c4",
        region_name="auto",
        config=Config(signature_version="s3v4"),
    )
    for fn in ["mm_long_gatekeeper_v2_500p.pkl", "mm_short_gatekeeper_v2_500p.pkl"]:
        R2.upload_file(str(MODELS_DIR / fn), "goclaw-data", f"botx8_cache/models/{fn}")
    log(f"🏁 Total pipeline finished in {(time.time()-t_start)/60:.2f} min & models uploaded to R2!")
