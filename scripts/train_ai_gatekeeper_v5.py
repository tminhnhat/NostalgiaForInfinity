import os, sys, time, gc, json

# Force UTF-8 stdout
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
import numpy as np
import pandas as pd
import talib.abstract as ta
import lightgbm as lgb
from pathlib import Path
from sklearn.metrics import roc_auc_score, average_precision_score, precision_score, classification_report
import joblib

def main():
    print("=" * 65)
    print("🚀 TRAINING AI GATEKEEPER v5.0 (LARGE PARAMETER MULTI-INDICATOR)")
    print("=" * 65)
    t_start = time.time()
    
    data_dir = Path("user_data/data/binance/futures")
    
    # 1. Load Whitelist Pairs
    with open("configs/backtest_config.json") as f:
        cfg = json.load(f)
    pairlist = cfg["exchange"]["pair_whitelist"]
    print(f"📋 Target Whitelist: {len(pairlist)} pairs")

    # 2. Load BTC HTF Data
    print("⏳ Loading & Processing BTC Macro Informative Data...")
    df_btc_1h = pd.read_feather(data_dir / "BTC_USDT_USDT-1h-futures.feather")
    df_btc_4h = pd.read_feather(data_dir / "BTC_USDT_USDT-4h-futures.feather")
    df_btc_1h['date'] = pd.to_datetime(df_btc_1h['date'])
    df_btc_4h['date'] = pd.to_datetime(df_btc_4h['date'])

    btc_c_1h = df_btc_1h['close'].to_numpy(dtype=float)
    e200_1h = ta.EMA(btc_c_1h, timeperiod=200)
    df_btc_1h['btc_rsi_1h'] = ta.RSI(btc_c_1h, timeperiod=14)
    df_btc_1h['btc_dist_ema200_1h'] = (btc_c_1h - e200_1h) / np.maximum(e200_1h, 1e-8)

    btc_c_4h = df_btc_4h['close'].to_numpy(dtype=float)
    e200_4h = ta.EMA(btc_c_4h, timeperiod=200)
    df_btc_4h['btc_rsi_4h'] = ta.RSI(btc_c_4h, timeperiod=14)
    df_btc_4h['btc_dist_ema200_4h'] = (btc_c_4h - e200_4h) / np.maximum(e200_4h, 1e-8)
    df_btc_4h['btc_roc_9_4h'] = ta.ROC(btc_c_4h, timeperiod=9)

    df_btc_1h_clean = df_btc_1h[['date', 'btc_rsi_1h', 'btc_dist_ema200_1h']].sort_values('date')
    df_btc_4h_clean = df_btc_4h[['date', 'btc_rsi_4h', 'btc_dist_ema200_4h', 'btc_roc_9_4h']].sort_values('date')

    # 3. Process Each Pair & Build Dataset
    all_dfs = []
    total_raw_candles = 0

    feature_cols = [
        'upper_wick', 'lower_wick', 'body_ratio', 'candle_range_norm',
        'dist_ema9', 'dist_ema21', 'dist_ema50', 'dist_ema200', 'ribbon_spread_9_21', 'ribbon_spread_50_200',
        'rsi_14', 'rsi_7', 'stochrsi_k', 'stochrsi_d',
        'bb_bandwidth', 'bb_percent', 'atr_norm',
        'vol_spike', 'sell_vol_ratio_3', 'sell_vol_ratio_6',
        'pair_dist_ema50_1h', 'pair_dist_ema200_1h', 'pair_rsi_1h', 'pair_dist_ema200_4h', 'pair_rsi_4h',
        'btc_rsi_1h', 'btc_rsi_4h', 'btc_dist_ema200_1h', 'btc_dist_ema200_4h', 'btc_roc_9_4h'
    ]

    print(f"📊 Feature Universe: {len(feature_cols)} Technical & Macro Indicators")
    print("⏳ Extracting indicators & labels across all pairs...")

    processed_count = 0
    for pair in pairlist:
        clean_symbol = pair.replace("/", "_").replace(":", "_")
        p5m = data_dir / f"{clean_symbol}-5m-futures.feather"
        p1h = data_dir / f"{clean_symbol}-1h-futures.feather"
        p4h = data_dir / f"{clean_symbol}-4h-futures.feather"

        if not (p5m.exists() and p1h.exists() and p4h.exists()):
            continue

        try:
            df_5m = pd.read_feather(p5m)
            df_1h = pd.read_feather(p1h)
            df_4h = pd.read_feather(p4h)

            df_5m['date'] = pd.to_datetime(df_5m['date'])
            df_1h['date'] = pd.to_datetime(df_1h['date'])
            df_4h['date'] = pd.to_datetime(df_4h['date'])

            total_raw_candles += len(df_5m)

            # Pair 1h
            c_1h = df_1h['close'].to_numpy(dtype=float)
            e50_1h = ta.EMA(c_1h, timeperiod=50)
            e200_1h = ta.EMA(c_1h, timeperiod=200)
            df_1h['pair_dist_ema50_1h'] = (c_1h - e50_1h) / np.maximum(e50_1h, 1e-8)
            df_1h['pair_dist_ema200_1h'] = (c_1h - e200_1h) / np.maximum(e200_1h, 1e-8)
            df_1h['pair_rsi_1h'] = ta.RSI(c_1h, timeperiod=14)

            # Pair 4h
            c_4h = df_4h['close'].to_numpy(dtype=float)
            e200_4h = ta.EMA(c_4h, timeperiod=200)
            df_4h['pair_dist_ema200_4h'] = (c_4h - e200_4h) / np.maximum(e200_4h, 1e-8)
            df_4h['pair_rsi_4h'] = ta.RSI(c_4h, timeperiod=14)

            # 5m
            c = df_5m['close'].to_numpy(dtype=float)
            o = df_5m['open'].to_numpy(dtype=float)
            h = df_5m['high'].to_numpy(dtype=float)
            l = df_5m['low'].to_numpy(dtype=float)
            v = df_5m['volume'].to_numpy(dtype=float)

            c_range = np.maximum(h - l, 1e-8)
            df_5m['upper_wick'] = (h - np.maximum(o, c)) / c_range
            df_5m['lower_wick'] = (np.minimum(o, c) - l) / c_range
            df_5m['body_ratio'] = np.abs(c - o) / c_range
            df_5m['candle_range_norm'] = c_range / np.maximum(c, 1e-8)

            ema9 = ta.EMA(c, timeperiod=9)
            ema21 = ta.EMA(c, timeperiod=21)
            ema50 = ta.EMA(c, timeperiod=50)
            ema200 = ta.EMA(c, timeperiod=200)

            df_5m['dist_ema9'] = (c - ema9) / np.maximum(ema9, 1e-8)
            df_5m['dist_ema21'] = (c - ema21) / np.maximum(ema21, 1e-8)
            df_5m['dist_ema50'] = (c - ema50) / np.maximum(ema50, 1e-8)
            df_5m['dist_ema200'] = (c - ema200) / np.maximum(ema200, 1e-8)
            df_5m['ribbon_spread_9_21'] = (ema21 - ema9) / np.maximum(c, 1e-8)
            df_5m['ribbon_spread_50_200'] = (ema200 - ema50) / np.maximum(c, 1e-8)

            df_5m['rsi_14'] = ta.RSI(c, timeperiod=14)
            df_5m['rsi_7'] = ta.RSI(c, timeperiod=7)

            fastk, fastd = ta.STOCHRSI(c, timeperiod=14, fastk_period=5, fastd_period=3)
            df_5m['stochrsi_k'] = fastk
            df_5m['stochrsi_d'] = fastd

            bb_u, bb_m, bb_l = ta.BBANDS(c, timeperiod=20, nbdevup=2.0, nbdevdn=2.0)
            df_5m['bb_bandwidth'] = (bb_u - bb_l) / np.maximum(bb_m, 1e-8)
            df_5m['bb_percent'] = (c - bb_l) / np.maximum(bb_u - bb_l, 1e-8)

            atr = ta.ATR(h, l, c, timeperiod=14)
            df_5m['atr_norm'] = atr / np.maximum(c, 1e-8)

            vol_sma24 = ta.SMA(v, timeperiod=24)
            df_5m['vol_spike'] = v / np.maximum(vol_sma24, 1e-8)

            is_red = (c < o).astype(float)
            red_vol = v * is_red
            sum_red_3 = ta.SUM(red_vol, timeperiod=3)
            sum_vol_3 = ta.SUM(v, timeperiod=3)
            df_5m['sell_vol_ratio_3'] = sum_red_3 / np.maximum(sum_vol_3, 1e-8)

            sum_red_6 = ta.SUM(red_vol, timeperiod=6)
            sum_vol_6 = ta.SUM(v, timeperiod=6)
            df_5m['sell_vol_ratio_6'] = sum_red_6 / np.maximum(sum_vol_6, 1e-8)

            # Merge HTF Pair & BTC
            df_5m = pd.merge_asof(df_5m.sort_values('date'), df_1h[['date', 'pair_dist_ema50_1h', 'pair_dist_ema200_1h', 'pair_rsi_1h']].sort_values('date'), on='date')
            df_5m = pd.merge_asof(df_5m, df_4h[['date', 'pair_dist_ema200_4h', 'pair_rsi_4h']].sort_values('date'), on='date')
            df_5m = pd.merge_asof(df_5m, df_btc_1h_clean, on='date')
            df_5m = pd.merge_asof(df_5m, df_btc_4h_clean, on='date')

            # Dynamic Triple Barrier Labeling (Short Direction)
            # Horizon: 24 bars (2 hours).
            horizon = 24
            k_tp = 2.5
            k_sl = 2.5
            min_tp = 0.010
            min_sl = 0.012

            atr_norm_arr = df_5m['atr_norm'].to_numpy(dtype=float)
            tp_pct = np.maximum(k_tp * atr_norm_arr, min_tp)
            sl_pct = np.maximum(k_sl * atr_norm_arr, min_sl)
            tp_targets = c * (1.0 - tp_pct)
            sl_targets = c * (1.0 + sl_pct)

            n = len(c)
            labels = np.zeros(n, dtype=np.int32)
            valid_mask = np.zeros(n, dtype=bool)

            # Pre-filter candidate setups to train the gatekeeper
            # We want all candles where downward movement or bearish setup occurs
            is_candidate = (
                (c < ema50) | (c < o) | (df_5m['rsi_14'] < 55) | (df_5m['vol_spike'] > 1.2)
            ).to_numpy()

            for i in range(200, n - horizon):
                if not is_candidate[i]:
                    continue
                
                tp_val = tp_targets[i]
                sl_val = sl_targets[i]
                
                win = False
                loss = False
                for step in range(1, horizon + 1):
                    bar_h = h[i + step]
                    bar_l = l[i + step]
                    hit_tp = bar_l <= tp_val
                    hit_sl = bar_h >= sl_val
                    if hit_tp and not hit_sl:
                        win = True
                        break
                    elif hit_sl and not hit_tp:
                        loss = True
                        break
                    elif hit_tp and hit_sl:
                        loss = True
                        break
                
                if win:
                    labels[i] = 1
                    valid_mask[i] = True
                elif loss:
                    labels[i] = 0
                    valid_mask[i] = True

            df_sub = df_5m.loc[valid_mask, ['date'] + feature_cols].copy()
            df_sub['target_win'] = labels[valid_mask]
            
            all_dfs.append(df_sub)
            processed_count += 1
            if processed_count % 20 == 0:
                print(f"  ... processed {processed_count}/{len(pairlist)} pairs ({round(time.time() - t_start, 1)}s)")

        except Exception as e:
            continue

    print(f"✅ Processed {processed_count} pairs from {total_raw_candles:,} raw 5m candles!")
    df_all = pd.concat(all_dfs, ignore_index=True)
    df_all = df_all.dropna().sort_values('date').reset_index(drop=True)
    
    total_samples = len(df_all)
    pos_samples = int(df_all['target_win'].sum())
    print(f"📊 Total Labeled Samples: {total_samples:,} | Wins: {pos_samples:,} ({pos_samples/total_samples:.1%}) | Noise/Loss: {total_samples - pos_samples:,}")

    # 4. Purged Time-Series Split (80% Train, 20% Test)
    split_idx = int(total_samples * 0.80)
    train_df = df_all.iloc[:split_idx]
    test_df = df_all.iloc[split_idx:]

    X_train = train_df[feature_cols].to_numpy(dtype=np.float32)
    y_train = train_df['target_win'].to_numpy(dtype=np.int32)
    X_test = test_df[feature_cols].to_numpy(dtype=np.float32)
    y_test = test_df['target_win'].to_numpy(dtype=np.int32)

    print(f"📦 Train Set: {len(X_train):,} samples ({train_df['date'].min()} -> {train_df['date'].max()})")
    print(f"📦 Test Set:  {len(X_test):,} samples ({test_df['date'].min()} -> {test_df['date'].max()})")

    # 5. Train LightGBM with Large Hyperparameters
    print("\n🧠 Training LightGBM Model with Large Hyperparameters...")
    params = {
        'objective': 'binary',
        'metric': 'binary_logloss',
        'boosting_type': 'gbdt',
        'n_estimators': 1000,
        'learning_rate': 0.02,
        'num_leaves': 127,
        'max_depth': 10,
        'min_child_samples': 50,
        'subsample': 0.85,
        'colsample_bytree': 0.80,
        'reg_alpha': 0.1,
        'reg_lambda': 1.5,
        'scale_pos_weight': 1.5,
        'n_jobs': -1,
        'random_state': 42,
        'verbose': -1
    }

    model = lgb.LGBMClassifier(**params)
    t_train = time.time()
    model.fit(X_train, y_train)
    print(f"⚡ Model Training Completed in {round(time.time() - t_train, 2)} s!")

    # 6. Out-of-Time Test Evaluation
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    roc_auc = roc_auc_score(y_test, y_pred_proba)
    pr_auc = average_precision_score(y_test, y_pred_proba)

    print("\n" + "=" * 50)
    print("📈 OUT-OF-TIME EVALUATION METRICS:")
    print("=" * 50)
    print(f"⭐ ROC-AUC Score: {roc_auc:.4f}")
    print(f"⭐ PR-AUC Score:  {pr_auc:.4f}")

    # Percentiles for Gatekeeper Calibration
    train_probs = model.predict_proba(X_train)[:, 1]
    p25 = float(np.percentile(train_probs, 25))
    p50 = float(np.percentile(train_probs, 50))
    p75 = float(np.percentile(train_probs, 75))
    p90 = float(np.percentile(train_probs, 90))
    print(f"🎯 Probability Calibration Percentiles:")
    print(f"   P25={p25:.4f} | P50={p50:.4f} | P75={p75:.4f} | P90={p90:.4f}")

    # Feature Importance Top 15
    importances = model.feature_importances_
    feat_imp = sorted(zip(feature_cols, importances), key=lambda x: x[1], reverse=True)
    print("\n🏆 Top 15 Most Important Indicators:")
    for f_name, f_imp in feat_imp[:15]:
        print(f"   - {f_name:24}: {f_imp:5d}")

    # 7. Save Model Bundle
    save_path = Path("user_data/models/nfix8_short_ai_v5.pkl")
    save_path.parent.mkdir(parents=True, exist_ok=True)

    # Set model to CPU device for universal portability
    model.set_params(device_type='cpu')

    model_bundle = {
        'model': model,
        'p25': p25,
        'p50': p50,
        'p75': p75,
        'p90': p90,
        'feature_cols': feature_cols,
        'version': 'v5.0_FullUniverse_LargeParam_Gatekeeper',
        'trained_at': time.strftime('%Y-%m-%d %H:%M:%S'),
        'metrics': {
            'roc_auc': roc_auc,
            'pr_auc': pr_auc,
            'train_samples': len(X_train),
            'test_samples': len(X_test),
            'total_features': len(feature_cols)
        },
        'dynamic_barrier_params': {
            'k_tp': k_tp, 'k_sl': k_sl, 'min_tp': min_tp, 'min_sl': min_sl, 'horizon': horizon
        }
    }

    joblib.dump(model_bundle, save_path, compress=3)
    print(f"\n💾 Saved AI Model Bundle v5.0 to: {save_path} ({round(os.path.getsize(save_path)/1024/1024, 2)} MB)")
    print(f"🎉 Total Pipeline Time: {round(time.time() - t_start, 2)} seconds!")

if __name__ == "__main__":
    main()
