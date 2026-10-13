# -*- coding: utf-8 -*-
"""
NostalgiaForInfinityX8_Combined
Wrapper Strategy combining NostalgiaForInfinityX8 with modular custom Short logic.
"""
import logging
from datetime import datetime
from typing import Optional
import numpy as np
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
        return f"{base_ver} + CustomShortSignals_v3.4_Apex_Shield"

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
        Extend informative pairs to include BTC 1h data for market breadth correlation tracking.
        """
        pairs = super().informative_pairs()
        btc_pair = self.btc_informative_pair()
        if (btc_pair, "1h") not in pairs:
            pairs.append((btc_pair, "1h"))
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

            # 2. Correlation / Market Breadth Guard:
            # Khi đã có >= 2 lệnh Short đang mở, kiểm tra xem BTC có đang hồi phục không:
            if len(open_shorts) >= 2 and hasattr(self, "dp") and self.dp:
                btc_pair = self.btc_informative_pair()
                # Kiểm tra BTC 1h
                btc_df = self.dp.get_pair_dataframe(pair=btc_pair, timeframe="1h")
                if btc_df is not None and not btc_df.empty and "date" in btc_df.columns:
                    btc_past = btc_df[btc_df["date"] <= current_time]
                    if len(btc_past) >= 25:
                        btc_close = btc_past["close"].iloc[-1]
                        btc_ema21 = ta.EMA(btc_past["close"].to_numpy(copy=False), timeperiod=21)[-1]
                        if btc_close > btc_ema21:
                            log.info(
                                "Market Breadth Guard (1h): Blocked %s short entry (%d active shorts & BTC 1h close %.1f > EMA21 %.1f at %s)",
                                pair, len(open_shorts), btc_close, btc_ema21, current_time,
                            )
                            return False

                # Kiểm tra BTC 5m (nếu BTC 5m đang hồi dốc trên EMA 21)
                btc_5m = self.dp.get_pair_dataframe(pair=btc_pair, timeframe="5m")
                if btc_5m is not None and not btc_5m.empty and "date" in btc_5m.columns:
                    btc_past_5m = btc_5m[btc_5m["date"] <= current_time]
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
