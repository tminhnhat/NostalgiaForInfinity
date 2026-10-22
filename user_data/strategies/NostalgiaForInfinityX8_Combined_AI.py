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

from NostalgiaForInfinityX8 import NostalgiaForInfinityX8
from NostalgiaForInfinityX8_Combined import NostalgiaForInfinityX8_Combined
from freqtrade.persistence import Trade

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
    ai_model_path: str = "user_data/models/nfix8_short_ai_v3.pkl"
    ai_fallback_model_path: str = "user_data/models/nfix8_short_ai_v2.pkl"

    # Danh sách các tag custom Short bị loại bỏ.
    # Mặc định rỗng (Rollback - Không hardcode bất kỳ tag nào).
    # Có thể bật/tắt tự do qua file cấu hình (config.json) tương tự cách làm của Nostalgia gốc.
    disabled_custom_short_tags: set = set()

    # Toggles cho từng điều kiện Short custom (tương tự short_entry_signal_params của Nostalgia gốc)
    custom_short_signal_params: dict = {
        "custom_short_701_enable": True,
        "custom_short_702_enable": True,
        "custom_short_703_enable": True,
        "custom_short_705_enable": False,
        "custom_short_706_enable": True,
        "custom_short_711_enable": True,
        "custom_short_712_enable": True,
        "custom_short_713_enable": True,
        "custom_short_714_enable": False,
        "custom_short_721_enable": True,
        "custom_short_722_enable": True,
        "custom_short_723_enable": True,
        "custom_short_724_enable": True,
        "custom_short_725_enable": False,
        "custom_short_731_enable": True,
    }

    def version(self) -> str:
        base_ver = super().version()
        return f"{base_ver} + AI_Gatekeeper_v3.9_AsymmetricAdaptiveTrailing"

    def __init__(self, config: dict) -> None:
        # Tạm thời ẩn các key custom khỏi nfi_parameters để Nostalgia gốc không log warning không cần thiết
        nfi_params = config.get("nfi_parameters", {}) if isinstance(config, dict) else {}
        custom_keys = ["disabled_custom_short_tags", "custom_short_tag_params", "custom_short_signal_params"]
        popped = {}
        if isinstance(nfi_params, dict):
            for k in custom_keys:
                if k in nfi_params:
                    popped[k] = nfi_params.pop(k)

        super().__init__(config)

        # Khôi phục lại nfi_parameters
        if isinstance(nfi_params, dict) and popped:
            nfi_params.update(popped)

        # Cập nhật cấu hình bật/tắt tag từ config file (tương tự Nostalgia gốc)
        self.update_custom_signals_from_config(self.config)

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

    def update_signals_from_config(self, config: dict) -> None:
        """
        Kế thừa và mở rộng cơ chế update_signals_from_config của Nostalgia gốc:
        Cập nhật tín hiệu Long & Short gốc (562,...), sau đó cập nhật Short Custom.
        """
        super().update_signals_from_config(config)
        self.update_custom_signals_from_config(self.config)

    def update_custom_signals_from_config(self, cfg: dict) -> None:
        """
        Cập nhật trạng thái bật/tắt của các tag Short Custom từ file config (JSON),
        hoàn toàn tương đồng với cơ chế update_signals_from_config của Nostalgia gốc.
        Hỗ trợ cấu hình ở cả 2 vị trí:
        1. Bên trong block 'nfi_parameters':
           {
               "custom_short_signal_params": { "custom_short_701_enable": false, ... },
               "disabled_custom_short_tags": ["701 703 731", "703 722 731", "724 731"],
               "custom_short_tag_params": { "701 703 731": false, ... }
           }
        2. Hoặc trực tiếp ở root của file config:
           {
               "disabled_custom_short_tags": ["701 703 731", ...],
               "custom_short_signal_params": { ... }
           }
        """
        if not isinstance(cfg, dict):
            return

        nfi_params = cfg.get("nfi_parameters", {})
        if not isinstance(nfi_params, dict):
            nfi_params = {}

        # 1. Cập nhật custom_short_signal_params (từng signal con 701, 702, ...)
        config_signals = {}
        if "custom_short_signal_params" in nfi_params and isinstance(nfi_params["custom_short_signal_params"], dict):
            config_signals.update(nfi_params["custom_short_signal_params"])
        if "custom_short_signal_params" in cfg and isinstance(cfg["custom_short_signal_params"], dict):
            config_signals.update(cfg["custom_short_signal_params"])

        for k, v in config_signals.items():
            if k in self.custom_short_signal_params:
                self.custom_short_signal_params[k] = bool(v)
                log.info("Custom short signal param '%s' updated from config to %s", k, v)

        # Đồng bộ sang short_strategy (NostalgiaForInfinityX8_ShortSignals)
        signal_map = {
            "custom_short_701_enable": "enable_short_support_breakdown",
            "custom_short_702_enable": "enable_short_macd_breakdown",
            "custom_short_703_enable": "enable_short_ema_ribbon",
            "custom_short_705_enable": "enable_short_bb_squeeze",
            "custom_short_711_enable": "enable_short_sfp",
            "custom_short_712_enable": "enable_short_exhaustion_top",
            "custom_short_713_enable": "enable_short_volume_climax",
            "custom_short_714_enable": "enable_short_bearish_divergence",
            "custom_short_721_enable": "enable_short_relief_rejection",
            "custom_short_722_enable": "enable_short_stochrsi_cross",
            "custom_short_723_enable": "enable_short_bb_scalp",
            "custom_short_731_enable": "enable_short_btc_spillover",
        }
        # Đồng bộ sang short_strategy (NostalgiaForInfinityX8_ShortSignals) nếu đã được khởi tạo
        if hasattr(self, "short_strategy") and self.short_strategy is not None:
            for param_key, attr_name in signal_map.items():
                if param_key in self.custom_short_signal_params and hasattr(self.short_strategy, attr_name):
                    setattr(self.short_strategy, attr_name, self.custom_short_signal_params[param_key])

        # 2. Cập nhật danh sách disabled_custom_short_tags (hoặc custom_short_tag_params)
        # Mặc định rỗng (Rollback - tất cả tag được bật nếu không có config chỉ định tắt)
        self.disabled_custom_short_tags = set()

        dis_list = []
        if "disabled_custom_short_tags" in nfi_params and isinstance(nfi_params["disabled_custom_short_tags"], (list, set)):
            dis_list.extend(nfi_params["disabled_custom_short_tags"])
        if "custom_short_tag_params" in nfi_params and isinstance(nfi_params["custom_short_tag_params"], dict):
            for tag, enabled in nfi_params["custom_short_tag_params"].items():
                if not enabled:
                    dis_list.append(tag)

        if "disabled_custom_short_tags" in cfg and isinstance(cfg["disabled_custom_short_tags"], (list, set)):
            dis_list.extend(cfg["disabled_custom_short_tags"])
        if "custom_short_tag_params" in cfg and isinstance(cfg["custom_short_tag_params"], dict):
            for tag, enabled in cfg["custom_short_tag_params"].items():
                if not enabled:
                    dis_list.append(tag)

        for tag in dis_list:
            norm_tag = " ".join(sorted(str(tag).strip().split()))
            self.disabled_custom_short_tags.add(norm_tag)

        if self.disabled_custom_short_tags:
            log.info(
                "Configured %d disabled custom short tags from config: %s",
                len(self.disabled_custom_short_tags),
                sorted(list(self.disabled_custom_short_tags)),
            )
        else:
            log.info("No custom short tags disabled via config. All custom short tags active (Rollback mode).")

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

    def _compute_market_regime_thresholds(self, df: DataFrame, indices: np.ndarray) -> np.ndarray:
        """
        ĐỀ XUẤT 4: Market Regime Conditioning (Phân loại 4 pha thị trường vĩ mô BTC)
        Tự động co giãn ngưỡng duyệt Short:
        - STRONG_BULL (BTC Uptrend mạnh): Ngưỡng 0.68 (Siêu phòng thủ, chặn short ngược sóng)
        - BEAR_PANIC (BTC Downtrend / xả mạnh): Ngưỡng 0.48 (Tấn công thuận xu hướng, bắt trọn đà rơi)
        - SIDEWAY_CHOP (BTC tích lũy / đi ngang): Ngưỡng 0.60 (Lọc nhiễu, chống bear trap)
        - CORRECTION_RECOVERY (Điều chỉnh bình thường): Ngưỡng 0.55 (Cân bằng)
        """
        n_cand = len(indices)
        thresholds = np.full(n_cand, self.ai_confidence_threshold, dtype=np.float32)

        btc_d4_col = "ai_feat_btc_dist_ema200_4h"
        btc_d1_col = "ai_feat_btc_dist_ema200_1h"
        if btc_d4_col not in df.columns or btc_d1_col not in df.columns:
            return thresholds

        btc_d4 = df.loc[indices, btc_d4_col].to_numpy()
        btc_d1 = df.loc[indices, btc_d1_col].to_numpy()
        btc_rsi = df.loc[indices, "ai_feat_btc_rsi_1h"].to_numpy() if "ai_feat_btc_rsi_1h" in df.columns else np.full(n_cand, 50.0)

        # 1. STRONG_BULL: BTC trên EMA 200 4h, trên EMA 200 1h > 1%, RSI >= 55.0
        is_strong_bull = (btc_d4 > 0.0) & (btc_d1 > 0.01) & (btc_rsi >= 55.0)

        # 2. BEAR_PANIC: BTC dưới EMA 200 4h, dưới EMA 200 1h < -1%, RSI <= 45.0
        is_bear_panic = (btc_d4 < 0.0) & (btc_d1 < -0.01) & (btc_rsi <= 45.0)

        # 3. SIDEWAY_CHOP: BTC dao động hẹp quanh EMA 200 1h (|dist| <= 1%) và RSI vùng 45-55
        is_chop = (np.abs(btc_d1) <= 0.01) & (btc_rsi >= 45.0) & (btc_rsi <= 55.0)

        thresholds = np.where(is_strong_bull, 0.68, thresholds)
        thresholds = np.where(is_bear_panic, 0.48, thresholds)
        thresholds = np.where(is_chop, 0.60, thresholds)

        return thresholds

    def populate_entry_trend(self, df: DataFrame, metadata: dict) -> DataFrame:
        """
        Quy trình tạo tín hiệu vào lệnh chuẩn hóa:
        1. Kế thừa 100% tín hiệu Long & Short gốc của NostalgiaForInfinityX8 (Tuyệt đối không can thiệp).
        2. Kích hoạt các tín hiệu Short custom mới từ short_strategy (Nhóm 701-731).
        3. AI Gatekeeper CHỈ kiểm soát các tín hiệu Short custom:
           - Áp dụng Đề Xuất 4: Phân loại Market Regime để co giãn ngưỡng động [0.48 - 0.68].
           - Nếu ai_short_prob >= dynamic_threshold: Phê duyệt và gắn nhãn _AI_PASS vào tag custom.
           - Nếu ai_short_prob < dynamic_threshold: VETO (hủy tín hiệu custom, enter_short_custom = 0).
        4. KHÔNG can thiệp, không lọc và không đổi tag của các tín hiệu thuộc Nostalgia gốc (như 562).
        5. Gộp các tín hiệu an toàn vào DataFrame theo chuẩn Combined.
        """
        # 1. Chạy tín hiệu Nostalgia gốc (Tất cả Long & Short gốc như 562)
        df = NostalgiaForInfinityX8.populate_entry_trend(self, df, metadata)

        # 2. Chạy tín hiệu Short custom của module Combined
        df = self.short_strategy.populate_entry_trend(df, metadata)

        # 3. AI Gatekeeper CHỈ thẩm định và kiểm soát tín hiệu Short Custom
        if self.ai_gatekeeper_enabled and "enter_short_custom" in df.columns:
            custom_mask = (df["enter_short_custom"] == 1).to_numpy()
            if np.any(custom_mask):
                # 3.0. Surgical Tag Pruning: Loại bỏ các tổ hợp tag custom có kỳ vọng âm
                if hasattr(self, "disabled_custom_short_tags") and self.disabled_custom_short_tags:
                    c_tags_raw = df["enter_tag_custom"].fillna("").astype(str).to_numpy()
                    cand_idxs = np.where(custom_mask)[0]
                    prune_mask = np.zeros(len(df), dtype=bool)
                    for idx in cand_idxs:
                        norm_tag = " ".join(sorted(c_tags_raw[idx].strip().split()))
                        if norm_tag in self.disabled_custom_short_tags:
                            prune_mask[idx] = True

                    if np.any(prune_mask):
                        df.loc[prune_mask, "enter_short_custom"] = 0
                        df.loc[prune_mask, "enter_tag_custom"] = ""
                        custom_mask = (df["enter_short_custom"] == 1).to_numpy()

                # 3.0.1. ĐỀ XUẤT 3: Thắt chặt xác nhận Đa Khung Thời Gian cho Tag 722 (StochRSI 5m Confirmation)
                # Tín hiệu StochRSI 5m cross-down rất dễ bị trôi dạt (drift 36h) nếu khung 1h của coin đang có lực hồi.
                # Chỉ cho phép Short 722 khi RSI 1h của cặp coin đồng thuận suy yếu (RSI 1h < 50.0).
                if np.any(custom_mask) and "ai_feat_pair_rsi_1h" in df.columns:
                    c_tags_series = df["enter_tag_custom"].fillna("").astype(str)
                    has_722 = custom_mask & c_tags_series.str.contains("722", regex=False).to_numpy()
                    rsi_1h_strong = (df["ai_feat_pair_rsi_1h"] >= 50.0).to_numpy()
                    invalid_722 = has_722 & rsi_1h_strong
                    if np.any(invalid_722):
                        df.loc[invalid_722, "enter_short_custom"] = 0
                        df.loc[invalid_722, "enter_tag_custom"] = ""
                        custom_mask = (df["enter_short_custom"] == 1).to_numpy()

                if np.any(custom_mask):
                    # Tính toán xác suất AI CHỈ trên các cây nến có tín hiệu custom còn lại
                    ai_probs = self._compute_ai_probability(df, custom_mask)
                    if "ai_short_prob" not in df.columns:
                        df["ai_short_prob"] = np.zeros(len(df), dtype=np.float32)
                    df.loc[custom_mask, "ai_short_prob"] = ai_probs[custom_mask]

                    # ĐỀ XUẤT 4: Co giãn ngưỡng động theo Chế độ Thị trường (Market Regime)
                    cand_idxs_valid = np.where(custom_mask)[0]
                    regime_th = self._compute_market_regime_thresholds(df, cand_idxs_valid)
                    req_thresholds = np.full(len(df), self.ai_confidence_threshold, dtype=np.float32)
                    req_thresholds[cand_idxs_valid] = regime_th

                    approved_custom = custom_mask & (ai_probs >= req_thresholds)
                    vetoed_custom = custom_mask & (ai_probs < req_thresholds)

                    # VETO tín hiệu custom không đạt chuẩn
                    if np.any(vetoed_custom):
                        df.loc[vetoed_custom, "enter_short_custom"] = 0
                        # Ghi nhận audit log cho tín hiệu custom bị chặn
                        pair = metadata.get("pair", "UNKNOWN")
                        dates = df.loc[vetoed_custom, "date"].to_numpy()
                        v_probs = ai_probs[vetoed_custom]
                        v_req = req_thresholds[vetoed_custom]
                        v_tags = df.loc[vetoed_custom, "enter_tag_custom"].fillna("").astype(str).to_numpy()
                        for d, p, rth, t in zip(dates, v_probs, v_req, v_tags):
                            self.veto_audit_records.append({
                                "date": str(d),
                                "pair": pair,
                                "tag": t,
                                "ai_prob": float(p),
                                "required_th": float(rth),
                                "status": "VETOED_CUSTOM"
                            })

                    # Gắn hậu tố _AI_PASS CHỈ cho các tag custom được duyệt
                    if np.any(approved_custom):
                        c_tags = df["enter_tag_custom"].fillna("").astype(str).to_numpy()
                        df.loc[:, "enter_tag_custom"] = np.where(
                            approved_custom,
                            c_tags + "_AI_PASS",
                            c_tags,
                        )

        # 4. Hợp nhất Short Entry signals theo chuẩn Combined:
        # - Lệnh Short gốc của Nostalgia (562) được giữ nguyên vẹn 100% không bị ô nhiễm tag
        # - Lệnh Short custom được AI phê duyệt được hợp nhất vào
        if "enter_short_custom" in df.columns:
            custom_short_trigger = df["enter_short_custom"] == 1
            has_long = (df["enter_long"] == 1) if "enter_long" in df.columns else False
            safe_short_trigger = custom_short_trigger & (~has_long)

            # Kích hoạt enter_short flag nếu có custom short an toàn
            df.loc[safe_short_trigger, "enter_short"] = 1

            # Hợp nhất enter_tag: tag gốc Nostalgia (như 562) giữ nguyên, nối thêm tag custom đã duyệt
            existing_tags = df["enter_tag"].fillna("").astype(str).to_numpy()
            custom_tags = df["enter_tag_custom"].fillna("").astype(str).to_numpy()

            merged_tags = np.where(
                safe_short_trigger,
                np.where(
                    existing_tags != "",
                    existing_tags + " " + custom_tags,
                    custom_tags,
                ),
                existing_tags,
            )
            df.loc[:, "enter_tag"] = merged_tags

        ohlcv_cols = {"date", "open", "high", "low", "close", "volume"}
        f_cols = [c for c in df.select_dtypes(include=["float64"]).columns if c not in ohlcv_cols]
        if f_cols:
            df[f_cols] = df[f_cols].astype(np.float32)

        for c in df.select_dtypes(include=["int64", "int32"]).columns:
            if c not in ohlcv_cols:
                c_min = df[c].min()
                c_max = df[c].max()
                if c_min >= -128 and c_max <= 127:
                    df[c] = df[c].astype(np.int8)
                elif c_min >= -32768 and c_max <= 32767:
                    df[c] = df[c].astype(np.int16)
                else:
                    df[c] = df[c].astype(np.int32)

        return df

    def custom_exit(
        self,
        pair: str,
        trade: "Trade",
        current_time: "datetime",
        current_rate: float,
        current_profit: float,
        **kwargs,
    ) -> Optional[str]:
        """
        ĐỀ XUẤT 5: AI Dynamic Exit & Profit Protection Engine
        1. AI Trailing Profit Lock: Chống cho lại thị trường khi đã từng lãi lớn (MFE >= +8% ROE)
        2. AI Dynamic Reversal Harvest: Chốt lời sớm khi nến 5m kiệt sức bán / rút chân pinbar
        3. AI Time-Decay & Drift Soft Exit: Thoát các lệnh short trôi dạt quá 36h không sinh lời
        4. Chuyển tiếp an toàn vào pipeline Combined & Nostalgia gốc
        """
        orig_tag = getattr(trade, "enter_tag", "") or ""
        leverage = trade.leverage or 5.0
        open_rate = trade.open_rate

        # =========================================================================
        # 1. ADAPTIVE TRAILING PROFIT ENGINE CHO VỊ THẾ SHORT
        # Áp dụng cho toàn bộ Short (gồm cả Tag 562 và Custom Short) vì Short là Single Order (không DCA).
        # Khóa lợi nhuận thích ứng theo biên độ MFE, tối ưu hóa các siêu lệnh như MVLL, CHIP, ICNT.
        # (ĐỐI VỚI LONG: Giữ nguyên 100% State Machine của Nostalgia gốc để không làm đứt gãy chu trình De-risk/Grinding).
        # =========================================================================
        if trade.is_short and current_profit >= 0.12:
            min_r = trade.min_rate if trade.min_rate is not None else open_rate
            mfe_roe = (open_rate - min_r) / open_rate * leverage

            # Tầng 1: Mega Short Trend (MFE >= +45% ROE = +9% spot 5x)
            # Khóa bảo vệ tại 65% của đỉnh MFE, bắt buộc current_profit >= +20% ROE (tối ưu MVLL từ +16% lên +31% ROE)
            if mfe_roe >= 0.45 and current_profit >= 0.20 and current_profit <= mfe_roe * 0.65:
                return f"exit_short_adaptive_trailing_mega ( {orig_tag})"

            # Tầng 2: Mid Short Trend (MFE >= +25% ROE = +5% spot 5x)
            # Khóa bảo vệ tối thiểu +15% ROE (chốt trong biên độ 12% - 15% ROE)
            if mfe_roe >= 0.25 and current_profit >= 0.12 and current_profit <= 0.15:
                return f"exit_short_adaptive_trailing_mid ( {orig_tag})"

        # =========================================================================
        # 2. AI SHORT PROTECTION ENGINE
        # =========================================================================
        is_ai_short = trade.is_short and ("_AI_PASS" in orig_tag or any(t in orig_tag for t in self.short_strategy.custom_short_tags))

        if is_ai_short:
            min_r = trade.min_rate if trade.min_rate is not None else open_rate
            mfe_lev = (open_rate - min_r) / open_rate * leverage
            trade_duration_hours = (current_time - trade.open_date_utc).total_seconds() / 3600.0

            # 0. AI STRUCTURAL EARLY INVALIDATION CUT (ĐỀ XUẤT 2):
            # Nếu vị thế Short Custom đang âm (current_profit <= -0.20, tức -20% ROE = -4% spot)
            # VÀ giá coin đã bứt phá đóng nến vượt lên trên đường thể chế 1H EMA 200:
            # Cấu trúc Downtrend đã bị gãy hoàn toàn.
            # Lập tức thoát hiểm khẩn cấp tại -20% ROE, ngăn chặn việc gồng lệnh chịu lỗ đến -50% hay -95%!
            if current_profit <= -0.20 and hasattr(self, "dp") and self.dp is not None:
                df_pair, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
                if len(df_pair) > 0:
                    current_rows = df_pair.loc[df_pair["date"] <= current_time]
                    if len(current_rows) > 0:
                        last_c = current_rows.iloc[-1]
                        e200_1h = last_c.get("EMA_200_1h", None) or last_c.get("ema_200_1h", None)
                        if e200_1h is not None and not np.isnan(e200_1h) and e200_1h > 0:
                            if current_rate > e200_1h:
                                return f"exit_ai_early_macro_cut ( {orig_tag})"

            # 1. AI Trailing Profit Lock:
            # Nếu vị thế đã từng đạt MFE >= +8.0% đòn bẩy (+1.6% spot) nhưng hiện tại tụt về <= +1.0% đòn bẩy:
            # Khóa lợi nhuận an toàn, không để lệnh từ lãi chuyển thành lỗ!
            if mfe_lev >= 0.080 and current_profit <= 0.010:
                return f"exit_ai_profit_lock ( {orig_tag})"

            # 2. AI Dynamic Reversal Harvest:
            # Nếu lệnh đang lãi tốt (current_profit >= +6.0% đòn bẩy, tức +1.2% spot)
            # VÀ nến 5m xuất hiện lực đỡ rút chân pinbar mạnh (râu dưới >= 35%) hoặc RSI quá bán đảo chiều:
            # Chốt lời chủ động ngay vùng đáy nến để tối ưu hóa lợi nhuận thực tế!
            if current_profit >= 0.060 and hasattr(self, "dp") and self.dp is not None:
                df_pair, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
                if len(df_pair) > 0:
                    current_rows = df_pair.loc[df_pair["date"] <= current_time]
                    if len(current_rows) > 0:
                        last_c = current_rows.iloc[-1]
                        l_wick = last_c.get("ai_feat_lower_wick", 0.0)
                        rsi = last_c.get("rsi_14", 50.0)
                        if l_wick >= 0.35 and rsi > 30.0:
                            return f"exit_ai_reversal_harvest ( {orig_tag})"

            # 3. AI TIME-DECAY & DRIFT SOFT EXIT:
            # Lệnh short giữ quá 36h mà không thể bứt phá (lợi nhuận <= +0.4% đòn bẩy):
            # Thoát vị thế trôi dạt để giải phóng margin và bảo vệ tài khoản:
            if trade_duration_hours >= 36.0 and current_profit <= 0.004:
                return f"exit_ai_drift_decay ( {orig_tag})"

        # Chuyển tiếp vào pipeline custom_exit của Combined & Nostalgia gốc
        if orig_tag and "_AI_PASS" in orig_tag:
            trade.enter_tag = orig_tag.replace("_AI_PASS", "").strip()

        res = super().custom_exit(
            pair=pair,
            trade=trade,
            current_time=current_time,
            current_rate=current_rate,
            current_profit=current_profit,
            **kwargs,
        )
        trade.enter_tag = orig_tag
        return res

    def adjust_trade_position(
        self,
        trade: Trade,
        current_time: datetime,
        current_rate: float,
        current_profit: float,
        min_stake: Optional[float],
        max_stake: float,
        current_entry_rate: float,
        current_exit_rate: float,
        current_entry_profit: float,
        current_exit_profit: float,
        **kwargs,
    ) -> Optional[float]:
        """
        Asymmetric Smart AI DCA Gatekeeper:
        1. SHORT PROTECTION (100% VETO REBUY):
           - Dữ liệu thực nghiệm 187 ngày chứng minh 100% lệnh Short Rebuy tag 'r' đều thua lỗ
             do short-squeeze (PUMP, JTO, ZEC).
           - CẤM TUYỆT ĐỐI nhồi Short khi giá đang tăng ngược. Giữ nguyên Single Order.
           -> Tăng PnL Short từ +58.4$ lên +92.2$ (+58%), biến tag 562 từ âm thành dương (+21.3$).
        2. LONG PROTECTION (100% PRESERVE NOSTALGIA GRINDING):
           - Giữ nguyên 100% cơ chế Grinding/Rebuy/De-risk đa tầng của Nostalgia cho Long.
           - Không can thiệp thô bạo vào Long để tránh làm đứt gãy State Machine của SOXL (+32$), SNXX (+11$), WLD (+31$).
        """
        adj = super().adjust_trade_position(
            trade=trade,
            current_time=current_time,
            current_rate=current_rate,
            current_profit=current_profit,
            min_stake=min_stake,
            max_stake=max_stake,
            current_entry_rate=current_entry_rate,
            current_exit_rate=current_exit_rate,
            current_entry_profit=current_entry_profit,
            current_exit_profit=current_exit_profit,
            **kwargs,
        )

        # Unpack stake/amount nếu Nostalgia trả về dạng tuple (amount, tag)
        adj_amount = adj[0] if isinstance(adj, (tuple, list)) else adj
        if adj_amount is None:
            return adj

        # Nếu là lệnh DE-RISK (bán bớt vị thế để hạ rủi ro, adj_amount <= 0): Giữ nguyên 100%
        if adj_amount <= 0:
            return adj

        # ĐỐI VỚI SHORT: Cấm tuyệt đối nhồi lệnh (Veto Short Rebuy - Shorting an appreciating asset is extreme negative EV)
        if trade.is_short:
            return None

        # ĐỐI VỚI LONG: Giữ nguyên 100% chu trình Grinding của Nostalgia gốc
        return adj

    def confirm_trade_entry(
        self,
        pair: str,
        order_type: str,
        amount: float,
        rate: float,
        time_in_force: str,
        current_time: datetime,
        entry_tag: Optional[str],
        side: str,
        **kwargs,
    ) -> bool:
        """
        Circuit Breaker & Safety Entry Confirmation:
        - Kế thừa toàn bộ Portfolio Exposure Guard (tối đa 4 lệnh Short) và Weekend/Monday Guards của Combined.
        - Extreme Volatility & Panic Dump Circuit Breaker cho Long:
          Chặn các lệnh Long bắt dao rơi khi Volume 1h nổ bất thường (> 8.0x SMA 24h) VÀ giá đang sập dốc đứng (> 8% trong 4h).
          Triệt tiêu các thảm họa flash dump không có thanh khoản hồi phục (như ca KORU -76.69$).
        """
        base_confirm = super().confirm_trade_entry(
            pair=pair,
            order_type=order_type,
            amount=amount,
            rate=rate,
            time_in_force=time_in_force,
            current_time=current_time,
            entry_tag=entry_tag,
            side=side,
            **kwargs,
        )
        if not base_confirm:
            return False

        # Extreme Volatility & Panic Dump Circuit Breaker cho vị thế Long
        if side in ("long", "buy") and hasattr(self, "dp") and self.dp is not None:
            try:
                df_pair, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
                if len(df_pair) >= 50:
                    current_rows = df_pair.loc[df_pair["date"] <= current_time]
                    if len(current_rows) >= 50:
                        last_close = float(current_rows["close"].iloc[-1])
                        vol_1h = float(current_rows["volume"].tail(12).sum())
                        vol_sma = float(current_rows["volume"].tail(288).mean() * 12)
                        vol_ratio = vol_1h / max(vol_sma, 1e-5)

                        idx_4h = -49 if len(current_rows) >= 49 else 0
                        p_4h_ago = float(current_rows["close"].iloc[idx_4h])
                        drop_4h = (last_close - p_4h_ago) / max(p_4h_ago, 1e-5)

                        if vol_ratio > 8.0 and drop_4h < -0.08:
                            log.warning(
                                "Circuit Breaker Triggered: Blocked %s Long entry at %s (Vol 1h ratio: %.1fx, 4h drop: %.1f%%)",
                                pair, current_time, vol_ratio, drop_4h * 100.0,
                            )
                            return False
            except Exception as e:
                log.warning("Circuit Breaker evaluation error for %s: %s", pair, e)

        return True

    def custom_stake_amount(
        self,
        pair: str,
        current_time: datetime,
        current_rate: float,
        proposed_stake: float,
        min_stake: Optional[float],
        max_stake: float,
        leverage: float,
        entry_tag: Optional[str],
        side: str,
        **kwargs,
    ) -> float:
        """
        Dynamic Position Sizing: Kết hợp Chiều 1 (Dollar Volatility Equalization) & Chiều 2 (AI Confidence Sizing)
        - Chiều 1: Nghịch đảo biến động (Inverse ATR%). Cố định Dollar Risk Budget.
                   Coin biến động thấp -> Tăng stake lên 120-130$.
                   Coin biến động cực đoan -> Tự động ép stake về 25-35$ để triệt tiêu drawdown.
        - Chiều 2: Trọng số tin cậy AI (AI Confidence Sizing).
                   ai_prob >= 0.75 -> Tăng stake 1.20x.
                   ai_prob < 0.60 -> Giảm stake 0.80x.
        - Dynamic Margin Buffer:
                   Chỉ cho phép nâng stake lên 130$ nếu số slot đang mở <= 6 (còn dôi dư margin trong ví).
                   Nếu số slot đang mở > 6: Khóa trần stake <= 100$ để giữ an toàn margin cho DCA/Maintenance.
        - Asymmetric Sizing Belts:
                   Khóa trần Short <= 100$ (tránh phóng đại lỗ các lệnh Short bão).
                   Khóa sàn Long >= 25$ (đảm bảo các lệnh DCA con 10-20% luôn >= 5 USDT, không vi phạm Min Notional Binance).
        """
        base_stake = proposed_stake if proposed_stake and proposed_stake > 0 else 100.0
        vol_mult = 1.0
        ai_mult = 1.0

        if hasattr(self, "dp") and self.dp is not None:
            df_pair, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
            if len(df_pair) > 0:
                current_rows = df_pair.loc[df_pair["date"] <= current_time]
                if len(current_rows) > 0:
                    last_c = current_rows.iloc[-1]

                    # 1. Chiều 1: Inverse ATR Sizing (Benchmark ATR% = 1.2% / nến 5m)
                    val_atr = last_c.get("ai_feat_atr_norm", None)
                    if val_atr is not None and not np.isnan(val_atr) and val_atr > 0:
                        atr_norm = float(val_atr)
                        vol_mult = 0.012 / atr_norm
                        vol_mult = float(np.clip(vol_mult, 0.25, 1.30))

                    # 2. Chiều 2: AI Confidence Sizing (áp dụng khi có ai_short_prob)
                    val_prob = last_c.get("ai_short_prob", None)
                    if val_prob is not None and not np.isnan(val_prob) and val_prob > 0:
                        p = float(val_prob)
                        if p >= 0.75:
                            ai_mult = 1.20
                        elif p < 0.60:
                            ai_mult = 0.80

        target_stake = base_stake * vol_mult * ai_mult

        # 3. Dynamic Margin Buffer & Tiered Sizing Belts:
        open_trades_count = len(Trade.get_open_trades()) if Trade else 0

        # Mặc định cho Long: Nâng stake lên 130$ nếu slot <= 6, ngược lại giữ <= 100$
        max_allowed_stake = 130.0 if open_trades_count <= 6 else 100.0

        # Phân tầng trần cho vị thế Short (Tiered Short Sizing):
        if side in ("short", "sell"):
            etag = str(entry_tag or "")

            # Tầng 1: Elite High-WR Short Tags (100% Win Rate thực chứng: 706, 724, 721)
            # Dữ liệu thực chứng 187 ngày: 8 lệnh Thắng / 0 lệnh Thua
            # -> Cho phép nâng stake lên đến 130$ khi slot <= 6 để tối đa hóa lợi nhuận mà không tăng rủi ro
            tier1_elite_tags = ("706", "724", "721")
            is_tier1 = any(t in etag for t in tier1_elite_tags) and ("_AI_PASS" in etag or "AI_PASS" in etag)

            # Tầng 2: Standard AI Short Tags (Win Rate thực chứng 75% - 89%: 702 703 731, 701 702 703 731)
            # Nới nhẹ trần lên 115$ khi slot <= 6 (vừa mở rộng biên lãi của 11 lệnh thắng, vừa khống chế mức tăng lỗ nếu có)
            tier2_ai_tags = ("702 703 731", "701 702 703 731")
            is_tier2 = any(t in etag for t in tier2_ai_tags) and ("_AI_PASS" in etag or "AI_PASS" in etag)

            if is_tier1 and open_trades_count <= 6:
                max_allowed_stake = 130.0
            elif is_tier2 and open_trades_count <= 6:
                max_allowed_stake = 115.0
            else:
                # Tầng 3: Tag 562 gốc (nguồn gốc các ca bão JTO, PUMP, ZEC, RENDER) và các tag chưa xác thực -> Khóa chặt trần <= 100$
                max_allowed_stake = 100.0

        # Khóa sàn Long >= 25$ (đảm bảo các lệnh nhồi con 10-20% luôn >= 5 USDT)
        min_allowed_stake = 25.0 if side in ("long", "buy") else 20.0

        if min_stake is not None:
            min_allowed_stake = max(min_allowed_stake, min_stake)
        if max_stake is not None and max_stake > 0:
            max_allowed_stake = min(max_allowed_stake, max_stake)

        target_stake = float(np.clip(target_stake, min_allowed_stake, max_allowed_stake))
        return target_stake




