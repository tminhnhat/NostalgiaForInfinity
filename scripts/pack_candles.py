#!/usr/bin/env python3
"""Pack Feather Candles for Colab / Cloud Transfer.

Packs user_data/data/binance/futures/*.feather into a single compressed tar.gz
bundle (~100-150MB) for 5-second 1-click transfer to Google Drive / Colab.
"""

from __future__ import annotations

import os
from pathlib import Path
import sys
import tarfile
import time

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def main():
    src_dir = Path("user_data/data/binance/futures")
    output_tar = Path("user_data/binance_candles_185d.tar.gz")

    if not src_dir.exists():
        print(f"❌ Không tìm thấy thư mục nến tại: {src_dir}")
        return 1

    feather_files = list(src_dir.glob("*.feather"))
    if not feather_files:
        print(f"❌ Không tìm thấy file .feather nào trong: {src_dir}")
        return 1

    print(f"📦 Tìm thấy {len(feather_files)} file nến .feather")
    print(f"⏳ Đang nén thành tệp duy nhất: {output_tar}...")

    t0 = time.time()
    with tarfile.open(output_tar, "w:gz") as tar:
        for f in feather_files:
            tar.add(f, arcname=f"futures/{f.name}")

    elapsed = time.time() - t0
    size_mb = output_tar.stat().st_size / (1024 * 1024)
    print(f"🎉 Hoàn tất trong {elapsed:.1f}s!")
    print(f"📁 Dung lượng file nén: {size_mb:.2f} MB")
    print(f"👉 Vị trí: {output_tar.resolve()}")
    print("\n💡 HƯỚNG DẪN DÙNG TRÊN GOOGLE COLAB:")
    print("1. Kéo thả file 'binance_candles_185d.tar.gz' này lên Google Drive vào thư mục: botx8_cache/")
    print("2. Khi chạy Colab, notebook sẽ giải nén nến chỉ trong 3-5 giây (thay vì tải 15-20 phút)!")
    return 0


if __name__ == "__main__":
    sys.exit(main())

