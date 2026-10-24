# -*- coding: utf-8 -*-
"""
NostalgiaForInfinityX8_Combined
Wrapper Strategy combining NostalgiaForInfinityX8 with modular custom Short logic.
"""
import logging
from datetime import datetime
from typing import Optional
import numpy as np
import pandas as pd
from pandas import DataFrame

from freqtrade.persistence import Trade, Order
import talib.abstract as ta
from NostalgiaForInfinityX8 import NostalgiaForInfinityX8
from NostalgiaForInfinityX8_ShortSignals import NostalgiaForInfinityX8_ShortSignals

log = logging.getLogger(__name__)


class NostalgiaForInfinityX8_Combined(NostalgiaForInfinityX8):
    """
    Combined Trading Strategy:
      - Base: NostalgiaForInfinityX8 (Full Long/Short, DCA/Grind v2-v4, Bad Trade Controller)
      - Extension: NostalgiaForInfinityX8_ShortSignals (Modular Short Entry & Exit Controller)
    """

    INTERFACE_VERSION = 3

    # Safety stoploss for Futures (80% margin loss)
    stoploss = -0.80

    # Futures leverage 5.0x
    futures_mode_leverage: float = 5.0
    futures_mode_leverage_rebuy_mode: float = 5.0
    futures_mode_leverage_grind_mode: float = 5.0

    def version(self) -> str:
        base_ver = super().version()
        return f"{base_ver} + CustomShortSignals_v3.6.3_Layer1_Layer2 + AsymmetricSmartDCA"

    def __init__(self, config: dict) -> None:
        super().__init__(config)
        self.stoploss = -0.80
        self.futures_mode_leverage = 5.0
        self.futures_mode_leverage_rebuy_mode = 5.0
        self.futures_mode_leverage_grind_mode = 5.0

        # Initialize the modular Short Strategy
        self.short_strategy = NostalgiaForInfinityX8_ShortSignals(config)

        # Register custom short tags into NFIX8 tag categories so that all downstream
        # subsystems (order tracking, position sizing, cache, exits) recognize them seamlessly.
        for tag in self.short_strategy.custom_short_tags:
            if tag not in self.short_normal_mode_tags:
                self.short_normal_mode_tags.append(tag)
            if tag not in self.short_known_mode_tags:
                self.short_known_mode_tags.append(tag)
            if tag not in self.short_exit_known_mode_tags:
                self.short_exit_known_mode_tags.append(tag)

        log.info(
            "NostalgiaForInfinityX8_Combined successfully initialized with custom short tags: %s",
            self.short_strategy.custom_short_tags,
        )

    def informative_pairs(self):
        """
        Extend informative pairs to include BTC 1h and 15m data for market breadth correlation tracking.
        """
        pairs = super().informative_pairs()
        btc_pair = self.btc_informative_pair()
        if (btc_pair, "1h") not in pairs:
            pairs.append((btc_pair, "1h"))
        if (btc_pair, "15m") not in pairs:
            pairs.append((btc_pair, "15m"))
        return pairs

    def informative_1h_indicators(self, metadata: dict, info_timeframe) -> DataFrame:
        """
        Extend base 1h informative indicators with EMA 50 to enable 1h Golden/Death Cross structural tracking.
        """
        inf_1h = super().informative_1h_indicators(metadata, info_timeframe)
        if not inf_1h.empty and "close" in inf_1h.columns:
            inf_1h["EMA_50"] = ta.EMA(inf_1h["close"].to_numpy(copy=False), timeperiod=50)
        return inf_1h

    def populate_indicators(self, df: DataFrame, metadata: dict) -> DataFrame:
        """
        1. Run all standard NFIX8 indicator calculations.
        2. Run modular Short indicator calculations.
        3. Downcast float64 to float32 to reduce memory footprint by 50% for 100+ pair backtests.
        """
        # Base NFIX8 indicators across all timeframes (5m, 15m, 1h, 4h, 1d, BTC)
        df = super().populate_indicators(df, metadata)

        # Additional Short-specific indicators
        df = self.short_strategy.populate_indicators(df, metadata)

        # Memory optimization for 100+ pair backtests on Colab:
        # Preserve OHLCV columns as float64 to pass Freqtrade sanity check; downcast 240+ indicator columns to float32
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

        # Free non-BTC informative dataframes from DataProvider cache to prevent RAM accumulation
        if hasattr(self, "dp") and self.dp is not None:
            if hasattr(self.dp, "_DataProvider__cached_pairs_backtesting"):
                for k in list(self.dp._DataProvider__cached_pairs_backtesting.keys()):
                    if "BTC" not in k[0]:
                        del self.dp._DataProvider__cached_pairs_backtesting[k]
            if hasattr(self.dp, "_DataProvider__cached_pairs"):
                for k in list(self.dp._DataProvider__cached_pairs.keys()):
                    if "BTC" not in k[0]:
                        del self.dp._DataProvider__cached_pairs[k]

        import gc, ctypes
        gc.collect()
        try:
            ctypes.CDLL("libc.so.6").malloc_trim(0)
        except Exception:
            pass

        return df

    def populate_entry_trend(self, df: DataFrame, metadata: dict) -> DataFrame:
        """
        1. Run NFIX8 base entry signals (all Long modes & base Short modes).
        2. Run modular Short entry signals.
        3. Merge signals safely:
           - Prevents concurrent Long/Short signals on the same candle.
           - Appends custom short tags to 'enter_tag' without erasing existing NFI tags.
        """
        # Run base NFIX8 entry generation
        df = super().populate_entry_trend(df, metadata)

        # Run custom short entry generation
        df = self.short_strategy.populate_entry_trend(df, metadata)

        # Merge Short Entry signals
        if "enter_short_custom" in df.columns:
            # Custom short trigger mask
            custom_short_trigger = df["enter_short_custom"] == 1
            
            # Anti-conflict guard: do not short if long entry is also firing on this candle
            safe_short_trigger = custom_short_trigger & (df["enter_long"] == 0)

            # Activate enter_short flag
            df.loc[safe_short_trigger, "enter_short"] = 1

            # Merge enter_tag column cleanly
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

        import gc, ctypes
        gc.collect()
        try:
            ctypes.CDLL("libc.so.6").malloc_trim(0)
        except Exception:
            pass

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
        Custom Exit Management for Combined Strategy:
        1. Dead-Trade Momentum Failure Cut:
           If trade has been open >= 24h, MFE never reached +0.8% leveraged (0.16% price),
           and current profit is <= -40% (-8% price), cut early to avoid full -95% stoploss doom.
        2. Delegates to NostalgiaForInfinityX8 native exit pipeline for all standard exits.
        """
        try:
            trade_duration_hours = (current_time - trade.open_date_utc).total_seconds() / 3600.0
            leverage = trade.leverage or 5.0
            open_rate = trade.open_rate
            enter_tag = trade.enter_tag if hasattr(trade, "enter_tag") and trade.enter_tag else "empty"

            if trade.is_short:
                min_r = trade.min_rate if trade.min_rate is not None else open_rate
                mfe_lev = (open_rate - min_r) / open_rate * leverage

                # Phương án 1 - Breakeven Protection Lock cho Breakdown Setups (Tag 705, 706):
                # Nếu lệnh có Tag 705 hoặc 706 từng đạt lãi >= +1.5% giá (+7.5% đòn bẩy),
                # mà hiện tại giá quay đầu về mức hòa vốn (<= +0.5% đòn bẩy = +0.1% giá),
                # thoát lệnh ngay để bảo toàn vốn và tiền phí sàn, chống đảo chiều thành lỗ sâu.
                if any(t in enter_tag for t in ["705", "706"]) and mfe_lev >= 0.075 and current_profit <= 0.005:
                    return f"exit_short_breakeven_lock ( {enter_tag})"

                # Phương án 1 - Quick Scalp Take Profit cho Breakdown Setups (Tag 705, 706):
                # Nếu lệnh có Tag 705 hoặc 706 đạt mức lãi >= +1.8% giá (+9.0% đòn bẩy),
                # chốt lời sớm để hiện thực hóa lợi nhuận của nhịp breakdown ngắn hạn.
                if any(t in enter_tag for t in ["705", "706"]) and current_profit >= 0.090:
                    return f"exit_short_scalp_tp ( {enter_tag})"

                # Retrieve analyzed dataframe for structural awareness (EMA 50 and EMA 200 on 1h)
                is_1h_golden_cross = False
                was_gc_at_entry = False
                ema_200_1h = None
                ema_50_1h = None
                if hasattr(self, "dp") and self.dp is not None:
                    df_pair, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
                    if len(df_pair) > 0:
                        # Slice up to current_time to avoid future-peeking in backtests while working in live
                        current_rows = df_pair.loc[df_pair["date"] <= current_time]
                        last_c = current_rows.iloc[-1] if len(current_rows) > 0 else df_pair.iloc[-1]
                        
                        ema_50_1h = last_c.get("EMA_50_1h", None)
                        if ema_50_1h is None:
                            ema_50_1h = last_c.get("ema_50_1h", None)
                            
                        ema_200_1h = last_c.get("EMA_200_1h", None)
                        if ema_200_1h is None:
                            ema_200_1h = last_c.get("ema_200_1h", None)
                            
                        if ema_50_1h is not None and ema_200_1h is not None:
                            if not np.isnan(ema_50_1h) and not np.isnan(ema_200_1h):
                                is_1h_golden_cross = bool(ema_50_1h > ema_200_1h)

                        # Check structural regime at trade entry to prevent false cuts on counter-trend entries
                        trade_id = getattr(trade, "id", None) or f"{pair}_{trade.open_date_utc}"
                        if not hasattr(self, "_entry_gc_cache"):
                            self._entry_gc_cache = {}
                        if trade_id not in self._entry_gc_cache:
                            entry_rows = df_pair.loc[df_pair["date"] <= trade.open_date_utc]
                            if len(entry_rows) > 0:
                                entry_c = entry_rows.iloc[-1]
                                e_50 = entry_c.get("EMA_50_1h", None) or entry_c.get("ema_50_1h", None)
                                e_200 = entry_c.get("EMA_200_1h", None) or entry_c.get("ema_200_1h", None)
                                self._entry_gc_cache[trade_id] = bool(
                                    e_50 is not None and e_200 is not None and not np.isnan(e_50) and not np.isnan(e_200) and e_50 > e_200
                                )
                            else:
                                self._entry_gc_cache[trade_id] = False
                        was_gc_at_entry = self._entry_gc_cache[trade_id]

                # NÂNG CẤP TẦNG 2: Emergency Macro Inversion Cut (Thoát hiểm khẩn cấp khi đảo chiều 1H)
                # Nếu vị thế Short đang âm sâu (<= -50% đòn bẩy = -10% giá) VÀ giá bứt phá vượt lên trên
                # đường trung bình thể chế 1H EMA 200:
                # Lập tức thoát lệnh tại mức -50% thay vì gồng chịu chết đến Stop Loss -95%.
                if current_profit <= -0.50 and ema_200_1h is not None and not np.isnan(ema_200_1h) and ema_200_1h > 0:
                    if current_rate > ema_200_1h:
                        return f"exit_short_macro_inversion_cut ( {enter_tag})"

                # Tier 1: Dead-Trade Momentum Failure Cut (24h)
                # If trade has been open >= 24h, MFE never reached +0.8% leveraged (0.16% price),
                # and current profit is <= -40% (-8% price), cut early to avoid full -95% stoploss doom.
                if trade_duration_hours >= 24.0 and mfe_lev <= 0.008 and current_profit <= -0.40:
                    return f"exit_dead_trade_cut_24h ( {enter_tag})"

                # NÂNG CẤP 2 (Tinh chỉnh): Cắt sớm khi vi phạm cấu trúc xu hướng 1H (True Structural Inversion)
                # Chỉ cắt khi:
                # 1. Lúc vào lệnh: Cặp tiền đang ở Death Cross (vào lệnh thuận theo xu hướng giảm 1h)
                # 2. Sau >= 36h: Cấu trúc 1H bị đảo chiều tăng sang Golden Cross (EMA 50 > EMA 200)
                # 3. Vị thế đang âm sâu <= -25% đòn bẩy (-5% giá)
                if trade_duration_hours >= 36.0 and not was_gc_at_entry and is_1h_golden_cross and current_profit <= -0.25:
                    return f"exit_macro_golden_cross_cut ( {enter_tag})"

                # Tier 2: Dead Drift Cut (72h / 3 days) - KHÔI PHỤC NGUYÊN BẢN BASELINE:
                # Cắt dứt khoát tất cả vị thế trôi dạt sau 72h nếu lỗ <= -45%, ngăn chặn tuyệt đối zombie drift
                if trade_duration_hours >= 72.0 and current_profit <= -0.45:
                    return f"exit_dead_drift_cut_72h ( {enter_tag})"

                # Tier 3: Zombie Capital Freeing Cut (120h / 5 days)
                # If trade has been open >= 120h (5 days) and current profit is <= -35% (-7% price),
                # cut early to prevent multi-week stagnation, negative funding & massive drawdown.
                if trade_duration_hours >= 120.0 and current_profit <= -0.35:
                    return f"exit_zombie_trade_cut_5d ( {enter_tag})"
            else:
                max_r = trade.max_rate if trade.max_rate is not None else open_rate
                mfe_lev = (max_r - open_rate) / open_rate * leverage

            return super().custom_exit(
                pair=pair,
                trade=trade,
                current_time=current_time,
                current_rate=current_rate,
                current_profit=current_profit,
                **kwargs,
            )
        except PermissionError:
            return None
        except Exception as e:
            log.warning(f"Error in custom_exit: {e}")
            return None

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
        Entry Confirmation Guard:
          - Validates base NFIX8 entry checks.
          - In futures short mode, checks safety guards if applicable.
        """
        # Call base validation
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

        # Additional protection for short trades
        if side in ("short", "sell"):
            tags = entry_tag.split() if entry_tag else []
            open_trades = Trade.get_open_trades()
            open_shorts = [t for t in open_trades if getattr(t, "is_short", False)]

            # 1. Portfolio Exposure Guard: Giới hạn tối đa 4 lệnh Short đồng thời
            # Bảo toàn ít nhất 2 slot cho vị thế Long và triệt tiêu rủi ro đồng loạt cháy lệnh Short khi đảo chiều
            if len(open_shorts) >= 4:
                log.info(
                    "Portfolio Exposure Guard: Blocked %s short entry (%d active shorts >= 4 max limit)",
                    pair, len(open_shorts),
                )
                return False

            # 2. Saturday Liquidity Trap Guard: Chống bẫy thanh khoản mỏng cuối tuần Thứ Bảy (quét stop loss các lệnh breakdown)
            # Triệt tiêu các cú Stop Loss lớn nhất: DASH -92$, ONDO -90$, HYPE -90$, VVV -86$, RKLB -78$, ZEC -52$
            if current_time.weekday() == 5:
                if any(t in ["701", "702", "703", "705", "706", "731"] for t in tags):
                    log.info(
                        "Saturday Liquidity Trap Guard: Blocked %s breakdown short (%s) on low-liquidity Saturday (%s)",
                        pair, entry_tag, current_time,
                    )
                    return False

            # 3. Monday US Open & Pre-Market Guard: Chặn bẫy quét thanh khoản phiên Mỹ thứ Hai (12:00 - 15:00 UTC)
            # Triệt tiêu các cú stop-hunt giả phá đáy đầu tuần của cá mập (như ca ONDO -91.17$ lúc 12:10 UTC và ARB -97$).
            # Đặc biệt chặn các lệnh bán đuổi phá đáy (breakdown setups: 701, 702, 703, 705, 706, 731) dễ bị dính bear trap.
            if current_time.weekday() == 0 and 12 <= current_time.hour < 15:
                if any(t in ["701", "702", "703", "705", "706", "731"] for t in tags):
                    log.info(
                        "Monday US Open Guard: Blocked %s breakdown short (%s) during US opening volatility sweep (%s)",
                        pair, entry_tag, current_time,
                    )
                    return False
                # Chặn relief bounce short (721, 724) trong khung giờ mở cửa chính thức của phiên Mỹ thứ Hai (14:00 - 15:00 UTC, triệt tiêu DOT -94.73 USDT)
                if current_time.hour == 14 and any(t in ["721", "724"] for t in tags):
                    log.info(
                        "Monday US Open Guard (Relief Bounce): Blocked %s relief bounce short (%s) during US open peak sweep (%s)",
                        pair, entry_tag, current_time,
                    )
                    return False

            # BTC Data Context for Market Breadth & Macro Filter Guards
            if hasattr(self, "dp") and self.dp:
                btc_pair = self.btc_informative_pair()
                cur_ts = pd.to_datetime(current_time, utc=True)

                # Kiểm tra BTC 1h
                btc_df_1h = self.dp.get_pair_dataframe(pair=btc_pair, timeframe="1h")
                btc_close = None
                btc_ema21 = None
                btc_rsi1h = None
                if btc_df_1h is not None and not btc_df_1h.empty and "date" in btc_df_1h.columns:
                    btc_past_1h = btc_df_1h[btc_df_1h["date"] <= cur_ts]
                    if len(btc_past_1h) >= 25:
                        btc_close = btc_past_1h["close"].iloc[-1]
                        btc_ema21 = ta.EMA(btc_past_1h["close"].to_numpy(copy=False), timeperiod=21)[-1]
                        btc_rsi1h = ta.RSI(btc_past_1h["close"].to_numpy(copy=False), timeperiod=14)[-1]

                # Kiểm tra BTC 15m
                btc_df_15m = self.dp.get_pair_dataframe(pair=btc_pair, timeframe="15m")
                btc_rsi15m = None
                if btc_df_15m is not None and not btc_df_15m.empty and "date" in btc_df_15m.columns:
                    btc_past_15m = btc_df_15m[btc_df_15m["date"] <= cur_ts]
                    if len(btc_past_15m) >= 25:
                        btc_rsi15m = ta.RSI(btc_past_15m["close"].to_numpy(copy=False), timeperiod=14)[-1]

                # 4. Extreme BTC Capitulation Climax Floor (Option 1 Triad Shield):
                # Khi BTC 1h RSI <= 23.0 (như cú sập hoảng loạn Black Monday và TIA -98.68 USDT tại RSI 22.5),
                # thị trường rơi vào Selling Climax cực độ và áp lực thanh lý cưỡng bức, ngay trước cú giật nảy hình chữ V bão táp.
                # Tuyệt đối cấm mở bất kỳ vị thế Short nào tại vùng cạn kiệt bán tháo này.
                if btc_rsi1h is not None and btc_rsi1h <= 23.0:
                    log.info(
                        "BTC Capitulation Climax Guard: Blocked %s short (%s) due to extreme BTC 1h RSI panic %.1f <= 23.0 at %s",
                        pair, entry_tag, btc_rsi1h, current_time,
                    )
                    return False

                # 5. BTC Oversold Exhaustion Trap Guard (Upgrade 1 & Option 1 Tag 705 & Option C Tag 722):
                # Chặn mở mới lệnh Short breakdown / scalp (701, 705, 706, 722) khi BTC 1h rơi vào vùng cạn kiệt bán tháo:
                # - Quá bán cùng cực: btc_rsi1h <= 33.5 (như GOAT 30.4, XPL 24.2, ZK 33.1, ALGO 33.1)
                # - Vùng bẫy Bear Trap đảo chiều: 34.0 <= btc_rsi1h <= 37.5 (như HBAR 34.2, 1000PEPE 34.8, RKLB 35.5, ENA 36.9)
                if any(t in ["701", "705", "706", "722"] for t in tags) and btc_rsi1h is not None:
                    if btc_rsi1h <= 33.5 or (34.0 <= btc_rsi1h <= 37.5):
                        log.info(
                            "BTC Oversold Exhaustion Guard: Blocked %s short (%s) due to BTC 1h RSI %.1f at %s",
                            pair, entry_tag, btc_rsi1h, current_time,
                        )
                        return False

                # Chặn Tag 705 khi BTC 1h đang trong xu hướng tăng (Close > EMA21) - Triệt tiêu bẫy TIA -40.5 USDT
                if "705" in tags and btc_close is not None and btc_ema21 is not None and btc_close > btc_ema21:
                    log.info(
                        "BTC Bull Trend Guard: Blocked %s breakdown short (705) due to BTC 1h close %.1f > EMA21 %.1f at %s",
                        pair, entry_tag, btc_close, btc_ema21, current_time,
                    )
                    return False

                # 4. BTC Momentum Filter cho Relief Bounces, Scalp Pullbacks & Breakdown (Chặn bẫy short squeeze):
                # Không Short khi BTC đang có đà phục hồi mạnh (RSI 15m > 54.0 hoặc RSI 1h > 54.0),
                # tránh chặn đầu xe lửa khi thị trường đang dồn lực hồi phục (triệt tiêu STRK -22.64 USDT, ZEC -48.95 USDT).
                if any(t in ["702", "703", "721", "722", "724"] for t in tags):
                    has_btc_bull_mom = (btc_rsi15m is not None and btc_rsi15m > 54.0) or (btc_rsi1h is not None and btc_rsi1h > 54.0)
                    if has_btc_bull_mom:
                        log.info(
                            "BTC Momentum Filter: Blocked %s breakdown/relief short (%s) due to strong BTC bullish momentum (RSI 15m: %s, 1h: %s) at %s",
                            pair, entry_tag, f"{btc_rsi15m:.1f}" if btc_rsi15m else "N/A", f"{btc_rsi1h:.1f}" if btc_rsi1h else "N/A", current_time,
                        )
                        return False

                # 5. Correlation / Market Breadth Guard (1h):
                # Khi đã có >= 3 lệnh Short đang mở, kiểm tra xem BTC có đang hồi phục không:
                if len(open_shorts) >= 3 and btc_close is not None and btc_ema21 is not None and btc_close > btc_ema21:
                    log.info(
                        "Market Breadth Guard (1h): Blocked %s short entry (%d active shorts & BTC 1h close %.1f > EMA21 %.1f at %s)",
                        pair, len(open_shorts), btc_close, btc_ema21, current_time,
                    )
                    return False

                # Kiểm tra BTC 5m (nếu BTC 5m đang hồi dốc trên EMA 21)
                if len(open_shorts) >= 3:
                    btc_5m = self.dp.get_pair_dataframe(pair=btc_pair, timeframe="5m")
                    if btc_5m is not None and not btc_5m.empty and "date" in btc_5m.columns:
                        btc_past_5m = btc_5m[btc_5m["date"] <= cur_ts]
                        if len(btc_past_5m) >= 25:
                            btc_c_5m = btc_past_5m["close"].iloc[-1]
                            btc_e21_5m = ta.EMA(btc_past_5m["close"].to_numpy(copy=False), timeperiod=21)[-1]
                            if btc_c_5m > btc_e21_5m * 1.0010:
                                log.info(
                                    "Market Breadth Guard (5m): Blocked %s short entry (%d active shorts & BTC 5m close %.1f > EMA21 %.1f at %s)",
                                    pair, len(open_shorts), btc_c_5m, btc_e21_5m, current_time,
                                )
                                return False

            if entry_tag:
                tags = entry_tag.split()
                # If entering via custom short, perform optional risk checks
                if any(t in self.short_strategy.custom_short_tags for t in tags):
                    # E.g., ensure bot is operating in a futures-enabled configuration
                    if not getattr(self, "trading_mode", "spot") == "futures" and not self.config.get("trading_mode") == "futures":
                        log.warning("Short trade attempted on non-futures mode: rejecting pair %s", pair)
                        return False

        return True

    def leverage(
        self,
        pair: str,
        current_time: datetime,
        current_rate: float,
        proposed_leverage: float,
        max_leverage: float,
        entry_tag: Optional[str],
        side: str,
        **kwargs,
    ) -> float:
        """
        Delegate 100% to NostalgiaForInfinityX8 native leverage mechanism:
        uses futures_mode_leverage, grind mode leverage, and rebuy mode leverage.
        """
        lev = super().leverage(
            pair=pair,
            current_time=current_time,
            current_rate=current_rate,
            proposed_leverage=proposed_leverage,
            max_leverage=max_leverage,
            entry_tag=entry_tag or "",
            side=side,
            **kwargs,
        )
        return min(lev, max_leverage) if max_leverage else lev

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
        Asymmetric Smart DCA Gatekeeper:
        1. SHORT PROTECTION: CẤM 100% việc nhồi Short khi giá đang tăng ngược xu hướng (Veto Short Rebuy 'r').
        2. LONG PROTECTION: Bảo toàn 100% cơ chế Grinding / Rebuy / De-risk đa tầng của Nostalgia cho Long.
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

        adj_amount = adj[0] if isinstance(adj, (tuple, list)) else adj
        if adj_amount is None:
            return adj

        if adj_amount <= 0:
            return adj

        if trade.is_short:
            return None

        return adj

