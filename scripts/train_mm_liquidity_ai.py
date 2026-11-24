# -*- coding: utf-8 -*-
"""
Train AI Meta-Labeling Gatekeepers (LightGBM) for Market Maker / Liquidity Heatmap / Order Flow
Long & Short Signals (6x leverage, Triple-Barrier Labeling, Strict Chronological Train/Val/OOS Split).
"""
from __future__ import annotations

import json
import os
import pickle
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd

def log(m: str) -> None:
    print(m, flush=True)

# Ensure lightgbm & scikit-learn installed on Colab
for mod, pkg in [("lightgbm", "lightgbm"), ("sklearn", "scikit-learn")]:
    try:
        __import__(mod)
    except ImportError:
        log(f"📦 Installing {pkg}...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", pkg], check=True)

import lightgbm as lgb
from sklearn.metrics import roc_auc_score
import talib.abstract as ta

REPO_DIR = Path("/content/NostalgiaForInfinity")
os.chdir(REPO_DIR)

DEST_DIR = REPO_DIR / "user_data/data/binance/futures"
MODELS_DIR = REPO_DIR / "user_data/models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)

cfg = json.loads((REPO_DIR / "configs/backtest_config.json").read_text())
PAIRS: List[str] = cfg["exchange"]["pair_whitelist"]

FEATURES: List[str] = [
    "mm_lower_wick_ratio",
    "mm_upper_wick_ratio",
    "mm_body_pct",
    "mm_atr_pct",
    "mm_range_atr",
    "mm_rvol",
    "mm_absorption",
    "mm_log_qvol_1h",
    "mm_buy_ratio",
    "mm_bar_delta_norm",
    "mm_cvd_12_norm",
    "mm_cvd_48_norm",
    "mm_cvd_div_long",
    "mm_cvd_div_short",
    "mm_mfi_14",
    "mm_cmf_20",
    "mm_vwap_z_4h",
    "mm_vwap_z_24h",
    "mm_dist_vwap_24h",
    "mm_dist_swing_low_24h",
    "mm_dist_swing_high_24h",
    "mm_rsi_5m",
    "mm_rsi_15m",
    "mm_rsi_1h",
    "mm_dist_ema200_1h",
    "mm_ema50_slope_1h",
    "btc_ret_15m_btc",
    "btc_ret_1h_btc",
    "btc_rsi_5m_btc",
]


def load_feather(pair: str, tf: str) -> pd.DataFrame:
    pb = pair.replace("/", "_").replace(":", "_")
    fp = DEST_DIR / f"{pb}-{tf}-futures.feather"
    if not fp.exists():
        return pd.DataFrame()
    df = pd.read_feather(fp)
    df["date"] = pd.to_datetime(df["date"], utc=True)
    return df.sort_values("date").reset_index(drop=True)


def merge_inf(df_5m: pd.DataFrame, df_inf: pd.DataFrame, suffix: str) -> pd.DataFrame:
    if df_inf is None or len(df_inf) == 0:
        return df_5m
    inf = df_inf.copy()
    cols = [c for c in inf.columns if c != "date"]
    inf[cols] = inf[cols].shift(1)
    ren = {c: f"{c}_{suffix}" for c in cols}
    inf = inf.rename(columns=ren)
    return pd.merge_asof(df_5m, inf[["date"] + list(ren.values())], on="date", direction="backward")


