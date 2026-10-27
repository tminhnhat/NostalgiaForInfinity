import zipfile, json
from pathlib import Path

def main():
    backtest_dir = Path("user_data/backtest_results")
    zip_files = sorted(list(backtest_dir.glob("backtest-result-*.zip")), key=lambda p: p.stat().st_mtime, reverse=True)
    if not zip_files:
        return
    result_zip = zip_files[0]
    
    with zipfile.ZipFile(result_zip) as z:
        for name in z.namelist():
            if name.endswith(".json") and not name.endswith(".meta.json") and not name.endswith("_config.json"):
                data = json.loads(z.read(name).decode("utf-8"))
                strat_key = list(data.get("strategy", data).keys())[0]
                trades = data.get("strategy", data)[strat_key].get("trades", [])
                break

    t702 = [t for t in trades if "702 703 731_AI_PASS" == (t.get("enter_tag") or "").strip()]
    print(f"Total trades for 702 703 731_AI_PASS: {len(t702)}")
    print(f"{'#':<3} | {'Pair':<8} | {'Duration':<8} | {'ROE%':<7} | {'MFE(5x)%':<9} | {'MAE(5x)%':<9} | {'Profit USDT':<12} | {'Exit Reason':<32}")
    print("-" * 115)
    total_roe = 0.0
    total_usdt = 0.0
    for i, t in enumerate(t702, 1):
        pair = t['pair'].split('/')[0]
        roe = float(t.get('profit_ratio', 0.0)) * 100
        usdt = float(t.get('profit_abs', 0.0))
        open_rate = t['open_rate']
        min_rate = t.get('min_rate', open_rate)
        max_rate = t.get('max_rate', open_rate)
        lev = float(t.get('leverage') or 5.0)
        dur = f"{t.get('trade_duration', 0)}m"

        # For Short: MFE is how far rate fell below open_rate; MAE is how far rate rose above open_rate
        mfe_lev = (open_rate - min_rate) / open_rate * 100 * lev
        mae_lev = (max_rate - open_rate) / open_rate * 100 * lev

        total_roe += roe
        total_usdt += usdt
        exit_r = t.get('exit_reason', '').split('(')[0].strip()
        print(f"{i:<3} | {pair:<8} | {dur:<8} | {roe:>+6.2f}% | {mfe_lev:>+7.2f}% | -{mae_lev:>6.2f}% | {usdt:>+8.2f} USDT | {exit_r}")
    print("-" * 115)
    print(f"Average ROE (Profit %): {total_roe / len(t702):+.2f}%")
    print(f"Total Profit: {total_usdt:+.2f} USDT")

if __name__ == '__main__':
    main()
