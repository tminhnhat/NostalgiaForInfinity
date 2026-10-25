#!/usr/bin/env python3
"""Offline Markets Patch for Freqtrade.

Bypasses Binance US IP geo-restrictions (HTTP 451) on cloud runners (GitHub Actions / Colab)
by loading pre-cached markets from user_data/markets_binance_futures.pkl.gz.
"""

import gzip
import os
import pickle
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def apply_patch():
    try:
        import freqtrade.exchange.exchange as fe
    except ImportError:
        print("⚠️ freqtrade not installed in current environment. Skipping patch.")
        return

    fe_file = fe.__file__
    with open(fe_file, "r", encoding="utf-8") as f:
        code = f.read()

    if "OFFLINE MARKETS PATCH" in code:
        print("✅ Offline Markets Patch already applied.")
        return

    patch_code = """
        # --- OFFLINE MARKETS PATCH ---
        import os, pickle, gzip
        for _p in [
            os.path.join(self._config.get('user_data_dir', 'user_data'), 'markets_binance_futures.pkl.gz'),
            'user_data/markets_binance_futures.pkl.gz',
        ]:
            if os.path.exists(_p):
                with gzip.open(_p, 'rb') as _f:
                    _m = pickle.load(_f)
                self._api_async.markets = _m
                self._api_async.set_markets(_m)
                return None
        # -----------------------------
"""

    target = "    def _load_async_markets(self, reload: bool = False) -> None:\n        try:"
    replacement = "    def _load_async_markets(self, reload: bool = False) -> None:" + patch_code + "        try:"

    if target in code:
        code = code.replace(target, replacement)
        with open(fe_file, "w", encoding="utf-8") as f:
            f.write(code)
        print("✅ Successfully applied Offline Markets Patch to Freqtrade exchange!")
    else:
        print("⚠️ Target signature not found in freqtrade exchange. Code might be different version.")


if __name__ == "__main__":
    apply_patch()
