import pandas as pd
import numpy as np

def main():
    # Let's inspect features in backtest zip
    import zipfile, json
    from pathlib import Path

    backtest_dir = Path("user_data/backtest_results")
    zip_files = sorted(list(backtest_dir.glob("backtest-result-*.zip")), key=lambda p: p.stat().st_mtime, reverse=True)
    with zipfile.ZipFile(zip_files[0]) as z:
        for name in z.namelist():
            if name.endswith(".json") and not name.endswith(".meta.json") and not name.endswith("_config.json"):
                data = json.loads(z.read(name).decode("utf-8"))
                strat_key = list(data.get("strategy", data).keys())[0]
                trades = data.get("strategy", data)[strat_key].get("trades", [])
                break

    for t in trades:
        if 'MSTR' in t['pair'] and '2026-07-01' in t['open_date']:
            print("MSTR trade:", json.dumps(t, indent=2))

if __name__ == '__main__':
    main()
