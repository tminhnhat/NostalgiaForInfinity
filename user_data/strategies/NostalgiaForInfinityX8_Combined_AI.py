# -*- coding: utf-8 -*-
"""
NostalgiaForInfinityX8_Combined_AI
Version: v3.6.3 + AI_Gatekeeper_v1.0_DualTag
Hướng 3: AI Meta-Labeling Gatekeeper kết hợp Dual-Tagging (_AI_PASS) & Kiểm toán Veto
Độc lập hoàn toàn với bản chuẩn NostalgiaForInfinityX8_Combined.py để dễ dàng chạy A/B Testing.
"""
import logging
import os
import pickle
from datetime import datetime
from typing import Optional, List, Dict, Any

import numpy as np
import pandas as pd
from pandas import DataFrame
import talib.abstract as ta

from NostalgiaForInfinityX8_Combined import NostalgiaForInfinityX8_Combined

log = logging.getLogger(__name__)


class NostalgiaForInfinityX8_Combined_AI(NostalgiaForInfinityX8_Combined):
    """
    Chiến lược nâng cấp tích hợp AI Gatekeeper theo Hướng 3:
    1. Kế thừa 100% logic Long và Layer 1 (Macro EMA 200) + Layer 2 (Emergency Inversion Cut).
    2. AI Gatekeeper (Meta-Labeling) đứng gác tại cửa ngõ vào lệnh Short:
       - Phân tích 15 đặc trưng vĩ mô, cấu trúc nến, áp lực râu và động lượng.
       - Chỉ phê duyệt mở lệnh khi độ tin cậy AI >= ai_confidence_threshold (mặc định 0.65).
    3. Dual-Tagging: Tự động gắn hậu tố '_AI_PASS' vào enter_tag của các lệnh được AI phê duyệt
       để bảng báo cáo Freqtrade hiển thị riêng biệt và đo lường ROI minh bạch.
    4. Audited Veto: Ghi nhận nhật ký các lệnh bị Veto để tính toán chỉ số Alpha của AI.
    5. Graceful Fallback: Nếu chưa có file model ML, tự động dùng Heuristic Scoring để chạy ngay.
    """

    INTERFACE_VERSION = 3

    # Cấu hình AI Gatekeeper
    ai_gatekeeper_enabled: bool = True
    ai_confidence_threshold: float = 0.55
    ai_model_path: str = "user_data/models/nfix8_short_ai_v2.pkl"
    ai_fallback_model_path: str = "user_data/models/nfix8_short_ai_v1.pkl"

    def version(self) -> str:
        base_ver = super().version()
        return f"{base_ver} + AI_Gatekeeper_v2.0_MTF_DualTag"

    def __init__(self, config: dict) -> None:
        super().__init__(config)

        # Danh sách tag phê duyệt AI cần đăng ký vào NFIX8 subsystems
        # để order tracking, position sizing và exit engines nhận diện trơn tru
        ai_tags_to_register = []
        for tag in list(self.short_strategy.custom_short_tags):
            ai_tag = f"{tag}_AI_PASS"
            ai_tags_to_register.append(ai_tag)
            # Thêm biến thể tổ hợp phổ biến
            ai_tags_to_register.append(f"{tag} 731_AI_PASS")
            ai_tags_to_register.append(f"702 703 731_AI_PASS")
            ai_tags_to_register.append(f"701 703 731_AI_PASS")
            ai_tags_to_register.append(f"703 722 731_AI_PASS")

        for atag in set(ai_tags_to_register):
            if atag not in self.short_normal_mode_tags:
                self.short_normal_mode_tags.append(atag)
            if atag not in self.short_known_mode_tags:
                self.short_known_mode_tags.append(atag)
            if atag not in self.short_exit_known_mode_tags:
                self.short_exit_known_mode_tags.append(atag)

        # Nạp mô hình AI (ưu tiên v2, fallback v1)
        self.ai_model = None
        self._load_ai_model()

        # Bộ nhớ đệm kiểm toán Veto (dành cho script đo lường Alpha)
        self.veto_audit_records: List[Dict[str, Any]] = []

        log.info(
            "NostalgiaForInfinityX8_Combined_AI initialized successfully! AI Gatekeeper: %s (Threshold: %.2f)",
            "ENABLED" if self.ai_gatekeeper_enabled else "DISABLED",
            self.ai_confidence_threshold,
        )

    def _load_ai_model(self) -> None:
        """Nạp model học máy từ đĩa (Pickle / Joblib / ONNX)."""
        self.ai_model = None
        self.ai_p25 = 0.1935
        self.ai_p50 = 0.3692
        self.ai_p75 = 0.5527
        self.ai_feature_cols = [
            'upper_wick', 'lower_wick', 'body_ratio',
            'dist_ema21', 'dist_ema50', 'dist_ema200',
            'rsi_14', 'bb_bandwidth', 'atr_norm', 'vol_spike',
            'sell_vol_ratio_3', 'sell_vol_ratio_6',
            'pair_dist_ema50_1h', 'pair_dist_ema200_1h', 'pair_rsi_1h',
            'btc_rsi_1h', 'btc_dist_ema200_1h', 'btc_dist_ema200_4h'
        ]
        
        target_path = self.ai_model_path if os.path.exists(self.ai_model_path) else self.ai_fallback_model_path
        if os.path.exists(target_path):
            try:
                import joblib
                bundle = joblib.load(target_path)
                if isinstance(bundle, dict) and "model" in bundle:
                    self.ai_model = bundle["model"]
                    self.ai_p25 = float(bundle.get("p25", 0.1935))
                    self.ai_p50 = float(bundle.get("p50", 0.3692))
                    self.ai_p75 = float(bundle.get("p75", 0.5527))
                    self.ai_feature_cols = bundle.get("feature_cols", self.ai_feature_cols)
                    ver = bundle.get("version", "v1.0")
                else:
                    self.ai_model = bundle
                    ver = "legacy"
                log.info(
                    "Loaded trained AI Gatekeeper model (%s) from %s (Features: %d, P50: %.4f)",
                    ver, target_path, len(self.ai_feature_cols), self.ai_p50
                )
            except Exception as e:
                log.warning("Failed to load AI model from %s: %s. Using heuristic gatekeeper fallback.", target_path, e)
                self.ai_model = None
        else:
            log.info(
                "Model files not found. Using Intelligent Rule-Engine Gatekeeper until trained model is uploaded."
            )
            self.ai_model = None

    def populate_indicators(self, df: DataFrame, metadata: dict) -> DataFrame:
        """
        1. Gọi populate_indicators của bản chuẩn (đầy đủ chỉ báo NFI + ShortSignals + Memory downcasting).
        2. Tính toán bổ sung 18 đặc trưng sạch Đa Khung Thời Gian (MTF) phục vụ AI Gatekeeper.
        """
        df = super().populate_indicators(df, metadata)

        # Đảm bảo không tính toán lặp lại nếu đã có
        if "ai_feat_upper_wick" in df.columns:
            return df

        # --- TÍNH TOÁN 18 ĐẶC TRƯNG ĐA KHUNG THỜI GIAN CHO AI GATEKEEPER ---
        open_p = df["open"].to_numpy(copy=False)
        high_p = df["high"].to_numpy(copy=False)
        low_p = df["low"].to_numpy(copy=False)
        close_p = df["close"].to_numpy(copy=False)
        vol = df["volume"].to_numpy(copy=False)

        candle_range = np.maximum(high_p - low_p, 1e-8)
        body = np.abs(close_p - open_p)

        # 1. Tỷ lệ râu nến trên (áp lực bán từ chối giá tăng)
        upper_wick = high_p - np.maximum(open_p, close_p)
        df["ai_feat_upper_wick"] = (upper_wick / candle_range).astype(np.float32)

        # 2. Tỷ lệ râu nến dưới (lực đỡ mua rút chân - rủi ro bẫy nảy)
        lower_wick = np.minimum(open_p, close_p) - low_p
        df["ai_feat_lower_wick"] = (lower_wick / candle_range).astype(np.float32)

        # 3. Tỷ lệ thân nến
        df["ai_feat_body_ratio"] = (body / candle_range).astype(np.float32)

        # 4. Khoảng cách giá đến các đường EMA
        for p, col in [(21, "ema_21"), (50, "ema_50"), (200, "ema_200")]:
            if col in df.columns:
                df[f"ai_feat_dist_ema{p}"] = ((close_p - df[col].to_numpy(copy=False)) / df[col].to_numpy(copy=False)).astype(np.float32)
            else:
                df[f"ai_feat_dist_ema{p}"] = 0.0

        # 5. Khoảng cách đến 1H EMA 200 (nếu có)
        e200_1h_col = "EMA_200_1h" if "EMA_200_1h" in df.columns else ("ema_200_1h" if "ema_200_1h" in df.columns else None)
        if e200_1h_col is not None:
            df["ai_feat_dist_ema200_1h"] = ((close_p - df[e200_1h_col].to_numpy(copy=False)) / np.maximum(df[e200_1h_col].to_numpy(copy=False), 1e-8)).astype(np.float32)
        else:
            df["ai_feat_dist_ema200_1h"] = 0.0

        # 6. Động lượng RSI và Volatility
        if "rsi_14" in df.columns:
            df["ai_feat_rsi_14"] = df["rsi_14"].to_numpy(copy=False).astype(np.float32)
        else:
            df["ai_feat_rsi_14"] = np.full(len(df), 50.0, dtype=np.float32)
        
        # 7. Bollinger Bandwidth (Độ co nén dải BB)
        if "bb_upperband2" in df.columns and "bb_lowerband2" in df.columns and "bb_middleband2" in df.columns:
            bb_w = (df["bb_upperband2"] - df["bb_lowerband2"]) / np.maximum(df["bb_middleband2"], 1e-8)
            df["ai_feat_bb_bandwidth"] = bb_w.astype(np.float32)
        else:
            df["ai_feat_bb_bandwidth"] = 0.05

        # 8. ATR Normalized (Biên độ dao động thực tế chuẩn hóa)
        atr = ta.ATR(high_p, low_p, close_p, timeperiod=14)
        df["ai_feat_atr_norm"] = (atr / np.maximum(close_p, 1e-8)).astype(np.float32)

        # 9. Tỷ lệ Volume đột biến so với SMA Volume 20
        vol_sma20 = ta.SMA(vol, timeperiod=20)
        df["ai_feat_vol_spike"] = (vol / np.maximum(vol_sma20, 1e-8)).astype(np.float32)

        # 10. Tỷ lệ Volume xả bán trong 3 và 6 nến gần nhất
        is_red = (close_p < open_p).astype(np.float32)
        red_vol = vol * is_red
        sum_red_3 = ta.SUM(red_vol, timeperiod=3)
        sum_vol_3 = ta.SUM(vol, timeperiod=3)
        df["ai_feat_sell_vol_ratio_3"] = (sum_red_3 / np.maximum(sum_vol_3, 1e-8)).astype(np.float32)
        df["ai_feat_sell_vol_ratio"] = df["ai_feat_sell_vol_ratio_3"] # Tương thích v1

        sum_red_6 = ta.SUM(red_vol, timeperiod=6)
        sum_vol_6 = ta.SUM(vol, timeperiod=6)
        df["ai_feat_sell_vol_ratio_6"] = (sum_red_6 / np.maximum(sum_vol_6, 1e-8)).astype(np.float32)

        # 11. Đặc trưng Đa Khung Thời Gian 1h của Coin (Pair HTF 1h)
        e50_1h = df["EMA_50_1h"] if "EMA_50_1h" in df.columns else (df["ema_50_1h"] if "ema_50_1h" in df.columns else None)
        df["ai_feat_pair_dist_ema50_1h"] = (((close_p - e50_1h.to_numpy(copy=False)) / np.maximum(e50_1h.to_numpy(copy=False), 1e-8)).astype(np.float32)) if e50_1h is not None else 0.0

        e200_1h = df["EMA_200_1h"] if "EMA_200_1h" in df.columns else (df["ema_200_1h"] if "ema_200_1h" in df.columns else None)
        df["ai_feat_pair_dist_ema200_1h"] = (((close_p - e200_1h.to_numpy(copy=False)) / np.maximum(e200_1h.to_numpy(copy=False), 1e-8)).astype(np.float32)) if e200_1h is not None else 0.0

        rsi_1h = df["rsi_14_1h"] if "rsi_14_1h" in df.columns else (df["rsi_1h"] if "rsi_1h" in df.columns else None)
        df["ai_feat_pair_rsi_1h"] = rsi_1h.to_numpy(copy=False).astype(np.float32) if rsi_1h is not None else np.full(len(df), 50.0, dtype=np.float32)

        # 12. Đặc trưng Vĩ mô BTC Đa Khung Thời Gian (1h & 4h)
        btc_rsi_1h = df["btc_rsi_14_1h"] if "btc_rsi_14_1h" in df.columns else (df["btc_rsi_1h"] if "btc_rsi_1h" in df.columns else None)
        df["ai_feat_btc_rsi_1h"] = btc_rsi_1h.to_numpy(copy=False).astype(np.float32) if btc_rsi_1h is not None else np.full(len(df), 50.0, dtype=np.float32)
        df["ai_feat_btc_rsi"] = df["ai_feat_btc_rsi_1h"] # Tương thích v1

        btc_c_1h = df["btc_close_1h"] if "btc_close_1h" in df.columns else None
        btc_e200_1h = df["btc_EMA_200_1h"] if "btc_EMA_200_1h" in df.columns else (df["btc_ema_200_1h"] if "btc_ema_200_1h" in df.columns else None)
        if btc_c_1h is not None and btc_e200_1h is not None:
            btc_d_1h = ((btc_c_1h - btc_e200_1h) / np.maximum(btc_e200_1h, 1e-8)).astype(np.float32)
            df["ai_feat_btc_dist_ema200_1h"] = btc_d_1h
            df["ai_feat_btc_dist_ema200"] = btc_d_1h # Tương thích v1
        else:
            df["ai_feat_btc_dist_ema200_1h"] = 0.0
            df["ai_feat_btc_dist_ema200"] = 0.0

        btc_c_4h = df["btc_close_4h"] if "btc_close_4h" in df.columns else btc_c_1h
        btc_e200_4h = df["btc_EMA_200_4h"] if "btc_EMA_200_4h" in df.columns else (df["btc_ema_200_4h"] if "btc_ema_200_4h" in df.columns else btc_e200_1h)
        if btc_c_4h is not None and btc_e200_4h is not None:
            df["ai_feat_btc_dist_ema200_4h"] = ((btc_c_4h - btc_e200_4h) / np.maximum(btc_e200_4h, 1e-8)).astype(np.float32)
        else:
            df["ai_feat_btc_dist_ema200_4h"] = 0.0

        return df

    def _compute_ai_probability(self, df: DataFrame, candidate_mask: np.ndarray) -> np.ndarray:
        """
        Tính toán xác suất thắng P(Win) của AI Gatekeeper cho các cây nến có tín hiệu Short.
        - Nếu có model ML: Dùng model.predict_proba() kèm hiệu chuẩn Percentile
        - Nếu chưa có model: Dùng Heuristic Scoring dựa trên 15 đặc trưng kỹ thuật
        """
        n_rows = len(df)
        probs = np.zeros(n_rows, dtype=np.float32)

        cand_indices = np.where(candidate_mask)[0]
        if len(cand_indices) == 0:
            return probs

        feat_map = {
            'upper_wick': 'ai_feat_upper_wick',
            'lower_wick': 'ai_feat_lower_wick',
            'body_ratio': 'ai_feat_body_ratio',
            'dist_ema21': 'ai_feat_dist_ema21',
            'dist_ema50': 'ai_feat_dist_ema50',
            'dist_ema200': 'ai_feat_dist_ema200',
            'rsi_14': 'ai_feat_rsi_14',
            'bb_bandwidth': 'ai_feat_bb_bandwidth',
            'atr_norm': 'ai_feat_atr_norm',
            'vol_spike': 'ai_feat_vol_spike',
            'sell_vol_ratio': 'ai_feat_sell_vol_ratio',
            'sell_vol_ratio_3': 'ai_feat_sell_vol_ratio_3',
            'sell_vol_ratio_6': 'ai_feat_sell_vol_ratio_6',
            'pair_dist_ema50_1h': 'ai_feat_pair_dist_ema50_1h',
            'pair_dist_ema200_1h': 'ai_feat_pair_dist_ema200_1h',
            'pair_rsi_1h': 'ai_feat_pair_rsi_1h',
            'btc_rsi': 'ai_feat_btc_rsi',
            'btc_rsi_1h': 'ai_feat_btc_rsi_1h',
            'btc_dist_ema200': 'ai_feat_btc_dist_ema200',
            'btc_dist_ema200_1h': 'ai_feat_btc_dist_ema200_1h',
            'btc_dist_ema200_4h': 'ai_feat_btc_dist_ema200_4h',
        }
        df_cols = [feat_map.get(col, f"ai_feat_{col}") for col in self.ai_feature_cols]
        all_cols_exist = all(c in df.columns for c in df_cols)

        if self.ai_model is not None and all_cols_exist:
            try:
                X_cand = df.loc[cand_indices, df_cols].to_numpy()
                if hasattr(self.ai_model, "predict_proba"):
                    raw_p = self.ai_model.predict_proba(X_cand)[:, 1]
                else:
                    raw_p = self.ai_model.predict(X_cand)
                
                # Hiệu chuẩn Percentile sang thang điểm tin cậy [0.10, 0.95]
                scores = np.interp(
                    raw_p,
                    [0.05, self.ai_p25, self.ai_p50, self.ai_p75, 0.75],
                    [0.10, 0.40, 0.60, 0.75, 0.95]
                )
                scores = np.clip(scores, 0.05, 0.98)
                probs[cand_indices] = scores
                return probs
            except Exception as e:
                log.warning("AI model prediction failed: %s. Falling back to heuristic scoring.", e)

        # HEURISTIC SCORING ENGINE (Đóng vai trò AI Baseline khi chưa nạp model ML)
        # Chấm điểm xác suất dựa trên logic bất đối xứng của Short:
        # + Điểm cộng: Nến từ chối tăng (râu trên cao), nến xả dứt khoát (râu dưới thấp),
        #              Volume bán áp đảo, BTC nằm dưới EMA 200 1h, giá nằm dưới EMA 200 1h
        # - Điểm trừ: Rút chân pinbar (râu dưới > 35%), BTC đang quá mua, volume cạn kiệt
        base_score = 0.50

        u_wick = df.loc[cand_indices, "ai_feat_upper_wick"].to_numpy()
        l_wick = df.loc[cand_indices, "ai_feat_lower_wick"].to_numpy()
        sell_vol = df.loc[cand_indices, "ai_feat_sell_vol_ratio"].to_numpy()
        dist_200_1h = df.loc[cand_indices, "ai_feat_dist_ema200_1h"].to_numpy()
        btc_dist_200 = df.loc[cand_indices, "ai_feat_btc_dist_ema200"].to_numpy()
        rsi = df.loc[cand_indices, "ai_feat_rsi_14"].to_numpy()

        score = np.full(len(cand_indices), base_score, dtype=np.float32)
        score += np.where(u_wick >= 0.25, 0.12, 0.0)
        score += np.where(sell_vol >= 0.60, 0.10, 0.0)
        score += np.where(dist_200_1h <= 0.0, 0.12, -0.20)  # Thưởng lớn khi dưới EMA 200 1h
        score += np.where(btc_dist_200 <= 0.0, 0.08, -0.10) # Thưởng khi BTC đang Downtrend
        score += np.where((rsi >= 30.0) & (rsi <= 48.0), 0.08, -0.05)

        # Phạt nặng các cây nến rút chân pinbar hoặc quá bán sâu
        score -= np.where(l_wick >= 0.35, 0.25, 0.0)
        score -= np.where(rsi < 25.0, 0.20, 0.0)

        # Kẹp xác suất trong khoảng [0.05, 0.98]
        score = np.clip(score, 0.05, 0.98)
        probs[cand_indices] = score
        return probs

    def populate_entry_trend(self, df: DataFrame, metadata: dict) -> DataFrame:
        """
        1. Gọi populate_entry_trend của bản chuẩn (đầy đủ Long/Short NFI và Custom Shorts).
        2. Nếu ai_gatekeeper_enabled:
           - Duyệt qua tất cả các cây nến có tín hiệu enter_short == 1.
           - Tính toán AI Confidence Score.
           - Nếu Score >= ai_confidence_threshold:
               * GIỮ LỆNH enter_short = 1
               * ĐỔI TAG: enter_tag = enter_tag + "_AI_PASS" (Dual-Tagging)
           - Nếu Score < ai_confidence_threshold:
               * VETO (HỦY LỆNH): enter_short = 0
               * Ghi nhận audit log lệnh bị chặn.
        """
        df = super().populate_entry_trend(df, metadata)

        if not self.ai_gatekeeper_enabled:
            return df

        if "ai_short_prob" not in df.columns:
            df["ai_short_prob"] = np.zeros(len(df), dtype=np.float32)

        short_cand_mask = (df["enter_short"] == 1).to_numpy()
        if not np.any(short_cand_mask):
            return df

        # Tính toán xác suất AI
        ai_probs = self._compute_ai_probability(df, short_cand_mask)
        df["ai_short_prob"] = ai_probs

        approved_mask = short_cand_mask & (ai_probs >= self.ai_confidence_threshold)
        vetoed_mask = short_cand_mask & (ai_probs < self.ai_confidence_threshold)

        # 1. HỦY LỆNH BỊ VETO (Bảo vệ 10 slot danh mục)
        if np.any(vetoed_mask):
            df.loc[vetoed_mask, "enter_short"] = 0
            # Ghi nhận các lệnh bị Veto để kiểm toán Alpha
            pair = metadata.get("pair", "UNKNOWN")
            dates = df.loc[vetoed_mask, "date"].to_numpy()
            v_probs = ai_probs[vetoed_mask]
            v_tags = df.loc[vetoed_mask, "enter_tag"].fillna("").astype(str).to_numpy()
            for d, p, t in zip(dates, v_probs, v_tags):
                self.veto_audit_records.append({
                    "date": str(d),
                    "pair": pair,
                    "tag": t,
                    "ai_prob": float(p),
                    "status": "VETOED"
                })

        # 2. DUAL-TAGGING: Gắn hậu tố '_AI_PASS' cho các lệnh được duyệt
        if np.any(approved_mask):
            tags = df["enter_tag"].fillna("").astype(str).to_numpy()
            new_tags = np.where(
                approved_mask,
                np.where(tags != "", tags + "_AI_PASS", "AI_PASS"),
                tags,
            )
            df.loc[:, "enter_tag"] = new_tags

        return df
