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
        return f"{base_ver} + CustomShortSignals_v3.5_Apex_Shield"

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

    def populate_indicators(self, df: DataFrame, metadata: dict) -> DataFrame:
        """
        1. Run all standard NFIX8 indicator calculations.
        2. Run modular Short indicator calculations.
        """
        # Base NFIX8 indicators across all timeframes (5m, 15m, 1h, 4h, 1d, BTC)
        df = super().populate_indicators(df, metadata)

        # Additional Short-specific indicators
        df = self.short_strategy.populate_indicators(df, metadata)

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
        Delegates fully to NostalgiaForInfinityX8 native exit pipeline to allow
        dynamic trailing, bad trade controller, and multi-tier take-profit mechanisms.
        """
        try:
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
        if side == "short":
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

            # 2. Monday US Open Guard: Chặn bẫy quét thanh khoản phiên Mỹ thứ Hai (13:00 - 15:00 UTC)
            # Triệt tiêu các cú stop-hunt giả phá đáy đầu tuần của cá mập (như ca ARB -97 USDT ngày 31/08).
            # Đặc biệt chặn các lệnh bán đuổi phá đáy (breakdown setups: 701, 702, 703, 705, 706) dễ bị dính bear trap.
            if current_time.weekday() == 0 and 13 <= current_time.hour < 15:
                if any(t in ["701", "702", "703", "705", "706"] for t in tags):
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

                # 3. BTC Oversold Exhaustion Trap Guard (Upgrade 1):
                # Chặn mở mới lệnh Short breakdown (701, 706) khi BTC 1h rơi vào vùng cạn kiệt bán tháo (34.0 <= RSI <= 37.5),
                # nơi cá mập thường giăng bẫy đảo chiều chữ V (Bear Trap triệt tiêu OP -96 USDT và AVAX -101.56 USDT).
                if any(t in ["701", "706"] for t in tags) and btc_rsi1h is not None and 34.0 <= btc_rsi1h <= 37.5:
                    log.info(
                        "BTC Oversold Exhaustion Guard: Blocked %s breakdown short (%s) due to BTC 1h RSI %.1f in bear trap zone [34.0, 37.5] at %s",
                        pair, entry_tag, btc_rsi1h, current_time,
                    )
                    return False

                # 4. BTC Momentum Filter cho Relief Bounces (Upgrade 3):
                # Không Short bắt đỉnh hồi kỹ thuật chạm EMA (721, 724) khi BTC đang có đà phục hồi mạnh
                # (RSI 15m > 54.0 hoặc RSI 1h > 54.0), tránh chặn đầu xe lửa khi thị trường đang dồn lực hồi phục (triệt tiêu DOT -94.73 USDT).
                if any(t in ["721", "724"] for t in tags):
                    has_btc_bull_mom = (btc_rsi15m is not None and btc_rsi15m > 54.0) or (btc_rsi1h is not None and btc_rsi1h > 54.0)
                    if has_btc_bull_mom:
                        log.info(
                            "BTC Momentum Filter: Blocked %s relief bounce short (%s) due to strong BTC bullish momentum (RSI 15m: %s, 1h: %s) at %s",
                            pair, entry_tag, f"{btc_rsi15m:.1f}" if btc_rsi15m else "N/A", f"{btc_rsi1h:.1f}" if btc_rsi1h else "N/A", current_time,
                        )
                        return False

                # 5. Correlation / Market Breadth Guard (1h):
                # Khi đã có >= 2 lệnh Short đang mở, kiểm tra xem BTC có đang hồi phục không:
                if len(open_shorts) >= 2 and btc_close is not None and btc_ema21 is not None and btc_close > btc_ema21:
                    log.info(
                        "Market Breadth Guard (1h): Blocked %s short entry (%d active shorts & BTC 1h close %.1f > EMA21 %.1f at %s)",
                        pair, len(open_shorts), btc_close, btc_ema21, current_time,
                    )
                    return False

                # Kiểm tra BTC 5m (nếu BTC 5m đang hồi dốc trên EMA 21)
                if len(open_shorts) >= 2:
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