def compute_features(df: pd.DataFrame, inf_15m: pd.DataFrame, inf_1h: pd.DataFrame, btc_5m: pd.DataFrame) -> pd.DataFrame:
    eps = 1e-10
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
    df["mm_buy_ratio"] = ((df["close"] - df["low"]) / candle_range).clip(0.0, 1.0)
    df["mm_sell_ratio"] = 1.0 - df["mm_buy_ratio"]
    df["mm_bar_delta"] = df["volume"] * (df["mm_buy_ratio"] - df["mm_sell_ratio"])

    vol_ma_48 = df["volume"].rolling(48, min_periods=10).mean().clip(lower=eps)
    df["mm_rvol"] = df["volume"] / vol_ma_48
    df["mm_bar_delta_norm"] = df["mm_bar_delta"] / vol_ma_48
    df["mm_cvd_12"] = df["mm_bar_delta"].rolling(12, min_periods=1).sum()
    df["mm_cvd_48"] = df["mm_bar_delta"].rolling(48, min_periods=1).sum()
    df["mm_cvd_12_norm"] = df["mm_cvd_12"] / (vol_ma_48 * 12.0)
    df["mm_cvd_48_norm"] = df["mm_cvd_48"] / (vol_ma_48 * 48.0)

    qvol_1h = (df["volume"] * df["close"]).rolling(12, min_periods=1).sum()
    df["mm_quote_vol_1h"] = qvol_1h
    df["mm_log_qvol_1h"] = np.log1p(qvol_1h.clip(lower=0.0))

    df["mm_absorption"] = df["mm_rvol"] / np.maximum(df["mm_body_pct"] / df["mm_atr_pct"], 0.25)
    df["mm_mfi_14"] = ta.MFI(df, timeperiod=14)
    mfm = ((df["close"] - df["low"]) - (df["high"] - df["close"])) / candle_range
    df["mm_cmf_20"] = (mfm * df["volume"]).rolling(20, min_periods=5).sum() / df["volume"].rolling(20, min_periods=5).sum().clip(lower=eps)

    typical = (df["high"] + df["low"] + df["close"]) / 3.0
    pv = typical * df["volume"]
    df["mm_vwap_4h"] = pv.rolling(48, min_periods=12).sum() / df["volume"].rolling(48, min_periods=12).sum().clip(lower=eps)
    df["mm_vwap_24h"] = pv.rolling(288, min_periods=24).sum() / df["volume"].rolling(288, min_periods=24).sum().clip(lower=eps)

    std_4h = (df["close"] - df["mm_vwap_4h"]).rolling(48, min_periods=12).std().clip(lower=eps)
    std_24h = (df["close"] - df["mm_vwap_24h"]).rolling(288, min_periods=24).std().clip(lower=eps)
    df["mm_vwap_z_4h"] = (df["close"] - df["mm_vwap_4h"]) / std_4h
    df["mm_vwap_z_24h"] = (df["close"] - df["mm_vwap_24h"]) / std_24h
    df["mm_dist_vwap_24h"] = (df["close"] - df["mm_vwap_24h"]) / df["mm_vwap_24h"].clip(lower=eps)

    df["mm_swing_low_24h"] = df["low"].rolling(288, min_periods=48).min().shift(1)
    df["mm_swing_high_24h"] = df["high"].rolling(288, min_periods=48).max().shift(1)
    df["mm_dist_swing_low_24h"] = (df["close"] - df["mm_swing_low_24h"]) / df["close"].clip(lower=eps)
    df["mm_dist_swing_high_24h"] = (df["mm_swing_high_24h"] - df["close"]) / df["close"].clip(lower=eps)

    prev_cvd_low_48 = df["mm_cvd_48"].rolling(48, min_periods=12).min().shift(3)
    prev_cvd_high_48 = df["mm_cvd_48"].rolling(48, min_periods=12).max().shift(3)
    df["mm_cvd_div_long"] = (df["mm_cvd_48"] - prev_cvd_low_48) / (vol_ma_48 * 48.0)
    df["mm_cvd_div_short"] = (prev_cvd_high_48 - df["mm_cvd_48"]) / (vol_ma_48 * 48.0)

    if len(inf_15m) > 20:
        i15 = inf_15m.copy()
        i15["mm_rsi"] = ta.RSI(i15, timeperiod=14)
        df = merge_inf(df, i15[["date", "mm_rsi"]], "15m")
    else:
        df["mm_rsi_15m"] = 50.0

    if len(inf_1h) > 50:
        i1h = inf_1h.copy()
        i1h["mm_rsi"] = ta.RSI(i1h, timeperiod=14)
        i1h["mm_ema50"] = ta.EMA(i1h, timeperiod=50)
        i1h["mm_ema200"] = ta.EMA(i1h, timeperiod=200)
        i1h["mm_ema50_slope"] = (i1h["mm_ema50"] - i1h["mm_ema50"].shift(4)) / i1h["mm_ema50"].shift(4).clip(lower=eps)
        df = merge_inf(df, i1h[["date", "mm_rsi", "mm_ema200", "mm_ema50_slope"]], "1h")
        df["mm_dist_ema200_1h"] = (df["close"] - df["mm_ema200_1h"]) / df["mm_ema200_1h"].clip(lower=eps)
    else:
        df["mm_rsi_1h"] = 50.0
        df["mm_dist_ema200_1h"] = 0.0
        df["mm_ema50_slope_1h"] = 0.0

    df = merge_inf(df, btc_5m, "btc")
    return df


