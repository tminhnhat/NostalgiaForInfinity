# -*- coding: utf-8 -*-
"""
NostalgiaForInfinityX8_ShortSignals
Modular Advanced Short Entry & Exit Strategy for Crypto Futures.

THIS MODULE ADDS BRAND NEW, QUANTITATIVE SHORT STRATEGIES INDEPENDENT OF NOSTALGIA:
  - Nhóm 1: Short Exhaustion / Market Tops (Bắt đỉnh, bẫy thanh khoản SFP, Blow-off Top)
    * Tag 711: Swing Failure Pattern (SFP) / Liquidity Sweep Fakeout
    * Tag 712: Multi-Timeframe Overbought Climax (RSI + BB Rejection)
    * Tag 713: Volume Climax Buying Exhaustion (Phe mua kiệt sức)
    * Tag 714: Multi-Timeframe Bearish Divergence (Phân kỳ giảm giá)
  
  - Nhóm 2: Short Trend Breakdown (Gãy cấu trúc hỗ trợ và MA)
    * Tag 701: Support / Donchian Channel Breakdown với Volume lớn
    * Tag 702: Death Cross Momentum & MACD Zero-Line Rejection
    * Tag 703: Bearish Moving Average Ribbon Expansion (EMA 21 < 50 < 200)

  - Nhóm 3: Short Scalp (Bắt nhịp điều chỉnh nhanh trong downtrend)
    * Tag 721: Relief Bounce Rejection (Hồi kỹ thuật chạm EMA bị từ chối)
    * Tag 722: StochRSI Overbought Cross-down trong Downtrend
    * Tag 723: Upper Bollinger Band Rejection Scalp

  - Nhóm 4: Short Market Alignment (Đồng pha theo đà sập của BTC)
    * Tag 731: BTC Momentum Breakdown Spillover (Altcoin xả theo BTC)
"""

import logging
from datetime import datetime
from typing import Optional, Tuple
import numpy as np
import pandas as pd
from pandas import DataFrame, Series
import talib.abstract as ta

log = logging.getLogger(__name__)


