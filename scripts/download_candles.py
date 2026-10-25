#!/usr/bin/env python3
"""Binance Vision Candle Downloader for Freqtrade.

Downloads daily kline archives directly from data.binance.vision (no API keys,
no US IP geo-restrictions), formats them for Freqtrade, and writes compressed
Parquet files directly to user_data/data/binance/.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone
import io
import json
import logging
import os
from pathlib import Path
import sys
import urllib.error
import urllib.request
import zipfile

import pandas as pd

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("CandleDownloader")

BINANCE_VISION_URL = (
    "https://data.binance.vision/data/{market}/daily/klines/{pair}/{timeframe}/{pair}-{timeframe}-{date}.zip"
)

CSV_COLUMNS = [
    "open_time",
    "open",
    "high",
    "low",
    "close",
    "volume",
    "close_time",
    "quote_volume",
    "count",
    "taker_buy_volume",
    "taker_buy_quote_volume",
    "ignore",
]


def load_config(config_path: Path) -> dict:
    if not config_path.exists():
        logger.warning(f"Config file {config_path} not found. Using defaults.")
        return {
            "exchange": "binance",
            "market_type": "spot",
            "timeframes": ["5m", "15m", "1h", "4h", "1d"],
            "pairs": ["BTC/USDT", "ETH/USDT", "BNB/USDT", "SOL/USDT"],
        }
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def download_single_day(
    pair: str, timeframe: str, date_str: str, market: str
) -> pd.DataFrame | None:
    pair_clean = pair.replace("/", "").replace(":", "")
    url = BINANCE_VISION_URL.format(
        market=market,
        pair=pair_clean,
        timeframe=timeframe,
        date=date_str,
    )
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            content = resp.read()
            with zipfile.ZipFile(io.BytesIO(content)) as z:
                csvs = [f for f in z.namelist() if f.endswith(".csv")]
                if not csvs:
                    return None
                with z.open(csvs[0]) as csv_file:
                    df = pd.read_csv(csv_file, header=None, names=CSV_COLUMNS)
                    return format_for_freqtrade(df)
    except urllib.error.HTTPError as e:
        if e.code != 404:
            logger.debug(f"HTTP {e.code} for {pair} {timeframe} {date_str}")
        return None
    except Exception as e:
        logger.debug(f"Fetch failed for {url}: {e}")
        return None


def format_for_freqtrade(df: pd.DataFrame) -> pd.DataFrame:
    out = pd.DataFrame()
    ts = pd.to_numeric(df["open_time"], errors="coerce")
    sample_val = ts.dropna().iloc[0] if not ts.dropna().empty else 0
    if sample_val > 1e16:
        unit = "ns"
    elif sample_val > 1e13:
        unit = "us"
    elif sample_val > 1e10:
        unit = "ms"
    else:
        unit = "s"

    out["date"] = pd.to_datetime(ts, unit=unit, utc=True)
    out["open"] = df["open"].astype("float64")
    out["high"] = df["high"].astype("float64")
    out["low"] = df["low"].astype("float64")
    out["close"] = df["close"].astype("float64")
    out["volume"] = df["volume"].astype("float64")
    return out


def process_pair_timeframe(
    pair: str,
    tf: str,
    dates: list[str],
    market: str,
    output_dir: Path,
    max_workers: int = 8,
):
    target_file = output_dir / f"{pair_filename_base}-{tf}.parquet"
    target_feather = output_dir / f"{pair_filename_base}-{tf}.feather"

    dfs = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(download_single_day, pair, tf, dt, market): dt
            for dt in dates
        }
        for future in as_completed(futures):
            res = future.result()
            if res is not None and not res.empty:
                dfs.append(res)

    if not dfs:
        logger.warning(f"No candles downloaded for {pair} {tf}")
        return

    new_data = pd.concat(dfs, ignore_index=True)

    if target_file.exists():
        try:
            existing = pd.read_parquet(target_file)
            combined = pd.concat([existing, new_data], ignore_index=True)
            combined = combined.drop_duplicates(subset=["date"]).sort_values(by="date")
        except Exception:
            combined = new_data.drop_duplicates(subset=["date"]).sort_values(by="date")
    else:
        combined = new_data.drop_duplicates(subset=["date"]).sort_values(by="date")

    target_file.parent.mkdir(parents=True, exist_ok=True)
    combined.to_parquet(target_file, compression="snappy", index=False)
    try:
        combined.to_feather(target_feather)
    except Exception as e:
        logger.debug(f"Could not save feather: {e}")
    logger.info(f"Saved {target_file.name} (candles: {len(combined)})")


def main():
    parser = argparse.ArgumentParser(description="Download Binance candles for Freqtrade")
    parser.add_argument("--config", type=Path, default=Path("configs/eval_pairs.json"))
    parser.add_argument("--output-dir", type=Path, default=Path("user_data/data/binance"))
    parser.add_argument("--days", type=int, default=30, help="Days of history to download")
    parser.add_argument("--workers", type=int, default=12, help="Parallel download threads")
    args = parser.parse_args()

    cfg = load_config(args.config)
    market = cfg.get("market_type", "spot")
    pairs = cfg.get("pairs", [])
    timeframes = cfg.get("timeframes", ["5m", "15m", "1h", "4h", "1d"])

    now_utc = datetime.now(timezone.utc)
    dates_to_fetch = [
        (now_utc - timedelta(days=d)).strftime("%Y-%m-%d")
        for d in range(1, args.days + 1)
    ]

    logger.info(f"Starting download for {len(pairs)} pairs across {len(timeframes)} timeframes ({args.days} days)...")
    args.output_dir.mkdir(parents=True, exist_ok=True)

    for pair in pairs:
        for tf in timeframes:
            process_pair_timeframe(
                pair=pair,
                tf=tf,
                dates=dates_to_fetch,
                market=market,
                output_dir=args.output_dir,
                max_workers=args.workers,
            )

    parquet_count = len(list(args.output_dir.glob("*.parquet")))
    logger.info(f"Download completed successfully. {parquet_count} parquet files in {args.output_dir}")


if __name__ == "__main__":
    main()