def triple_barrier_label(
    opens: np.ndarray,
    highs: np.ndarray,
    lows: np.ndarray,
    closes: np.ndarray,
    idx: int,
    is_short: bool,
    tp_spot: float = 0.0135,   # +8.1% gross / ~+7.5% net ROE at 6x
    sl_spot: float = 0.055,    # -33.0% ROE at 6x
    horizon: int = 576,        # 48h on 5m
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


def build_dataset() -> Tuple[pd.DataFrame, pd.DataFrame]:
    t0 = time.time()
    btc_raw = load_feather("BTC/USDT:USDT", "5m")
    btc_5m = btc_raw[["date"]].copy()
    btc_5m["btc_ret_1h"] = btc_raw["close"].pct_change(12)
    btc_5m["btc_ret_15m"] = btc_raw["close"].pct_change(3)
    btc_5m["btc_rsi_5m"] = ta.RSI(btc_raw, timeperiod=14)

    long_rows = []
    short_rows = []

    for pair in PAIRS:
        df5 = load_feather(pair, "5m")
        if len(df5) < 500:
            continue
        df15 = load_feather(pair, "15m")
        df1h = load_feather(pair, "1h")
        df = compute_features(df5, df15, df1h, btc_5m)
        df = df[(df["date"] >= "2025-11-21") & (df["date"] <= "2026-11-21")].reset_index(drop=True)
        if len(df) < 400:
            continue

        # Broad Market Maker Liquidity Sweep / Overextension Candidates
        has_liq = (df["volume"] > 0) & (df["mm_quote_vol_1h"] >= 250_000.0)
        cand_long = (
            has_liq
            & (df["mm_vwap_z_24h"] <= -2.0)
            & (df["mm_rsi_15m"] < 38.0)
            & (df["mm_rvol"] >= 1.8)
            & ((df["mm_lower_wick_ratio"] >= 0.35) | (df["mm_buy_ratio"] >= 0.58))
        )
        cand_short = (
            has_liq
            & (df["mm_vwap_z_24h"] >= 2.0)
            & (df["mm_rsi_15m"] > 62.0)
            & (df["mm_rvol"] >= 1.8)
            & ((df["mm_upper_wick_ratio"] >= 0.35) | (df["mm_sell_ratio"] >= 0.58))
        )

        opens = df["open"].to_numpy()
        highs = df["high"].to_numpy()
        lows = df["low"].to_numpy()
        closes = df["close"].to_numpy()
        dates = df["date"].to_numpy()

        # De-duplicate with 24-bar (2h) cooldown per pair/side
        last_l = -100
        for idx in np.flatnonzero(cand_long.to_numpy()):
            if idx - last_l < 24:
                continue
            lbl, ret = triple_barrier_label(opens, highs, lows, closes, int(idx), is_short=False)
            if lbl < 0:
                continue
            last_l = int(idx)
            row = {f: float(df.at[idx, f]) if pd.notna(df.at[idx, f]) else np.nan for f in FEATURES}
            row["date"] = dates[idx]
            row["pair"] = pair
            row["label"] = lbl
            row["ret_roe"] = ret
            long_rows.append(row)

        last_s = -100
        for idx in np.flatnonzero(cand_short.to_numpy()):
            if idx - last_s < 24:
                continue
            lbl, ret = triple_barrier_label(opens, highs, lows, closes, int(idx), is_short=True)
            if lbl < 0:
                continue
            last_s = int(idx)
            row = {f: float(df.at[idx, f]) if pd.notna(df.at[idx, f]) else np.nan for f in FEATURES}
            row["date"] = dates[idx]
            row["pair"] = pair
            row["label"] = lbl
            row["ret_roe"] = ret
            short_rows.append(row)

    df_l = pd.DataFrame(long_rows)
    df_s = pd.DataFrame(short_rows)
    log(f"✅ Dataset built in {time.time()-t0:.1f}s | Long candidates={len(df_l)} (base WR={df_l['label'].mean()*100:.2f}%) | Short candidates={len(df_s)} (base WR={df_s['label'].mean()*100:.2f}%)")
    return df_l, df_s


def train_and_eval(df: pd.DataFrame, side_name: str, out_path: Path) -> Dict:
    df = df.sort_values("date").reset_index(drop=True)
    df["date"] = pd.to_datetime(df["date"], utc=True)

    train = df[df["date"] < "2026-06-20"]
    val = df[(df["date"] >= "2026-06-20") & (df["date"] < "2026-08-20")]
    oos = df[df["date"] >= "2026-08-20"]

    X_tr, y_tr = train[FEATURES], train["label"]
    X_va, y_va = val[FEATURES], val["label"]
    X_te, y_te = oos[FEATURES], oos["label"]

    model = lgb.LGBMClassifier(
        n_estimators=400,
        learning_rate=0.03,
        max_depth=4,
        num_leaves=10,
        min_child_samples=40,
        subsample=0.8,
        subsample_freq=1,
        colsample_bytree=0.7,
        reg_alpha=2.0,
        reg_lambda=8.0,
        random_state=42,
        verbose=-1,
    )
    model.fit(
        X_tr, y_tr,
        eval_set=[(X_va, y_va)],
        callbacks=[lgb.early_stopping(40, verbose=False)],
    )

    p_va = model.predict_proba(X_va)[:, 1]
    p_te = model.predict_proba(X_te)[:, 1]
    auc_va = roc_auc_score(y_va, p_va)
    auc_te = roc_auc_score(y_te, p_te)
    log(f"\n================ {side_name.upper()} AI GATEKEEPER ================")
    log(f"Split sizes: Train={len(train)} | Val={len(val)} (AUC={auc_va:.4f}) | OOS Test={len(oos)} (AUC={auc_te:.4f})")

    log("Threshold sweep on PURE OUT-OF-SAMPLE (2026-08-20 -> 2026-11-21):")
    best_th = 0.85
    for th in [0.70, 0.75, 0.80, 0.85, 0.88, 0.90, 0.92]:
        m_va = p_va >= th
        m_te = p_te >= th
        n_te = int(m_te.sum())
        if n_te == 0:
            log(f"  th>={th:.2f} | OOS N=0")
            continue
        wr_va = float(y_va[m_va].mean() * 100) if m_va.sum() > 0 else 0.0
        wr_te = float(y_te[m_te].mean() * 100)
        avg_te = float(oos.loc[m_te, "ret_roe"].mean())
        log(f"  th>={th:.2f} | Val N={int(m_va.sum()):<4} WR={wr_va:5.2f}% | OOS N={n_te:<4} WR={wr_te:5.2f}% | OOS AvgROE={avg_te:+6.2f}%")

    # Top 10 feature importances
    imp = pd.Series(model.feature_importances_, index=FEATURES).sort_values(ascending=False)
    log("Top 10 Features: " + ", ".join(f"{k}({v})" for k, v in imp.head(10).items()))

    payload = {
        "model": model,
        "features": FEATURES,
        "side": side_name,
        "auc_val": auc_va,
        "auc_oos": auc_te,
        "train_end": "2026-06-20",
    }
    with open(out_path, "wb") as f:
        pickle.dump(payload, f)
    log(f"💾 Saved model -> {out_path}")
    return payload


if __name__ == "__main__":
    df_l, df_s = build_dataset()
    train_and_eval(df_l, "long", MODELS_DIR / "mm_long_gatekeeper_v1.pkl")
    train_and_eval(df_s, "short", MODELS_DIR / "mm_short_gatekeeper_v1.pkl")