class NostalgiaForInfinityX8_ShortSignals:
    """
    Dedicated Quantitative Short Signals Engine.
    Provides completely new Short Entry and Exit algorithms for Freqtrade.
    """

    def __init__(self, config: dict = None) -> None:
        self.config = config or {}

        # =========================================================================
        # Toggles cho từng nhóm tín hiệu mới
        # =========================================================================
        self.enable_custom_short = True

        # Nhóm 1: Exhaustion & Liquidity Sweeps
        self.enable_short_sfp = True                   # Tag 711 (SFP Sweep - rất tốt)
        self.enable_short_exhaustion_top = True        # Tag 712 (BBU Rejection - top performer)
        self.enable_short_volume_climax = True         # Tag 713 (Volume Climax - tốt khi kết hợp)
        self.enable_short_bearish_divergence = False   # Tag 714 (Tắt vì 5m divergence bị nhiễu cao)

        # Nhóm 2: Trend Breakdown
        self.enable_short_support_breakdown = True     # Tag 701 (Donchian breakdown - rất mạnh)
        self.enable_short_macd_breakdown = True        # Tag 702 (Siết chặt volume + trend + confluence)
        self.enable_short_ema_ribbon = True            # Tag 703 (EMA Ribbon expansion - tốt)
        self.enable_short_bb_squeeze = False           # Tag 705 (Tắt vì 5m squeeze có kỳ vọng âm -69.51$)

        # Nhóm 3: Scalp Signals
        self.enable_short_relief_rejection = True      # Tag 721 (EMA21 relief rejection - rất tốt)
        self.enable_short_stochrsi_cross = True        # Tag 722 (Siết chặt xác nhận xu hướng)
        self.enable_short_bb_scalp = True              # Tag 723 (Siết chặt dốc Bollinger & volume)

        # Nhóm 4: BTC Spillover
        self.enable_short_btc_spillover = True         # Tag 731 (BTC dump spillover - 83.9% winrate)

        # =========================================================================
        # Exit Thresholds chuyên biệt cho Short
        # =========================================================================
        self.tp_target_swing = 0.035                   # +3.5% chốt lời swing
        self.tp_target_scalp = 0.020                   # +2.0% chốt lời scalp
        self.tp_target_oversold = 0.012                # +1.2% chốt lời khi RSI quá bán sâu
        
        self.invalidation_sl_tight = -0.025            # -2.5% cắt lỗ scalp (cho phép thở qua nhiễu 5m)
        self.invalidation_sl_wide = -0.035             # -3.5% cắt lỗ swing tối đa (bảo vệ tài khoản)

        # Danh sách toàn bộ các tags mới
        self.custom_short_tags = [
            "701", "702", "703", "705", "706",
            "711", "712", "713", "714",
            "721", "722", "723", "724", "725",
            "731",
            "short_custom_breakdown",
            "short_custom_sfp",
            "short_custom_exhaustion",
            "short_custom_scalp",
            "short_custom_btc_dump"
        ]

        log.info(
            "NostalgiaForInfinityX8_ShortSignals initialized with %d new short entry tags.",
            len(self.custom_short_tags),
        )

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Tính toán các chỉ báo kỹ thuật định lượng chuyên biệt cho chiến lược Short.
        """
        close = dataframe["close"].to_numpy(copy=False)
        high = dataframe["high"].to_numpy(copy=False)
        low = dataframe["low"].to_numpy(copy=False)
        open_px = dataframe["open"].to_numpy(copy=False)
        volume = dataframe["volume"].to_numpy(copy=False)

        # 1. Hình thái nến (Candlestick Anatomy: Upper Wick, Body, Lower Wick)
        hl_range = high - low
        hl_safe = np.where(hl_range == 0, 1e-9, hl_range)
        upper_wick = high - np.maximum(close, open_px)
        lower_wick = np.minimum(close, open_px) - low
        body = np.abs(close - open_px)

        dataframe["upper_wick_ratio"] = upper_wick / hl_safe
        dataframe["lower_wick_ratio"] = lower_wick / hl_safe
        dataframe["body_ratio"] = body / hl_safe

        # 2. Moving Averages nếu chưa có
        if "EMA_9" not in dataframe.columns:
            dataframe["EMA_9"] = ta.EMA(close, timeperiod=9)
        if "EMA_21" not in dataframe.columns:
            dataframe["EMA_21"] = ta.EMA(close, timeperiod=21)
        if "EMA_50" not in dataframe.columns:
            dataframe["EMA_50"] = ta.EMA(close, timeperiod=50)
        if "EMA_200" not in dataframe.columns:
            dataframe["EMA_200"] = ta.EMA(close, timeperiod=200)

        # 3. Bollinger Bands (20, 2.0) & Band Width Squeeze
        bbu, bbm, bbl = ta.BBANDS(close, timeperiod=20, nbdevup=2.0, nbdevdn=2.0, matype=0)
        dataframe["BBU_20_2.0"] = bbu
        dataframe["BBL_20_2.0"] = bbl
        dataframe["BBM_20_2.0"] = bbm
        bb_range = bbu - bbl
        bbm_safe = np.where(bbm == 0, 1e-9, bbm)
        bb_width = bb_range / bbm_safe
        dataframe["bb_width"] = bb_width
        dataframe["bb_width_sma_20"] = ta.SMA(bb_width, timeperiod=20)

        # 4. Volatility & ATR
        dataframe["ATR_14"] = ta.ATR(high, low, close, timeperiod=14)

        # 5. Volume Climax Analysis
        vol_sma_20 = ta.SMA(volume, timeperiod=20)
        vol_sma_safe = np.where(vol_sma_20 == 0, 1e-9, vol_sma_20)
        dataframe["vol_spike_ratio"] = volume / vol_sma_safe

        # 6. Swing Extremes & Donchian Channels (Hỗ trợ / Kháng cự động)
        dataframe["rolling_high_12"] = ta.MAX(high, timeperiod=12)
        dataframe["rolling_high_24"] = ta.MAX(high, timeperiod=24)
        dataframe["rolling_high_48"] = ta.MAX(high, timeperiod=48)
        dataframe["rolling_low_12"] = ta.MIN(low, timeperiod=12)
        dataframe["rolling_low_24"] = ta.MIN(low, timeperiod=24)
        dataframe["rolling_low_48"] = ta.MIN(low, timeperiod=48)

        # 7. MACD (12, 26, 9)
        macd, macdsignal, macdhist = ta.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
        dataframe["macd_custom"] = macd
        dataframe["macdsignal_custom"] = macdsignal
        dataframe["macdhist_custom"] = macdhist

        # 8. StochRSI (14, 14, 3, 3)
        rsi_14 = dataframe["RSI_14"].to_numpy(copy=False) if "RSI_14" in dataframe.columns else ta.RSI(close, timeperiod=14)
        stoch_rsi_low = ta.MIN(rsi_14, timeperiod=14)
        stoch_rsi_high = ta.MAX(rsi_14, timeperiod=14)
        stoch_range = np.where(stoch_rsi_high - stoch_rsi_low == 0, 1e-9, stoch_rsi_high - stoch_rsi_low)
        raw_stoch_k = ((rsi_14 - stoch_rsi_low) / stoch_range) * 100.0
        dataframe["stochrsi_k_custom"] = ta.SMA(raw_stoch_k, timeperiod=3)
        dataframe["stochrsi_d_custom"] = ta.SMA(dataframe["stochrsi_k_custom"].to_numpy(copy=False), timeperiod=3)
        dataframe["rolling_rsi_max_24"] = ta.MAX(rsi_14, timeperiod=24)

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Đánh giá các điều kiện Short HOÀN TOÀN MỚI và xuất ra:
          - enter_short_custom: 1 nếu thỏa mãn ít nhất 1 điều kiện
          - enter_tag_custom: chuỗi chứa các tag tương ứng (701..731)
        """
        if not self.enable_custom_short:
            dataframe["enter_short_custom"] = 0
            dataframe["enter_tag_custom"] = ""
            return dataframe

        n_rows = len(dataframe)
        enter_short_custom = np.zeros(n_rows, dtype=int)
        enter_tag_custom = np.full(n_rows, "", dtype=object)

        # Views mảng NumPy tối ưu tốc độ
        close = dataframe["close"].to_numpy(copy=False)
        high = dataframe["high"].to_numpy(copy=False)
        low = dataframe["low"].to_numpy(copy=False)
        open_px = dataframe["open"].to_numpy(copy=False)
        volume = dataframe["volume"].to_numpy(copy=False)

        bbu = dataframe["BBU_20_2.0"].to_numpy(copy=False)
        bbl = dataframe["BBL_20_2.0"].to_numpy(copy=False)
        bbm = dataframe["BBM_20_2.0"].to_numpy(copy=False)

        ema_9 = dataframe["EMA_9"].to_numpy(copy=False)
        ema_21 = dataframe["EMA_21"].to_numpy(copy=False)
        ema_50 = dataframe["EMA_50"].to_numpy(copy=False)
        ema_200 = dataframe["EMA_200"].to_numpy(copy=False)

        upper_wick_ratio = dataframe["upper_wick_ratio"].to_numpy(copy=False)
        lower_wick_ratio = dataframe["lower_wick_ratio"].to_numpy(copy=False)
        body_ratio = dataframe["body_ratio"].to_numpy(copy=False)
        vol_spike_ratio = dataframe["vol_spike_ratio"].to_numpy(copy=False)

        rolling_high_24 = dataframe["rolling_high_24"].to_numpy(copy=False)
        rolling_low_12 = dataframe["rolling_low_12"].to_numpy(copy=False)
        rolling_low_24 = dataframe["rolling_low_24"].to_numpy(copy=False)
        rolling_low_48 = dataframe["rolling_low_48"].to_numpy(copy=False)
        bb_width = dataframe["bb_width"].to_numpy(copy=False)
        bb_width_sma_20 = dataframe["bb_width_sma_20"].to_numpy(copy=False)
        rolling_rsi_max_24 = dataframe["rolling_rsi_max_24"].to_numpy(copy=False)

        macd = dataframe["macd_custom"].to_numpy(copy=False)
        macdhist = dataframe["macdhist_custom"].to_numpy(copy=False)
        stochrsi_k = dataframe["stochrsi_k_custom"].to_numpy(copy=False)
        stochrsi_d = dataframe["stochrsi_d_custom"].to_numpy(copy=False)

        rsi_14 = dataframe["RSI_14"].to_numpy(copy=False) if "RSI_14" in dataframe.columns else ta.RSI(close, timeperiod=14)

        # Kiểm tra xung lượng xả mạnh thực sự trên khung 4h (loại bỏ hoàn toàn sideway chop)
        btc_dumping = np.zeros(n_rows, dtype=bool)
        if "ROC_9_4h" in dataframe.columns:
            btc_dumping = dataframe["ROC_9_4h"].to_numpy(copy=False) < -1.0
        elif "BTC_RSI_14_4h" in dataframe.columns:
            btc_dumping = dataframe["BTC_RSI_14_4h"].to_numpy(copy=False) < 45.0

        # Weekend Liquidity Guards: Chống bẫy thanh khoản mỏng cuối tuần (MM bẫy Stoploss / Short Squeeze)
        is_sunday = np.zeros(n_rows, dtype=bool)
        is_saturday = np.zeros(n_rows, dtype=bool)
        # Monday Trap Guards:
        # 1. Weekly Open Trap: Rạng sáng Thứ Hai (00:00 - 02:00 UTC) khi nến tuần mới mở (áp dụng toàn bộ tags)
        is_monday_morning = np.zeros(n_rows, dtype=bool)
        # 2. US Open Trap: Phiên Mỹ Thứ Hai mở cửa & quét thanh khoản sớm (12:00 - 15:00 UTC) khi cá mập quét thanh khoản phá đáy
        is_monday_us_open = np.zeros(n_rows, dtype=bool)
        if "date" in dataframe.columns:
            d_series = dataframe["date"].dt
            dow = d_series.dayofweek.to_numpy(copy=False)
            hr = d_series.hour.to_numpy(copy=False)
            is_sunday = (dow == 6)
            is_saturday = (dow == 5)
            is_monday_morning = (dow == 0) & (hr < 2)
            is_monday_us_open = (dow == 0) & (hr >= 12) & (hr < 15)

        # BTC Bullish Momentum Guard: Không Short khi BTC khung lớn đang có đà tăng dốc
        btc_bullish = np.zeros(n_rows, dtype=bool)
        if "BTC_RSI_14_4h" in dataframe.columns:
            btc_bullish = dataframe["BTC_RSI_14_4h"].to_numpy(copy=False) > 52.0
        elif "BTC_RSI_14_1h" in dataframe.columns:
            btc_bullish = dataframe["BTC_RSI_14_1h"].to_numpy(copy=False) > 52.0
        elif "RSI_14_4h" in dataframe.columns and metadata.get("pair", "").startswith("BTC"):
            btc_bullish = dataframe["RSI_14_4h"].to_numpy(copy=False) > 52.0

        # Bộ lọc siêu xu hướng tăng (Tránh Short chặn đầu xe lửa khi 1h đang uptrend parabolic)
        rsi_1h_overbought = np.zeros(n_rows, dtype=bool)
        rsi_1h_oversold = np.zeros(n_rows, dtype=bool)
        if "RSI_14_1h" in dataframe.columns:
            rsi_1h = dataframe["RSI_14_1h"].to_numpy(copy=False)
            rsi_1h_overbought = (rsi_1h > 62.0) & (close > ema_200)
            rsi_1h_oversold = rsi_1h < 30.0

        # NÂNG CẤP TẦNG 1: Macro 1H Trend Guards (Đường xu hướng thể chế 1H EMA 200)
        close_above_ema200_1h = np.zeros(n_rows, dtype=bool)
        if "EMA_200_1h" in dataframe.columns:
            ema_200_1h = dataframe["EMA_200_1h"].to_numpy(copy=False)
            close_above_ema200_1h = (close > ema_200_1h) & np.isfinite(ema_200_1h) & (ema_200_1h > 0)
        elif "ema_200_1h" in dataframe.columns:
            ema_200_1h = dataframe["ema_200_1h"].to_numpy(copy=False)
            close_above_ema200_1h = (close > ema_200_1h) & np.isfinite(ema_200_1h) & (ema_200_1h > 0)

        # Trạng thái siêu sóng tăng đa khung thời gian
        macro_bull_ribbon = (ema_9 > ema_21) & (ema_21 > ema_50) & (ema_50 > ema_200) & (close > ema_200)

        # =========================================================================
        # TÍNH TOÁN CÁC MASK ĐIỀU KIỆN ĐỘC LẬP (ĐÃ TỐI ƯU GIẢM NHIỄU)
        # =========================================================================

        # TAG 711: Swing Failure Pattern (SFP) - Top Performer 100% Winrate
        shift_high_24 = np.roll(rolling_high_24, 1)
        cond_711 = (
            (volume > 0)
            & (high > shift_high_24)                      # Quét qua đỉnh cũ 24 nến (2h)
            & (close < shift_high_24)                     # Đóng cửa thất bại dưới đỉnh cũ (Fakeout rõ ràng)
            & (upper_wick_ratio >= 0.40)                  # Râu trên dài từ chối giá
            & (vol_spike_ratio >= 1.25)                   # Volume quét thanh khoản cao
            & (close < open_px)                           # BẮT BUỘC NẾN ĐỎ
            & (rsi_14 >= 62.0)                            # Xung lượng đang ở vùng cao
            & (close < ema_9 * 1.008)                     # Không ở quá xa EMA 9
        )

        # TAG 712: Multi-Timeframe Overbought Rejection tại Dải Trên BB
        # Tối ưu: Bỏ hoàn toàn rsi_3, bắt buộc nến đỏ, đóng cửa lọt lại vào trong dải BB
        cond_712 = (
            (volume > 0)
            & (high >= bbu * 0.998)                       # Quét chạm hoặc đâm thủng dải trên BB
            & (close < bbu)                               # Bắt buộc đóng nến lọt lại vào bên trong BB
            & (close < open_px)                           # BẮT BUỘC NẾN ĐỎ (Tuyệt đối không short nến xanh)
            & (upper_wick_ratio >= 0.42)                  # Râu trên từ chối dài
            & (rsi_14 >= 68.0)                            # Chỉ dùng RSI 14 chuẩn (loại bỏ rsi_3 gây nhiễu)
            & (vol_spike_ratio >= 1.25)                   # Volume xác nhận phe bán ra hàng
            & (close < (high + low) * 0.50)               # Đóng cửa nằm ở nửa dưới cây nến
        )

        # TAG 713: Volume Climax Buying Exhaustion
        # Tối ưu: Bắt buộc nến đỏ, râu xả áp đảo, đóng cửa dưới BBU
        cond_713 = (
            (volume > 0)
            & (vol_spike_ratio >= 2.0)                    # Khối lượng nổ đột biến gấp đôi trung bình
            & (upper_wick_ratio >= 0.45)                  # Râu xả chiếm ưu thế áp đảo
            & (close < open_px)                           # BẮT BUỘC NẾN ĐỎ
            & (close < bbu)                               # Đóng dưới dải trên BB
            & (body_ratio <= 0.35)                        # Thân nến nhỏ (phe mua bất lực sau nổ volume)
            & (high >= bbu * 0.998)
            & (rsi_14 >= 65.0)
        )

        # TAG 701: Support Breakdown (Phá vỡ đáy Donchian 24 nến)
        # Tối ưu: Bắt buộc nến đỏ, râu dưới ngắn (loại bẫy rút chân), đóng dưới EMA 9 & EMA 21
        shift_low_24 = np.roll(rolling_low_24, 1)
        cond_701 = (
            (volume > 0)
            & (close < shift_low_24)                      # Đóng cửa phá vỡ hoàn toàn đáy 24 nến
            & (close < open_px)                           # BẮT BUỘC NẾN ĐỎ
            & (lower_wick_ratio <= 0.30)                  # Râu dưới ngắn (áp lực bán duy trì, không rút chân)
            & (close < ema_9) & (close < ema_21)          # Nằm dưới EMA 9 và EMA 21
            & (ema_50 < ema_200)                          # Downtrend tổng thể
            & (vol_spike_ratio >= 1.25)                   # Volume xả gia tăng
            & (vol_spike_ratio <= 5.0)                    # Loại bỏ volume dị biệt selling climax
            & (rsi_14 > 28.0) & (rsi_14 < 46.0)           # Đang có quán tính giảm, chưa quá bán
            & (stochrsi_k >= 20.0)                        # Chống bán tháo ở đáy 5m
            & (~rsi_1h_oversold)                          # Không short khi 1h đã quá bán sâu < 30
            & (~rsi_1h_overbought)                        # Không short nếu khung 1h đang siêu tăng
            & (~is_saturday)                              # Chống bẫy thanh khoản Thứ Bảy
            & (~is_sunday)                                # Chống bẫy thanh khoản Chủ Nhật
            & (~is_monday_morning)                        # Chống bẫy fakeout rạng sáng Thứ Hai
            & (~is_monday_us_open)                         # Chống bẫy quét thanh khoản phiên Mỹ Thứ Hai
            & (~btc_bullish)                              # Không short khi BTC đang tăng dốc
        )

        # TAG 703: Bearish Moving Average Ribbon Expansion (Tối ưu hóa: kiểm soát độ dốc & mở rộng dải)
        shift_ema_9 = np.roll(ema_9, 1)
        shift_ema_21 = np.roll(ema_21, 1)
        ribbon_spread = (ema_21 - ema_9) / np.where(ema_21 == 0, 1e-9, ema_21)
        cond_703 = (
            (volume > 0)
            & (ema_9 < ema_21)
            & (ema_21 < ema_50)
            & (ema_50 < ema_200)
            & (ema_9 < shift_ema_9)                       # EMA 9 dốc xuống xác nhận đà giảm
            & (ema_21 < shift_ema_21)                     # EMA 21 dốc xuống xác nhận đà giảm
            & (ribbon_spread >= 0.0006)                   # Dải Ribbon mở rộng thực sự (spread >= 0.06%, loại bỏ flat chop)
            & (close < ema_9)
            & (close < open_px)
            & (vol_spike_ratio >= 1.25)                   # Chuẩn volume bán xác nhận từ 1.25 trở lên
            & (vol_spike_ratio <= 5.0)                    # Loại bỏ volume dị biệt selling climax
            & (rsi_14 > 30.0) & (rsi_14 < 46.0)
            & (stochrsi_k >= 20.0)                        # Chống bán tháo ở đáy 5m
            & (~rsi_1h_overbought)                        # Không short nếu 1h đang siêu tăng
            & (~rsi_1h_oversold)                          # Không short nếu 1h đã quá bán sâu < 30 (chống bẫy đảo chiều)
            & (~is_saturday)                              # Chống bẫy thanh khoản Thứ Bảy
            & (~is_sunday)                                # Chống bẫy thanh khoản Chủ Nhật
            & (~is_monday_morning)                        # Chống bẫy fakeout rạng sáng Thứ Hai
            & (~is_monday_us_open)                         # Chống bẫy quét thanh khoản phiên Mỹ Thứ Hai
            & (~btc_bullish)                              # Không short khi BTC đang tăng dốc
        )

        # TAG 731: BTC Momentum Breakdown Spillover (Đồng pha theo BTC)
        ribbon_spread_731 = (ema_21 - ema_9) / np.where(ema_21 == 0, 1e-9, ema_21)
        cond_731 = (
            (volume > 0)
            & btc_dumping                                 # BTC sập
            & (ema_50 < ema_200)                          # Downtrend
            & (ema_9 < ema_21)                            # Phân kỳ giảm giữa 2 MA ngắn hạn
            & (ribbon_spread_731 >= 0.0006)               # Loại bỏ hoàn toàn flat MA chop (< 0.06% spread)
            & (close < ema_9) & (close < ema_21)          # Đóng nến dưới cả 2 đường EMA
            & (close < open_px)
            & (vol_spike_ratio >= 1.25)
            & (rsi_14 > 28.0) & (rsi_14 < 48.0)
            & (stochrsi_k >= 20.0)                        # Chống bán tháo ở đáy 5m
            & (~rsi_1h_oversold)                          # Không short khi 1h đã quá bán sâu < 30
            & (~rsi_1h_overbought)                        # Không short khi 1h đang uptrend mạnh
            & (~is_saturday)                              # Chống bẫy thanh khoản Thứ Bảy
            & (~is_sunday)                                # Chống bẫy thanh khoản Chủ Nhật
            & (~is_monday_morning)                        # Chống bẫy fakeout rạng sáng Thứ Hai
            & (~is_monday_us_open)                         # Chống bẫy quét thanh khoản phiên Mỹ Thứ Hai
            & (~btc_bullish)
        )

        # TAG 702: MACD Zero-Line Rejection & Momentum
        shift_macdhist = np.roll(macdhist, 1)
        shift_low_12 = np.roll(rolling_low_12, 1)
        cond_702 = (
            (volume > 0)
            & (ema_50 < ema_200)                          # Bắt buộc Downtrend khung lớn
            & (~close_above_ema200_1h)                    # NÂNG CẤP TẦNG 1: Tuyệt đối không Short khi nến nằm trên 1H EMA 200 (chống bẫy ngược sóng lớn)
            & (macd < 0.0)                                # MACD nằm dưới đường Zero
            & (macdhist < 0.0)                            # Histogram âm
            & (macdhist < shift_macdhist)                 # Gia tốc giảm mạnh dần
            & (close < ema_21) & (close < ema_50)
            & (close < open_px)
            & (lower_wick_ratio <= 0.40)                  # NÂNG CẤP HƯỚNG 1: Nến xả dứt khoát, loại bỏ bẫy rút chân pinbar (râu dưới > 40%)
            & (vol_spike_ratio >= 1.20)                   # Lực bán đột biến xác nhận
            & (vol_spike_ratio <= 5.0)                    # Loại bỏ volume dị biệt selling climax
            & (rsi_14 > 28.0) & (rsi_14 < 48.0)
            & (stochrsi_k >= 20.0)                        # BẢO VỆ CHỐNG BÁN ĐÁY: Không short khi StochRSI đã cạn kiệt ở đáy
            & ((close < shift_low_12) | btc_dumping)
            & (~rsi_1h_oversold)                          # Không short khi 1h đã quá bán sâu < 30
            & (~is_saturday)                              # Chống bẫy thanh khoản Thứ Bảy
            & (~is_sunday)                                # Chống bẫy thanh khoản Chủ Nhật
            & (~is_monday_morning)                        # Chống bẫy fakeout rạng sáng Thứ Hai
            & (~is_monday_us_open)                         # Chống bẫy quét thanh khoản phiên Mỹ Thứ Hai
            & (~btc_bullish)                              # Không short khi BTC đang tăng dốc
        )

        # TAG 721: Relief Bounce Rejection tại EMA 21 trong Downtrend (Tối ưu hóa chuyên sâu)
        shift_ema_21 = np.roll(ema_21, 1)
        prev_candle_green = np.roll(close, 1) > np.roll(open_px, 1)
        cond_721 = (
            (volume > 0)
            & (ema_50 < ema_200)                          # Downtrend tổng thể
            & (ema_21 < shift_ema_21)                     # EMA 21 dốc xuống xác nhận cản động
            & prev_candle_green                           # Nến trước đó là nhịp hồi xanh
            & (high >= ema_21 * 0.9995)                   # Quét chạm hoặc vượt nhẹ qua EMA 21
            & (close < ema_21)                            # Đóng nến dưới EMA 21
            & (close < ema_9)                             # Xác nhận lực xả dưới cả EMA 9
            & (close < open_px)                           # BẮT BUỘC NẾN ĐỎ
            & (upper_wick_ratio >= 0.40)                  # Râu xả rõ ràng
            & (vol_spike_ratio >= 1.25)                   # Volume bán xác nhận
            & (rsi_14 >= 42.0) & (rsi_14 <= 58.0)
            & (~rsi_1h_oversold)                          # Không short khi 1h đã quá bán sâu < 30
            & (~rsi_1h_overbought)                        # Không short khi 1h đang uptrend mạnh
            & (~is_sunday)                                # Chống bẫy thanh khoản Chủ Nhật
            & (~is_monday_morning)                        # Chống bẫy fakeout rạng sáng Thứ Hai
            & (~btc_bullish)                              # Không short khi BTC đang tăng dốc
        )

        # TAG 722: StochRSI Overbought Cross-down trong Downtrend
        shift_k = np.roll(stochrsi_k, 1)
        shift_d = np.roll(stochrsi_d, 1)
        cross_down = (shift_k >= shift_d) & (stochrsi_k < shift_d)
        cond_722 = (
            (volume > 0)
            & (ema_50 < ema_200)
            & (close < ema_21)
            & cross_down
            & (shift_k >= 75.0)
            & (close < open_px)
            & (vol_spike_ratio >= 1.20)
            & (~rsi_1h_oversold)                          # Không short khi 1h đã quá bán sâu < 30
            & (~is_sunday)                                # Chống bẫy thanh khoản Chủ Nhật
            & (~is_monday_morning)                        # Chống bẫy fakeout rạng sáng Thứ Hai
            & (~btc_bullish)                              # Không short khi BTC đang tăng dốc
        )

        # TAG 723: Upper Bollinger Band Rejection Scalp
        shift_bbm = np.roll(bbm, 3)
        cond_723 = (
            (volume > 0)
            & (ema_50 < ema_200)
            & (high >= bbu * 0.998)
            & (close < bbu * 0.995)
            & (bbm < shift_bbm)
            & (close < open_px)
            & (upper_wick_ratio >= 0.42)
            & (vol_spike_ratio >= 1.20)
            & (rsi_14 >= 58.0)
            & (~is_sunday)                                # Chống bẫy thanh khoản Chủ Nhật
            & (~is_monday_morning)                        # Chống bẫy fakeout rạng sáng Thứ Hai
            & (~btc_bullish)                              # Không short khi BTC đang tăng dốc
        )

        # TAG 724: EMA 50 Relief Bounce Rejection (Từ chối hồi kỹ thuật tại EMA 50)
        shift_ema_50 = np.roll(ema_50, 1)
        prev_candle_green = np.roll(close, 1) > np.roll(open_px, 1)
        cond_724 = (
            (volume > 0)
            & (ema_50 < ema_200)                          # Downtrend tổng thể
            & (ema_50 < shift_ema_50)                     # EMA 50 đang dốc xuống xác nhận cản động
            & (high >= ema_50 * 0.9995)                   # Quét chạm hoặc vượt nhẹ qua EMA 50
            & (close < ema_50)                            # Đóng cửa bị đạp xuống dưới EMA 50
            & (close < ema_21)                            # Đóng nến dưới EMA 21 xác nhận lực xả
            & (close < open_px)                           # BẮT BUỘC NẾN ĐỎ
            & (upper_wick_ratio >= 0.38)                  # Râu trên dài thể hiện áp lực bán từ chối
            & (vol_spike_ratio >= 1.25)                   # Volume xả xác nhận
            & (rsi_14 >= 44.0) & (rsi_14 <= 58.0)         # Vùng RSI hồi kỹ thuật điển hình
            & (prev_candle_green | (high >= ema_50))      # Thực sự có nhịp hồi trước đó hoặc râu đâm qua EMA 50
            & (~rsi_1h_oversold)                          # Không short khi 1h đã quá bán sâu < 30
            & (~rsi_1h_overbought)                        # Không short khi 1h đang quá mua/parabolic
            & (~is_sunday)                                # Chống bẫy thanh khoản Chủ Nhật
            & (~is_monday_morning)                        # Chống bẫy fakeout rạng sáng Thứ Hai
            & (~btc_bullish)                              # Không short khi BTC đang tăng dốc
        )

        # TAG 705: Bollinger Band Squeeze Breakdown (Nén dải BB và sập gãy - Tối ưu hóa chuyên sâu Phương án 1)
        cond_705 = (
            (volume > 0)
            & (ema_50 < ema_200)                          # Bắt buộc Downtrend tổng thể
            & (close < ema_21)                            # Đóng cửa dưới EMA 21
            & (bb_width < bb_width_sma_20 * 0.85)         # Biên độ dải BB co thắt mạnh hơn 15% so với SMA20
            & (close < bbl)                               # Đóng cửa gãy thủng dải dưới BB
            & (close < open_px)                           # BẮT BUỘC NẾN ĐỎ
            & (body_ratio >= 0.50)                        # Thân nến giảm dứt khoát chiếm >= 50% biên độ
            & (upper_wick_ratio <= 0.35)                  # Râu trên ngắn xác nhận phe bán áp đảo, không bị rút chân
            & (vol_spike_ratio >= 1.60)                   # Volume bùng nổ vượt trội xác nhận breakout
            & (vol_spike_ratio <= 3.50)                   # GIỚI HẠN TRẦN: Loại bỏ volume bán tháo dị biệt selling climax (hạ từ 5.0 xuống 3.50)
            & (macdhist < 0.0)                            # MACD Histogram âm
            & (macdhist < shift_macdhist)                 # Đà xả đang gia tốc
            & (rsi_14 >= 33.0)                            # CHỐNG BÁN ĐÁY: Không short khi RSI đã quá bán cạn kiệt
            & (stochrsi_k >= 30.0)                        # Chưa quá bán ở đáy 5m (tránh bán đáy)
            & (~rsi_1h_oversold)                          # Không short khi 1h đã quá bán sâu < 30 (chống bẫy kiệt sức)
            & (~rsi_1h_overbought)                        # Không short khi 1h đang uptrend mạnh
            & (~is_saturday)                              # Chống bẫy thanh khoản Thứ Bảy
            & (~is_sunday)                                # Chống bẫy thanh khoản Chủ Nhật
            & (~is_monday_morning)                        # Chống bẫy fakeout quét thanh khoản mở nến tuần rạng sáng Thứ Hai
            & (~is_monday_us_open)                         # Chống bẫy quét thanh khoản phiên Mỹ Thứ Hai
            & (~btc_bullish)                              # Không short khi BTC đang tăng dốc
        )

        # TAG 725: Bearish RSI Divergence Exhaustion (Phân kỳ giảm giá RSI khung 5m)
        shift_rsi_max_24 = np.roll(rolling_rsi_max_24, 1)
        cond_725 = (
            (volume > 0)
            & (high > shift_high_24)                      # Giá tạo đỉnh cao mới so với 24 nến trước (2 giờ)
            & (rsi_14 < shift_rsi_max_24)                 # Nhưng RSI lại thấp hơn đỉnh RSI tương ứng (Phân kỳ đỉnh)
            & (close < shift_high_24)                     # Đóng cửa thất bại dưới đỉnh cũ (Fakeout rõ ràng)
            & (close < open_px)                           # BẮT BUỘC NẾN ĐỎ
            & (upper_wick_ratio >= 0.40)                  # Râu trên dài từ chối giá
            & (rsi_14 >= 58.0)                            # RSI ở vùng phân phối
            & (vol_spike_ratio >= 1.25)                   # Volume xả phân phối
            & (~is_sunday)                                # Chống bẫy thanh khoản Chủ Nhật
            & (~is_monday_morning)                        # Chống bẫy fakeout rạng sáng Thứ Hai
            & (~btc_bullish)                              # Không short khi BTC đang tăng dốc
        )

        # TAG 706: Donchian 48-Period Macro Breakdown (Gãy hỗ trợ lớn 4 giờ)
        # Nâng cấp Phương án A: Thêm giới hạn trần volume chống selling climax,
        # nâng bộ lọc RSI/StochRSI chống bán đáy cạn kiệt, bắt buộc nến đỏ xác nhận.
        shift_low_48 = np.roll(rolling_low_48, 1)
        cond_706 = (
            (volume > 0)
            & (close < shift_low_48)                      # Gãy thủng đáy 48 nến (4 giờ tích lũy sụp đổ)
            & (close < open_px)                           # BẮT BUỘC NẾN ĐỎ
            & (lower_wick_ratio <= 0.25)                  # Râu dưới rất ngắn (lực bán một chiều, không rút chân)
            & (close < ema_9) & (close < ema_21) & (close < ema_50)  # Nằm dưới EMA 9, 21, 50
            & (vol_spike_ratio >= 1.40)                   # Volume xả đột biến
            & (vol_spike_ratio <= 3.50)                   # GIỚI HẠN TRẦN: Chống bẫy selling climax hoảng loạn
            & (rsi_14 >= 33.0)                            # CHỐNG BÁN ĐÁY: Không short khi RSI đã quá bán cạn kiệt
            & (stochrsi_k >= 25.0)                        # Chống bán tháo ở đáy cạn kiệt
            & btc_dumping                                 # Đồng pha BTC xả mạnh trên 4h
            & (~is_saturday)                              # Chống bẫy thanh khoản Thứ Bảy
            & (~is_sunday)                                # Chống bẫy thanh khoản Chủ Nhật
            & (~is_monday_morning)                        # Chống bẫy fakeout rạng sáng Thứ Hai
            & (~is_monday_us_open)                         # Chống bẫy quét thanh khoản phiên Mỹ Thứ Hai
            & (~btc_bullish)                              # Không short khi BTC đang tăng dốc
        )

        # =========================================================================
        # CONFLUENCE ENGINE: LỌC SẠCH NHIỄU - CHỈ VÀO KHI HỘI TỤ ĐỦ ĐIỀU KIỆN CHẤT LƯỢNG CAO
        # =========================================================================

        # Setup 1: Exhaustion Confluence - ĐÃ TẮT ĐỂ TRIỆT TIÊU 100% NHIỄU BẮT ĐỈNH TRONG SÓNG TĂNG
        trigger_exhaustion = np.zeros(n_rows, dtype=bool)

        # Setup 2: Trend Breakdown Confluence có Retest (Không bán đuổi đáy)
        # Nến xả phải có râu test lại gần EMA 9 (high >= ema_9 * 0.997) và đóng đỏ dưới EMA 9
        retest_confirmed = (high >= ema_9 * 0.997) & (close < ema_9)
        trigger_breakdown = cond_703 & cond_731 & (cond_702 | cond_701) & retest_confirmed

        # Setup 3: Relief Rejection Confluence (EMA21 Rejection đi kèm BTC dump VÀ MACD đà giảm)
        trigger_rejection = cond_721 & cond_731 & cond_702 if self.enable_short_relief_rejection else np.zeros(n_rows, dtype=bool)

        # Setup 4: Scalp Pullback Confluence (StochRSI cross-down từ vùng cao trong Ribbon downtrend - 100% Winrate)
        trigger_scalp = cond_722 & cond_703 & cond_731

        # Setup 5: EMA 50 Relief Bounce Rejection (Chạm cản EMA 50 bị đạp xuống mạnh)
        trigger_ema50_reject = cond_724 & cond_731

        # Setup 6: BB Squeeze Breakdown (Thắt nút cổ chai BB bùng nổ theo chiều giảm)
        trigger_bb_squeeze = cond_705 & (cond_703 | cond_702) if self.enable_short_bb_squeeze else np.zeros(n_rows, dtype=bool)

        # Setup 7: Bearish Divergence Exhaustion (Phân kỳ đỉnh RSI cạn kiệt đà tăng)
        trigger_bear_div = cond_725 & cond_731

        # Setup 8: Macro 48-Period Donchian Breakdown có Retest (Không bán đuổi đáy nến xả)
        trigger_macro_breakdown = cond_706 & cond_731 & retest_confirmed

        # Setup 9: BB Upper Rejection Scalp (Chạm dải trên dốc xuống bị từ chối)
        trigger_bb_rejection = cond_723 & cond_731

        # BỘ LỌC VĨ MÔ QUY TẮC VÀNG: BẮT BUỘC DOWNTREND KHUNG LỚN & KHÔNG BÁN ĐÁY QUÁ BÁN
        # Tuyệt đối cấm Short bất kỳ coin nào đang nằm trên EMA 200 hoặc khi RSI đã rơi vào vùng quá bán sâu (<32)
        macro_bearish_regime = (
            (close < ema_200)
            & (ema_50 < ema_200)
            & (~rsi_1h_overbought)
            & (close < open_px)
            & (rsi_14 > 30.0)
        )

        # TỔNG HỢP ĐIỀU KIỆN ĐỦ ĐỂ VÀO LỆNH (ĐÃ LỌC SẠCH NHIỄU)
        qualified_entry = (
            trigger_breakdown
            | trigger_rejection
            | trigger_scalp
            | trigger_ema50_reject
            | trigger_bb_squeeze
            | trigger_bear_div
            | trigger_macro_breakdown
            | trigger_bb_rejection
        ) & macro_bearish_regime

        # Gán nhãn các tag cho những cây nến ĐẠT TIÊU CHUẨN CONFLUENCE
        idxs = np.where(qualified_entry)[0]
        if len(idxs) > 0:
            enter_short_custom[idxs] = 1
            all_signals = [
                (cond_711, "711"),
                (cond_712, "712"),
                (cond_713, "713"),
                (cond_701, "701"),
                (cond_702, "702"),
                (cond_703, "703"),
                (cond_705, "705"),
                (cond_706, "706"),
                (cond_721, "721"),
                (cond_722, "722"),
                (cond_723, "723"),
                (cond_724, "724"),
                (cond_725, "725"),
                (cond_731, "731"),
            ]
            for sig_mask, tag in all_signals:
                active_idxs = np.intersect1d(idxs, np.where(sig_mask)[0])
                for i in active_idxs:
                    cur = enter_tag_custom[i]
                    enter_tag_custom[i] = tag if not cur else f"{cur} {tag}"

        dataframe["enter_short_custom"] = enter_short_custom
        dataframe["enter_tag_custom"] = enter_tag_custom

        return dataframe

    def custom_exit(
        self,
        pair: str,
        trade,
        current_time: datetime,
        current_rate: float,
        current_profit: float,
        last_candle: Series,
        previous_candle: Series,
    ) -> Tuple[bool, Optional[str]]:
        """
        Bộ quy tắc thoát lệnh chuyên biệt cho các vị thế Short mới (701..731):
          1. Chốt lời theo mục tiêu (Swing / Scalp)
          2. Chốt lời sớm khi giá rơi vào vùng quá bán sâu (tránh nhịp rút chân)
          3. Khóa lợi nhuận (Profit lock) khi có lãi nhưng xuất hiện tín hiệu đảo chiều
          4. Cắt lỗ chặt (Invalidation SL) để phòng tránh Short Squeeze
          5. Thoát lệnh quá hạn (Time-based stale exit) nếu thị trường đi ngang ngưng giảm
        """
        enter_tag = getattr(trade, "enter_tag", "") or ""
        enter_tags = enter_tag.split()

        # Nhận diện nhóm tag
        is_scalp = any(t in ["721", "722", "723", "724"] for t in enter_tags)
        is_exhaustion = any(t in ["711", "712", "713", "714", "725"] for t in enter_tags)
        is_breakdown = any(t in ["701", "702", "703", "705", "706", "731"] for t in enter_tags)

        # 1. Take Profit Targets
        if is_scalp and current_profit >= self.tp_target_scalp:
            return True, "custom_short_tp_scalp"

        if is_exhaustion and current_profit >= self.tp_target_swing:
            return True, "custom_short_tp_swing"

        if current_profit >= 0.028:
            return True, "custom_short_tp_target"

        # 2. Oversold Bounce Exit (RSI <= 24 hoặc giá xuyên thủng dải dưới BBL)
        rsi_14 = last_candle.get("RSI_14", 50.0)
        bbl = last_candle.get("BBL_20_2.0", current_rate * 0.95)
        if current_profit >= self.tp_target_oversold:
            if rsi_14 <= 24.0 or current_rate <= bbl:
                return True, "custom_short_tp_oversold_bounce"

        # 3. Profit Lock: Khi đã có lãi >= +2.0%, nếu có nến rút chân dài hoặc vượt EMA 21 thì chốt lời ngay
        ema_21 = last_candle.get("EMA_21", None)
        lower_wick_ratio = last_candle.get("lower_wick_ratio", 0.0)
        if current_profit >= 0.020:
            if lower_wick_ratio >= 0.40 or (ema_21 is not None and last_candle["close"] > ema_21):
                return True, "custom_short_profit_lock"

        # 4. Invalidation Stoploss (Phòng ngừa Short Squeeze)
        if is_scalp and current_profit <= self.invalidation_sl_tight:
            return True, "custom_short_scalp_tight_sl"

        if current_profit <= self.invalidation_sl_wide:
            return True, "custom_short_wide_sl"

        # 5. Structural Invalidation: Chỉ áp dụng cho Breakdown khi vượt ngược lên trên EMA 50
        if is_breakdown:
            ema_50 = last_candle.get("EMA_50", None)
            if ema_50 is not None and last_candle["close"] > ema_50 * 1.015 and current_profit < -0.018:
                return True, "custom_short_ema50_invalidation"

        # 6. Time-based Stale Exit: Nếu giữ hơn 4 giờ (240 phút) mà vẫn âm nhẹ, chốt lệnh để giải phóng vốn
        open_date = getattr(trade, "open_date_utc", None)
        if open_date is not None:
            trade_duration_min = (current_time - open_date).total_seconds() / 60
            if trade_duration_min >= 240 and current_profit < -0.008:
                return True, "custom_short_time_stale_exit"

        return False, None
