#!/usr/bin/env python3
"""Binance Vision Candle Downloader for Freqtrade.

Downloads daily kline archives directly from data.binance.vision (no API keys,
no US IP geo-restrictions), formats them for Freqtrade (supporting both Futures and Spot),
and writes compressed Feather & Parquet files directly to user_data/data/binance/.
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
            "trading_mode": "futures",
            "exchange": {"name": "binance", "pair_whitelist": ["BTC/USDT:USDT", "ETH/USDT:USDT"]},
        }
    with open(config_path, "r", encoding="utf-8") as f:
        # Support JSON files that might have comments
        content = f.read()
        lines = [line for line in content.splitlines() if not line.strip().startswith("//")]
        return json.loads("\n".join(lines))


def download_single_day(
    pair: str, timeframe: str, date_str: str, market: str
) -> pd.DataFrame | None:
    pair_clean = pair.split(":")[0].replace("/", "")
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
                    first_line = csv_file.readline().decode("utf-8", errors="ignore")
                    csv_file.seek(0)
                    if "open_time" in first_line:
                        df = pd.read_csv(csv_file)
                    else:
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
    is_futures: bool = False,
    max_workers: int = 8,
):
    pair_filename_base = pair.replace("/", "_").replace(":", "_")
    target_dir = output_dir / "futures" if is_futures else output_dir
    suffix = "-futures" if is_futures else ""
    target_file = target_dir / f"{pair_filename_base}-{tf}{suffix}.parquet"
    target_feather = target_dir / f"{pair_filename_base}-{tf}{suffix}.feather"

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

    target_dir.mkdir(parents=True, exist_ok=True)
    combined.to_parquet(target_file, compression="snappy", index=False)
    try:
        combined.to_feather(target_feather)
    except Exception as e:
        logger.debug(f"Could not save feather: {e}")
    logger.info(f"Saved {target_feather.name} (candles: {len(combined)})")


def main():
    parser = argparse.ArgumentParser(description="Download Binance candles for Freqtrade")
    parser.add_argument("--config", type=Path, default=Path("configs/backtest_config.json"))
    parser.add_argument("--output-dir", type=Path, default=Path("user_data/data/binance"))
    parser.add_argument("--days", type=int, default=30, help="Days of history to download")
    parser.add_argument("--workers", type=int, default=16, help="Parallel download threads")
    args = parser.parse_args()

    cfg = load_config(args.config)
    trading_mode = cfg.get("trading_mode", cfg.get("market_type", "spot"))
    is_futures = (trading_mode == "futures")
    market = "futures/um" if is_futures else "spot"

    pairs = cfg.get("exchange", {}).get("pair_whitelist", []) or cfg.get("pairs", [])
    timeframes = list(dict.fromkeys([cfg.get("timeframe", "5m"), "15m", "1h", "4h", "1d"]))

    now_utc = datetime.now(timezone.utc)
    dates_to_fetch = [
        (now_utc - timedelta(days=d)).strftime("%Y-%m-%d")
        for d in range(1, args.days + 1)
    ]

    logger.info(f"Configuration: mode={trading_mode}, market={market}")
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
                is_futures=is_futures,
                max_workers=args.workers,
            )

    target_dir = args.output_dir / "futures" if is_futures else args.output_dir
    feather_count = len(list(target_dir.glob("*.feather")))
    parquet_count = len(list(target_dir.glob("*.parquet")))
    logger.info(f"Download completed successfully. {feather_count} feather & {parquet_count} parquet files in {target_dir}")


if __name__ == "__main__":
    main()
