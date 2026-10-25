#!/usr/bin/env python3
"""Binance Vision to Cloudflare R2 Ingestion Engine.

Downloads daily klines from data.binance.vision (bypassing US IP geo-restrictions),
converts them into compressed Parquet files compatible with Freqtrade,
and syncs them to Cloudflare R2 via rclone.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import io
import json
import logging
import os
from pathlib import Path
import subprocess
import sys
import urllib.request
import zipfile

import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("R2Ingestion")

BINANCE_VISION_BASE = "https://data.binance.vision/data/{market}/daily/klines/{pair}/{timeframe}/{pair}-{timeframe}-{date}.zip"

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
            "pairs": ["BTC/USDT", "ETH/USDT", "SOL/USDT"],
            "r2_bucket": "freqtrade-data",
            "r2_prefix": "binance",
        }
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def download_daily_kline(pair_raw: str, timeframe: str, target_date: str, market: str = "spot") -> pd.DataFrame | None:
    pair_clean = pair_raw.replace("/", "").replace(":", "")
    url = BINANCE_VISION_BASE.format(
        market=market,
        pair=pair_clean,
        timeframe=timeframe,
        date=target_date,
    )
    logger.debug(f"Fetching: {url}")
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            content = response.read()
            with zipfile.ZipFile(io.BytesIO(content)) as z:
                csv_files = [f for f in z.namelist() if f.endswith(".csv")]
                if not csv_files:
                    return None
                with z.open(csv_files[0]) as csv_file:
                    df = pd.read_csv(csv_file, header=None, names=CSV_COLUMNS)
                    return df
    except urllib.error.HTTPError as e:
        if e.code == 404:
            logger.debug(f"No archive available for {pair_raw} {timeframe} {target_date} (404)")
        else:
            logger.warning(f"HTTP {e.code} while fetching {url}")
        return None
    except Exception as e:
        logger.error(f"Error downloading {url}: {e}")
        return None


def format_for_freqtrade(df: pd.DataFrame) -> pd.DataFrame:
    """Format raw Binance Vision CSV to Freqtrade standard parquet format."""
    out = pd.DataFrame()
    # Dynamic timestamp unit auto-detection (handles s, ms, us, ns)
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


def update_parquet_file(file_path: Path, new_df: pd.DataFrame):
    """Merge new candles into existing Parquet file, deduplicating by date."""
    if file_path.exists():
        try:
            existing_df = pd.read_parquet(file_path)
            combined = pd.concat([existing_df, new_df], ignore_index=True)
            combined = combined.drop_duplicates(subset=["date"]).sort_values(by="date")
        except Exception as e:
            logger.warning(f"Could not read existing {file_path}: {e}. Overwriting.")
            combined = new_df
    else:
        combined = new_df

    file_path.parent.mkdir(parents=True, exist_ok=True)
    combined.to_parquet(file_path, compression="snappy", index=False)
    logger.info(f"Updated {file_path.name} (total candles: {len(combined)})")


def sync_to_r2(local_dir: Path, bucket: str, prefix: str):
    """Sync processed parquet files to Cloudflare R2 using rclone."""
    remote_dest = f"r2:{bucket}/{prefix}"
    logger.info(f"Syncing local directory {local_dir} to Cloudflare R2 -> {remote_dest}")
    cmd = [
        "rclone",
        "sync",
        str(local_dir),
        remote_dest,
        "--fast-list",
        "--transfers=8",
        "-v",
    ]
    try:
        res = subprocess.run(cmd, check=True, capture_output=True, text=True)
        logger.info(f"RClone sync successful: {res.stdout.strip()}")
    except FileNotFoundError:
        logger.error("rclone command not found. Ensure rclone is installed in PATH.")
    except subprocess.CalledProcessError as e:
        logger.error(f"rclone failed (code {e.returncode}): {e.stderr}")


def main():
    parser = argparse.ArgumentParser(description="Ingest Binance candles to Cloudflare R2")
    parser.add_argument("--config", type=Path, default=Path("configs/r2_sync_pairs.json"))
    parser.add_argument("--output-dir", type=Path, default=Path("user_data/data/binance"))
    parser.add_argument("--days", type=int, default=2, help="Days of history to fetch (default: last 2 days)")
    parser.add_argument("--target-date", type=str, default=None, help="Specific date YYYY-MM-DD")
    parser.add_argument("--sync", action="store_true", help="Sync output directory to Cloudflare R2 via rclone")
    args = parser.parse_args()

    cfg = load_config(args.config)
    market = cfg.get("market_type", "spot")
    pairs = cfg.get("pairs", [])
    timeframes = cfg.get("timeframes", ["5m", "15m", "1h", "4h", "1d"])
    bucket = cfg.get("r2_bucket", "freqtrade-data")
    prefix = cfg.get("r2_prefix", "binance")

    now_utc = datetime.now(timezone.utc)
    if args.target_date:
        dates_to_fetch = [args.target_date]
    else:
        # Fetch target days (Binance Vision posts full day daily archives usually 1-2 days ago)
        dates_to_fetch = [
            (now_utc - timedelta(days=d)).strftime("%Y-%m-%d")
            for d in range(1, args.days + 1)
        ]

    logger.info(f"Target dates: {dates_to_fetch}")
    logger.info(f"Pairs ({len(pairs)}): {pairs}")
    logger.info(f"Timeframes: {timeframes}")

    for pair in pairs:
        pair_filename_base = pair.replace("/", "_").replace(":", "_")
        for tf in timeframes:
            combined_dfs = []
            for dt in dates_to_fetch:
                df = download_daily_kline(pair, tf, dt, market=market)
                if df is not None and not df.empty:
                    combined_dfs.append(format_for_freqtrade(df))

            if combined_dfs:
                new_data = pd.concat(combined_dfs, ignore_index=True)
                target_file = args.output_dir / f"{pair_filename_base}-{tf}.parquet"
                update_parquet_file(target_file, new_data)

    if args.sync:
        sync_to_r2(args.output_dir, bucket, prefix)

    logger.info("Ingestion completed successfully.")


if __name__ == "__main__":
    main()
