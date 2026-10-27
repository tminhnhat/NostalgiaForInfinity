# 📈 Báo Cáo Đánh Giá Hiệu Suất Backtest Toàn Diện (Comprehensive Quantitative Report)

| Thông Tin Phiên Chạy | Chi Tiết | Đánh Dấu / Định Danh |
| :--- | :--- | :--- |
| 🏷️ **Phiên bản Chiến lược (Version)** | **`v7.2`** | `v7.2` |
| 🔖 **Git Commit** | `b2b4429` | `ci: optimize daily backtest workflow with candle caching, 24 workers, skip-existing, and cache-none` |
| 🚀 **Đánh dấu lần chạy (Run Marker)** | **`v7.2-upstream163-101pairs`** | `Workflow #local` |
| 🤖 **Chiến lược (Strategy)** | `NostalgiaForInfinityX8_Combined_AI` | `Combined AI Engine` |
| 📅 **Thời gian đánh giá (Evaluation Date)** | `2026-10-27 16:02:39 UTC` | `UTC` |
| ⏱️ **Cửa sổ Backtest (Timerange)** | `20260430-20261027` | `178 ngày` |
| 📁 **Tệp kết quả (Source File)** | `backtest-result-2026-10-27_23-02-02.zip` | `Binance Futures 5m` |

---

## ⚖️ So Sánh Hiệu Suất Với Lần Backtest Trước (Benchmark Comparison)

| Chỉ số định lượng | Lần chạy này [v7.2-upstream163-101pairs - b2b4429] | Lần trước [v7.2-upstream163-101pairs - c52d557] | Chênh lệch (Δ Delta) | Xu hướng |
| :--- | :--- | :--- | :--- | :--- |
| **Tỷ lệ thắng (Winrate)** | **85.02%** | **97.08%** | `-12.06%` | 🔴 Suy giảm |
| **Lợi nhuận ròng (Net Profit %)** | **+881.20%** | **+522.21%** | `+358.99%` | 🟢 Cải thiện |
| **Lợi nhuận tuyệt đối (USDT)** | **+1,762.39 USDT** | **+1,044.41 USDT** | `+717.98 USDT` | 🟢 Cải thiện |
| **Hệ số Sharpe (Sharpe Ratio)** | **14.39** | **11.59** | `+2.80` | 🟢 Cải thiện |
| **Hệ số Sortino (Sortino Ratio)** | **18.52** | **47.34** | `-28.82` | 🔴 Suy giảm |
| **Sụt giảm tối đa (Max Drawdown %)** | **6.56%** | **2.03%** | `+4.52%` | 🔴 Suy giảm |
| **Hệ số lãi/lỗ (Profit Factor)** | **2.98** | **39.95** | `-36.96` | 🔴 Suy giảm |
| **Tổng số lệnh (Total Trades)** | **434** | **137** | `+297.00 lệnh` | 🟢 Cải thiện |
| **Chuỗi lệnh thua dài nhất** | **4 trades** | **1 trades** | `+3.00 lệnh` | 🔴 Suy giảm |
| **Kỳ vọng toán học (Expectancy)** | **4.0608** | **7.6234** | `-3.56` | 🔴 Suy giảm |
| **Hệ số Calmar (Calmar Ratio)** | **1442.44** | **2789.50** | `-1,347.07` | 🔴 Suy giảm |

---

## 🏛️ Ma Trận Lịch Sử Đối Soát Giữa Các Lần Chạy (Multi-Run Version History Matrix)

> *Bảng tổng hợp đối chiếu kết quả backtest qua từng phiên bản và lần chạy để tiện theo dõi tiến trình tối ưu hóa.*

| Đánh dấu lần chạy (Run Marker) | Phiên bản | Commit | Ngày chạy | Tỷ lệ thắng (Winrate) | Lợi nhuận ròng | Max DD % | Sharpe | Profit Factor | Tổng lệnh | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `20261027` | **`v7.0`** | `-` | 20261027 | **92.75%** | +916.30 USDT (+458.2%) | 3.52% | 11.06 | 20.11 | `138` | ⚪ Đã lưu |
| `20261027` | **`v7.0`** | `-` | 20261027 | **89.93%** | +838.73 USDT (+419.4%) | 2.97% | 10.43 | 15.48 | `139` | ⚪ Đã lưu |
| `20261027` | **`v7.0`** | `-` | 20261027 | **76.01%** | +1,056.87 USDT (+528.4%) | 23.23% | 13.55 | 1.74 | `717` | ⚪ Đã lưu |
| `v7.0-baseline` | **`v7.0`** | `1911385` | 20261027 | **95.59%** | +988.89 USDT (+494.4%) | 2.03% | 11.24 | 26.38 | `136` | ⚪ Đã lưu |
| `v7.1-relief-rejection` | **`v7.1`** | `56b0067` | 20261027 | **97.06%** | +1,037.73 USDT (+518.9%) | 2.03% | 11.55 | 39.79 | `136` | ⚪ Đã lưu |
| `20261027` | **`v7.0`** | `-` | 20261027 | **97.08%** | +1,044.41 USDT (+522.2%) | 2.03% | 11.59 | 39.95 | `137` | ⚪ Đã lưu |
| `v7.2-new-short-tags` | **`v7.2`** | `12c4e69` | 20261027 | **97.08%** | +1,044.41 USDT (+522.2%) | 2.03% | 11.59 | 39.95 | `137` | ⚪ Đã lưu |
| `v7.2-upstream163-101pairs` | **`v7.2`** | `b2b4429` | 20261027 | **85.02%** | +1,762.39 USDT (+881.2%) | 6.56% | 14.39 | 2.98 | `434` | 🎯 **HIỆN TẠI** |

---

## 🎯 Chỉ Số Hiệu Suất Cốt Lõi (Executive Performance Metrics)

| Chỉ số định lượng | Giá trị thực tế | Đánh giá Benchmark | Tiêu chuẩn chất lượng |
| :--- | :--- | :--- | :--- |
| **Tỷ lệ thắng (Winrate)** | **85.02%** | 🟢 Robust | Ngưỡng an toàn >= 70% |
| **Hệ số Sharpe (Sharpe Ratio)** | **14.39** | 🟢 Exceptional | Chuẩn Alpha quỹ >= 2.0 |
| **Hệ số Sortino (Sortino Ratio)** | **18.52** | 🟢 Excellent | Đo lường rủi ro sụt giảm âm |
| **Sụt giảm tài khoản tối đa (Max Drawdown %)** | **6.56%** | 🟢 Defended | Giới hạn rủi ro < 15% |
| **Sụt giảm tuyệt đối (Max Drawdown Abs)** | **+130.55 USDT** | 🟢 Đã kiểm soát | Độ sâu drawdown danh mục |
| **Hệ số lãi/lỗ (Profit Factor)** | **2.98** | 🟢 High | Chuẩn định lượng >= 1.5 |
| **Chuỗi thua dài nhất (Longest Loss Streak)** | **4 trades** | 🟡 Elevated | Kiểm soát chuỗi sụt giảm |

---

## 📊 Chỉ Số Định Lượng Mở Rộng (Secondary Quantitative Indicators)

| Chỉ số định lượng | Kết quả | Mô tả & Ý nghĩa kỹ thuật |
| :--- | :--- | :--- |
| **Tổng số lệnh (Total Trades)** | `434` | Tổng số lệnh đã hoàn tất trong timerange |
| **Tổng lệnh thắng / hòa / thua** | `369` thắng / `0` hòa / `65` thua | Phân bổ kết quả các giao dịch |
| **Lợi nhuận ròng % (Net Profit %)** | `+881.20%` | Tỷ lệ tăng trưởng toàn bộ tài khoản |
| **Lợi nhuận tuyệt đối (Net Profit Abs)** | `+1,762.39 USDT` | Lợi nhuận bằng tiền mặt (USDT) |
| **Lợi nhuận trung bình / lệnh** | `+4.06 USDT` | Hiệu quả trung bình mỗi lần vào lệnh |
| **Mật độ giao dịch (Trades Per Day)** | `2.44 lệnh / ngày` | Tần suất giao dịch bình quân |
| **Kỳ vọng toán học (Expectancy)** | `4.0608` | Lợi nhuận kỳ vọng trên mỗi 1 đơn vị rủi ro |
| **Hệ số Calmar (Calmar Ratio)** | `1442.44` | Tỷ lệ lợi nhuận trên sụt giảm vốn tối đa |
| **Tốc độ tăng trưởng kép (CAGR)** | `10705.81%` | Compound Annual Growth Rate quy năm |

---

## ⚔️ Thống Kê Phân Bổ Vị Thế (Long vs Short Performance)

| Vị thế (Position) | Số lệnh | Tỷ trọng | Tỷ lệ thắng (Winrate) | Lợi nhuận (USDT) | Lợi nhuận (%) | Đánh giá |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 **Lệnh Mua (Long)** | `166` | 38.2% | **99.40%** | **+1,845.59 USDT** | +2506.26% | 🟢 Vượt trội |
| 🔴 **Lệnh Bán (Short)** | `268` | 61.8% | **76.12%** | **-83.20 USDT** | +28.09% | 🟡 Tốt |
| 🌐 **Toàn bộ danh mục** | `434` | 100.0% | **85.02%** | **+1,762.39 USDT** | +881.20% | 🎯 Hoàn tất |

## 🚪 Phân Tích Lý Do Thoát Lệnh (Exit Reason Breakdown)

| Lý do đóng lệnh (Exit Reason) | Số lệnh | Tỷ trọng | Tỷ lệ thắng (Winrate) | Lợi nhuận (USDT) |
| :--- | :--- | :--- | :--- | :--- |
| `TOTAL` | `434` | 100.0% | **85.0%** | +1,762.39 USDT |
| `exit_ai_reversal_harvest ( 741_AI_PASS)` | `92` | 21.2% | **100.0%** | +339.12 USDT |
| `exit_ai_early_structural_cut ( 741_AI_PASS)` | `37` | 8.5% | **0.0%** | -482.05 USDT |
| `exit_ai_reversal_harvest ( 725 741_AI_PASS)` | `25` | 5.8% | **100.0%** | +104.76 USDT |
| `exit_profit_long_rebuy_t_0_1_m ( 64 )` | `14` | 3.2% | **100.0%** | +45.71 USDT |
| `exit_ai_profit_lock ( 741_AI_PASS)` | `12` | 2.8% | **100.0%** | +16.07 USDT |
| `exit_ai_reversal_harvest ( 702 703 731_AI_PASS)` | `11` | 2.5% | **100.0%** | +21.23 USDT |
| `exit_ai_reversal_harvest ( 711 725 741_AI_PASS)` | `10` | 2.3% | **100.0%** | +38.09 USDT |
| `exit_short_adaptive_trailing_scalp ( 562 )` | `9` | 2.1% | **100.0%** | +87.80 USDT |
| `exit_ai_profit_lock ( 725 741_AI_PASS)` | `7` | 1.6% | **100.0%** | +10.30 USDT |
| `exit_profit_long_tc_t_0_1_m ( 142 )` | `7` | 1.6% | **100.0%** | +7.53 USDT |
| `exit_ai_early_structural_cut ( 725 741_AI_PASS)` | `7` | 1.6% | **0.0%** | -99.76 USDT |
| `exit_long_rebuy_d_6_1 ( 64 )` | `5` | 1.2% | **100.0%** | +195.26 USDT |
| `exit_ai_early_structural_cut ( 711 725 741_AI_PASS)` | `5` | 1.2% | **0.0%** | -100.51 USDT |
| `exit_long_rebuy_e_r ( 65 )` | `4` | 0.9% | **100.0%** | +33.33 USDT |
| `exit_ai_reversal_harvest ( 702 703 731 743_AI_PASS)` | `4` | 0.9% | **100.0%** | +12.41 USDT |
| `exit_profit_long_tc_t_0_1_m ( 143 )` | `4` | 0.9% | **100.0%** | +7.19 USDT |
| `exit_profit_long_tc_t_0_1_m ( 144 )` | `4` | 0.9% | **100.0%** | +6.84 USDT |
| `exit_long_quick_q_9 ( 44 )` | `3` | 0.7% | **100.0%** | +55.26 USDT |
| `exit_short_adaptive_trailing_scalp ( 542 )` | `3` | 0.7% | **100.0%** | +24.11 USDT |
| `exit_profit_long_tc_t_1_1_m ( 145 )` | `3` | 0.7% | **100.0%** | +16.59 USDT |
| `exit_long_normal_u_1 ( 2 )` | `3` | 0.7% | **100.0%** | +12.95 USDT |
| `exit_profit_long_tc_t_0_1_m ( 145 )` | `3` | 0.7% | **100.0%** | +8.22 USDT |
| `exit_ai_profit_lock ( 711 725 741_AI_PASS)` | `3` | 0.7% | **100.0%** | +5.09 USDT |
| `exit_profit_long_rebuy_t_0_1_m ( 62 )` | `3` | 0.7% | **100.0%** | +3.90 USDT |
| `exit_profit_short_rebuy_t_0_1_m ( 562 )` | `3` | 0.7% | **100.0%** | +3.11 USDT |
| `exit_ai_drift_decay ( 741_AI_PASS)` | `3` | 0.7% | **0.0%** | -14.58 USDT |
| `exit_long_rebuy_d_7_1 ( 64 )` | `2` | 0.5% | **100.0%** | +126.16 USDT |
| `exit_long_normal_d_4_1 ( 2 )` | `2` | 0.5% | **100.0%** | +79.47 USDT |
| `exit_long_normal_d_7_1 ( 2 )` | `2` | 0.5% | **100.0%** | +60.27 USDT |
| `exit_long_rebuy_d_4_1 ( 65 )` | `2` | 0.5% | **100.0%** | +46.12 USDT |
| `exit_long_quick_q_6 ( 42 )` | `2` | 0.5% | **100.0%** | +45.78 USDT |
| `exit_long_rebuy_d_4_1 ( 64 )` | `2` | 0.5% | **100.0%** | +30.41 USDT |
| `exit_short_rebuy_1_1_1 ( 562 )` | `2` | 0.5% | **100.0%** | +27.45 USDT |
| `exit_long_normal_d_6_1 ( 2 )` | `2` | 0.5% | **100.0%** | +24.51 USDT |
| `exit_long_rapid_rpd_2 ( 102 )` | `2` | 0.5% | **100.0%** | +16.06 USDT |
| `exit_long_tc_u_1 ( 141 )` | `2` | 0.5% | **100.0%** | +14.99 USDT |
| `exit_profit_long_tc_t_2_1_m ( 142 )` | `2` | 0.5% | **100.0%** | +13.21 USDT |
| `exit_long_tc_d_5_1 ( 141 142 )` | `2` | 0.5% | **100.0%** | +9.83 USDT |
| `exit_long_tc_d_5_1 ( 142 )` | `2` | 0.5% | **100.0%** | +9.76 USDT |
| `exit_profit_long_scalp_t_1_1_m ( 163 )` | `2` | 0.5% | **100.0%** | +8.87 USDT |
| `exit_short_rebuy_u_1 ( 562 )` | `2` | 0.5% | **100.0%** | +6.75 USDT |
| `exit_profit_long_tc_t_0_1_m ( 141 )` | `2` | 0.5% | **100.0%** | +3.85 USDT |
| `exit_profit_long_rebuy_t_0_1_m ( 61 )` | `2` | 0.5% | **100.0%** | +3.19 USDT |
| `exit_ai_profit_lock ( 702 703 731_AI_PASS)` | `2` | 0.5% | **100.0%** | +3.14 USDT |
| `exit_profit_long_scalp_t_0_1_m ( 163 )` | `2` | 0.5% | **100.0%** | +1.44 USDT |
| `exit_ai_drift_decay ( 725 741_AI_PASS)` | `2` | 0.5% | **0.0%** | -3.34 USDT |
| `exit_short_universal_structural_cut ( 562 )` | `2` | 0.5% | **0.0%** | -21.46 USDT |
| `exit_ai_early_structural_cut ( 724 741_AI_PASS)` | `2` | 0.5% | **0.0%** | -37.59 USDT |
| `exit_short_universal_structural_cut ( 741_AI_PASS)` | `2` | 0.5% | **0.0%** | -41.54 USDT |
| `exit_long_rebuy_d_6_1 ( 62 )` | `1` | 0.2% | **100.0%** | +67.29 USDT |
| `exit_long_rebuy_2_1_1 ( 64 )` | `1` | 0.2% | **100.0%** | +65.09 USDT |
| `exit_long_quick_d_11_1 ( 43 )` | `1` | 0.2% | **100.0%** | +62.80 USDT |
| `exit_long_normal_d_6_1 ( 1 )` | `1` | 0.2% | **100.0%** | +42.47 USDT |
| `exit_long_rebuy_d_8_1 ( 64 )` | `1` | 0.2% | **100.0%** | +37.09 USDT |
| `exit_long_rebuy_w_6_1 ( 64 )` | `1` | 0.2% | **100.0%** | +34.41 USDT |
| `exit_long_normal_d_4_1 ( 6 )` | `1` | 0.2% | **100.0%** | +33.04 USDT |
| `exit_long_normal_d_7_1 ( 6 )` | `1` | 0.2% | **100.0%** | +31.94 USDT |
| `exit_long_tc_d_8_1 ( 142 )` | `1` | 0.2% | **100.0%** | +30.34 USDT |
| `exit_long_tc_d_3_1 ( 141 )` | `1` | 0.2% | **100.0%** | +28.54 USDT |
| `exit_long_tc_d_5_1 ( 141 )` | `1` | 0.2% | **100.0%** | +27.42 USDT |
| `exit_short_adaptive_trailing_mega ( 562 )` | `1` | 0.2% | **100.0%** | +24.74 USDT |
| `exit_long_scalp_d_5_1 ( 163 )` | `1` | 0.2% | **100.0%** | +24.45 USDT |
| `exit_long_normal_u_3 ( 6 141 )` | `1` | 0.2% | **100.0%** | +22.99 USDT |
| `exit_long_tc_3_1_1 ( 141 142 )` | `1` | 0.2% | **100.0%** | +22.37 USDT |
| `exit_long_rebuy_d_9_1 ( 65 )` | `1` | 0.2% | **100.0%** | +21.71 USDT |
| `exit_long_tc_d_6_1 ( 144 )` | `1` | 0.2% | **100.0%** | +17.86 USDT |
| `exit_profit_long_rebuy_t_7_1_m ( 63 )` | `1` | 0.2% | **100.0%** | +17.79 USDT |
| `exit_short_adaptive_trailing_scalp ( 711 725 741_AI_PASS)` | `1` | 0.2% | **100.0%** | +15.58 USDT |
| `exit_long_scalp_d_6_1 ( 61 162 )` | `1` | 0.2% | **100.0%** | +14.88 USDT |
| `exit_long_rebuy_d_6_1 ( 63 )` | `1` | 0.2% | **100.0%** | +14.46 USDT |
| `exit_long_rebuy_d_6_1 ( 61 )` | `1` | 0.2% | **100.0%** | +13.59 USDT |
| `exit_long_quick_q_6 ( 47 )` | `1` | 0.2% | **100.0%** | +13.59 USDT |
| `exit_long_rebuy_d_8_1 ( 61 )` | `1` | 0.2% | **100.0%** | +13.49 USDT |
| `exit_long_scalp_d_6_1 ( 162 )` | `1` | 0.2% | **100.0%** | +13.09 USDT |
| `exit_profit_long_tc_t_2_1_m ( 145 )` | `1` | 0.2% | **100.0%** | +12.92 USDT |
| `exit_long_tc_d_5_1 ( 145 )` | `1` | 0.2% | **100.0%** | +12.39 USDT |
| `exit_profit_long_normal_t_2_1_m ( 3 )` | `1` | 0.2% | **100.0%** | +11.62 USDT |
| `exit_ai_reversal_harvest ( 702 703 705 731_AI_PASS)` | `1` | 0.2% | **100.0%** | +11.62 USDT |
| `exit_long_quick_d_7_1 ( 42 )` | `1` | 0.2% | **100.0%** | +11.26 USDT |
| `exit_profit_long_quick_t_2_1_m ( 46 )` | `1` | 0.2% | **100.0%** | +11.17 USDT |
| `exit_long_tc_u_1 ( 141 142 )` | `1` | 0.2% | **100.0%** | +10.89 USDT |
| `exit_long_tc_u_1 ( 142 )` | `1` | 0.2% | **100.0%** | +10.54 USDT |
| `exit_long_normal_d_3_2 ( 5 )` | `1` | 0.2% | **100.0%** | +10.54 USDT |
| `exit_profit_short_rebuy_t_1_1_m ( 562 )` | `1` | 0.2% | **100.0%** | +10.47 USDT |
| `exit_long_rebuy_d_5_1 ( 63 )` | `1` | 0.2% | **100.0%** | +9.79 USDT |
| `exit_long_tc_d_6_1 ( 141 )` | `1` | 0.2% | **100.0%** | +9.29 USDT |
| `exit_long_normal_u_1 ( 1 )` | `1` | 0.2% | **100.0%** | +8.92 USDT |
| `exit_long_tc_d_6_1 ( 141 143 163 )` | `1` | 0.2% | **100.0%** | +8.14 USDT |
| `exit_profit_long_normal_t_1_1_m ( 3 )` | `1` | 0.2% | **100.0%** | +7.68 USDT |
| `exit_profit_long_tc_t_1_1_m ( 141 )` | `1` | 0.2% | **100.0%** | +7.56 USDT |
| `exit_profit_long_rebuy_t_3_1_m ( 61 )` | `1` | 0.2% | **100.0%** | +7.51 USDT |
| `exit_profit_long_tc_t_1_1_m ( 141 142 )` | `1` | 0.2% | **100.0%** | +7.43 USDT |
| `exit_long_tc_d_4_2 ( 145 )` | `1` | 0.2% | **100.0%** | +7.37 USDT |
| `exit_long_normal_u_4 ( 1 61 )` | `1` | 0.2% | **100.0%** | +6.84 USDT |
| `exit_long_tc_d_5_1 ( 62 144 )` | `1` | 0.2% | **100.0%** | +6.72 USDT |
| `exit_long_normal_d_8_1 ( 4 )` | `1` | 0.2% | **100.0%** | +6.66 USDT |
| `exit_long_normal_d_3_1 ( 1 )` | `1` | 0.2% | **100.0%** | +6.65 USDT |
| `exit_profit_long_rebuy_t_2_1_m ( 65 )` | `1` | 0.2% | **100.0%** | +6.51 USDT |
| `exit_ai_reversal_harvest ( 703 721 741_AI_PASS)` | `1` | 0.2% | **100.0%** | +6.37 USDT |
| `exit_long_normal_d_7_1 ( 2 101 141 )` | `1` | 0.2% | **100.0%** | +6.35 USDT |
| `exit_long_normal_d_5_1 ( 2 )` | `1` | 0.2% | **100.0%** | +6.01 USDT |
| `exit_long_tc_d_5_1 ( 144 )` | `1` | 0.2% | **100.0%** | +5.51 USDT |
| `exit_profit_long_normal_t_0_1_m ( 2 )` | `1` | 0.2% | **100.0%** | +5.14 USDT |
| `exit_long_normal_d_5_1 ( 6 102 141 )` | `1` | 0.2% | **100.0%** | +5.13 USDT |
| `exit_long_tc_d_3_2 ( 102 142 )` | `1` | 0.2% | **100.0%** | +5.07 USDT |
| `exit_long_normal_d_5_1 ( 5 )` | `1` | 0.2% | **100.0%** | +4.86 USDT |
| `exit_long_normal_d_6_1 ( 2 141 )` | `1` | 0.2% | **100.0%** | +4.52 USDT |
| `exit_long_quick_q_2 ( 41 )` | `1` | 0.2% | **100.0%** | +4.52 USDT |
| `exit_profit_long_rapid_t_1_1_m ( 102 )` | `1` | 0.2% | **100.0%** | +4.51 USDT |
| `exit_profit_long_tc_t_0_1_m ( 141 142 )` | `1` | 0.2% | **100.0%** | +4.34 USDT |
| `exit_ai_reversal_harvest ( 724 741_AI_PASS)` | `1` | 0.2% | **100.0%** | +4.06 USDT |
| `exit_long_normal_u_2 ( 4 41 61 )` | `1` | 0.2% | **100.0%** | +3.83 USDT |
| `exit_long_rapid_rpd_6 ( 102 )` | `1` | 0.2% | **100.0%** | +3.74 USDT |
| `exit_profit_long_tc_t_3_1_m ( 143 )` | `1` | 0.2% | **100.0%** | +3.69 USDT |
| `exit_profit_long_rebuy_t_1_1_m ( 62 )` | `1` | 0.2% | **100.0%** | +3.65 USDT |
| `exit_profit_long_rebuy_t_2_1_m ( 62 )` | `1` | 0.2% | **100.0%** | +3.39 USDT |
| `exit_ai_reversal_harvest ( 742_AI_PASS)` | `1` | 0.2% | **100.0%** | +3.21 USDT |
| `exit_ai_reversal_harvest ( 721 724 731_AI_PASS)` | `1` | 0.2% | **100.0%** | +2.62 USDT |
| `exit_profit_long_normal_t_0_1_m ( 6 102 )` | `1` | 0.2% | **100.0%** | +2.54 USDT |
| `exit_long_quick_u_1 ( 42 )` | `1` | 0.2% | **100.0%** | +2.47 USDT |
| `exit_ai_profit_lock ( 702 703 706 731 743_AI_PASS)` | `1` | 0.2% | **100.0%** | +2.41 USDT |
| `exit_ai_reversal_harvest ( 702 731 743_AI_PASS)` | `1` | 0.2% | **100.0%** | +2.38 USDT |
| `exit_ai_reversal_harvest ( 703 721 731_AI_PASS)` | `1` | 0.2% | **100.0%** | +2.28 USDT |
| `exit_long_normal_u_2 ( 2 )` | `1` | 0.2% | **100.0%** | +2.27 USDT |
| `exit_ai_reversal_harvest ( 711 741_AI_PASS)` | `1` | 0.2% | **100.0%** | +2.16 USDT |
| `exit_long_quick_u_1 ( 43 )` | `1` | 0.2% | **100.0%** | +1.80 USDT |
| `exit_profit_long_scalp_t_2_1_m ( 163 )` | `1` | 0.2% | **100.0%** | +1.77 USDT |
| `exit_short_adaptive_trailing_scalp ( 702 703 731_AI_PASS)` | `1` | 0.2% | **100.0%** | +1.72 USDT |
| `exit_profit_long_rebuy_t_2_1_m ( 64 )` | `1` | 0.2% | **100.0%** | +1.70 USDT |
| `exit_profit_long_normal_t_0_1_m ( 6 )` | `1` | 0.2% | **100.0%** | +1.67 USDT |
| `exit_ai_reversal_harvest ( 721 724 741_AI_PASS)` | `1` | 0.2% | **100.0%** | +1.63 USDT |
| `exit_profit_long_normal_t_2_1_m ( 2 63 101 )` | `1` | 0.2% | **100.0%** | +1.62 USDT |
| `exit_profit_long_scalp_t_0_1_m ( 161 )` | `1` | 0.2% | **100.0%** | +1.54 USDT |
| `exit_long_tc_u_1 ( 144 )` | `1` | 0.2% | **100.0%** | +1.47 USDT |
| `exit_profit_long_normal_t_0_1_m ( 3 )` | `1` | 0.2% | **100.0%** | +1.36 USDT |
| `exit_ai_reversal_harvest ( 701 702 703 731 743_AI_PASS)` | `1` | 0.2% | **100.0%** | +1.23 USDT |
| `exit_profit_long_quick_t_1_1_m ( 42 )` | `1` | 0.2% | **100.0%** | +1.17 USDT |
| `exit_profit_long_rapid_t_0_1_m ( 102 )` | `1` | 0.2% | **100.0%** | +1.12 USDT |
| `exit_profit_long_scalp_t_0_1_m ( 162 )` | `1` | 0.2% | **100.0%** | +0.93 USDT |
| `exit_long_normal_w_0_1 ( 1 )` | `1` | 0.2% | **100.0%** | +0.92 USDT |
| `exit_profit_long_quick_t_0_1_m ( 43 )` | `1` | 0.2% | **100.0%** | +0.84 USDT |
| `exit_ai_profit_lock ( 721 741_AI_PASS)` | `1` | 0.2% | **100.0%** | +0.83 USDT |
| `exit_ai_profit_lock ( 703 721 741_AI_PASS)` | `1` | 0.2% | **100.0%** | +0.52 USDT |
| `exit_ai_profit_lock ( 703 705 706 731_AI_PASS)` | `1` | 0.2% | **100.0%** | +0.43 USDT |
| `exit_ai_profit_lock ( 724 741_AI_PASS)` | `1` | 0.2% | **100.0%** | +0.41 USDT |
| `exit_long_normal_w_0_1 ( 3 )` | `1` | 0.2% | **100.0%** | +0.37 USDT |
| `exit_profit_long_normal_t_0_1_m ( 5 )` | `1` | 0.2% | **100.0%** | +0.36 USDT |
| `exit_profit_long_normal_t_0_1_m ( 3 142 )` | `1` | 0.2% | **100.0%** | +0.18 USDT |
| `exit_ai_562_aged_breakeven ( 562 )` | `1` | 0.2% | **0.0%** | -4.32 USDT |
| `exit_bad_trade_abandon_18d ( 120 )` | `1` | 0.2% | **0.0%** | -10.57 USDT |
| `exit_ai_drift_decay ( 711 725 741_AI_PASS)` | `1` | 0.2% | **0.0%** | -11.07 USDT |
| `exit_short_universal_structural_cut ( 542 )` | `1` | 0.2% | **0.0%** | -16.34 USDT |
| `exit_short_universal_structural_cut ( 725 741_AI_PASS)` | `1` | 0.2% | **0.0%** | -44.73 USDT |

## 🔍 Bảng Phân Tích Đầy Đủ Tất Cả Các Entry Tags (Full Enter Tag Breakdown)

> *Bảng tổng hợp chi tiết 100% tất cả các tag tín hiệu vào lệnh (Entry Tags) đã hoạt động trong phiên backtest.*

| Enter Tag | Vị thế | Số lệnh | Tỷ lệ thắng (Winrate) | Thắng/Hòa/Thua | Tổng LN % | Tổng LN (USDT) | LN TB/Lệnh | Thời lượng TB | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `TOTAL` | 🟢 Long Core | `434` | **85.0%** | 369/0/65 | +881.20% | **+1,762.39 USDT** | +5.84% | 9:55:00 | 🟢 Tối ưu |
| `64` | 🟢 Long Core | `27` | **100.0%** | 27/0/0 | +267.91% | **+535.82 USDT** | +18.22% | 10:41:00 | 🟢 Tối ưu |
| `2` | 🟢 Long Core | `12` | **100.0%** | 12/0/0 | +95.31% | **+190.62 USDT** | +20.29% | 2:08:00 | 🟢 Tối ưu |
| `562` | 🟢 Long Core | `21` | **85.7%** | 18/0/3 | +67.27% | **+134.54 USDT** | +5.75% | 1 day, 6:33:00 | 🟢 Tối ưu |
| `65` | 🟢 Long Core | `8` | **100.0%** | 8/0/0 | +53.84% | **+107.68 USDT** | +19.27% | 2:26:00 | 🟢 Tối ưu |
| `141` | 🟢 Long Core | `8` | **100.0%** | 8/0/0 | +45.83% | **+91.65 USDT** | +12.45% | 9:52:00 | 🟢 Tối ưu |
| `62` | 🟢 Long Core | `6` | **100.0%** | 6/0/0 | +39.12% | **+78.24 USDT** | +8.45% | 14:27:00 | 🟢 Tối ưu |
| `142` | 🟢 Long Core | `13` | **100.0%** | 13/0/0 | +35.69% | **+71.38 USDT** | +10.31% | 8:34:00 | 🟢 Tối ưu |
| `6` | 🟢 Long Core | `3` | **100.0%** | 3/0/0 | +33.32% | **+66.65 USDT** | +18.75% | 17:13:00 | 🟢 Tối ưu |
| `43` | 🟢 Long Core | `3` | **100.0%** | 3/0/0 | +32.72% | **+65.44 USDT** | +26.00% | 0:35:00 | 🟢 Tối ưu |
| `42` | 🟢 Long Core | `5` | **100.0%** | 5/0/0 | +30.34% | **+60.68 USDT** | +15.41% | 2 days, 5:12:00 | 🟢 Tối ưu |
| `1` | 🟢 Long Core | `4` | **100.0%** | 4/0/0 | +29.48% | **+58.96 USDT** | +11.14% | 1 day, 20:39:00 | 🟢 Tối ưu |
| `145` | 🟢 Long Core | `9` | **100.0%** | 9/0/0 | +28.75% | **+57.50 USDT** | +10.61% | 8:46:00 | 🟢 Tối ưu |
| `44` | 🟢 Long Core | `3` | **100.0%** | 3/0/0 | +27.63% | **+55.26 USDT** | +22.49% | 2:32:00 | 🟢 Tối ưu |
| `141 142` | 🟢 Long Core | `6` | **100.0%** | 6/0/0 | +27.43% | **+54.86 USDT** | +13.96% | 9:57:00 | 🟢 Tối ưu |
| `63` | 🟢 Long Core | `3` | **100.0%** | 3/0/0 | +21.02% | **+42.05 USDT** | +33.10% | 3:02:00 | 🟢 Tối ưu |
| `61` | 🟢 Long Core | `5` | **100.0%** | 5/0/0 | +18.89% | **+37.79 USDT** | +20.53% | 2:10:00 | 🟢 Tối ưu |
| `163` | 🟢 Long Core | `6` | **100.0%** | 6/0/0 | +18.26% | **+36.52 USDT** | +9.34% | 2:25:00 | 🟢 Tối ưu |
| `144` | 🟢 Long Core | `7` | **100.0%** | 7/0/0 | +15.84% | **+31.68 USDT** | +11.45% | 12:38:00 | 🟢 Tối ưu |
| `702 703 731_AI_PASS` | 🤖 Short AI Gatekeeper | `14` | **100.0%** | 14/0/0 | +13.04% | **+26.08 USDT** | +5.51% | 4:54:00 | 🟢 Tối ưu |
| `102` | 🟢 Long Core | `5` | **100.0%** | 5/0/0 | +12.71% | **+25.43 USDT** | +5.25% | 2:58:00 | 🟢 Tối ưu |
| `6 141` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +11.50% | **+22.99 USDT** | +16.21% | 19:20:00 | 🟢 Tối ưu |
| `3` | 🟢 Long Core | `4` | **100.0%** | 4/0/0 | +10.52% | **+21.04 USDT** | +5.12% | 19:42:00 | 🟢 Tối ưu |
| `5` | 🟢 Long Core | `3` | **100.0%** | 3/0/0 | +7.88% | **+15.76 USDT** | +14.52% | 3:03:00 | 🟢 Tối ưu |
| `61 162` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +7.44% | **+14.88 USDT** | +32.22% | 4:05:00 | 🟢 Tối ưu |
| `162` | 🟢 Long Core | `2` | **100.0%** | 2/0/0 | +7.01% | **+14.03 USDT** | +17.33% | 0:52:00 | 🟢 Tối ưu |
| `47` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +6.79% | **+13.59 USDT** | +13.38% | 1 day, 2:00:00 | 🟢 Tối ưu |
| `702 703 731 743_AI_PASS` | 🤖 Short AI Gatekeeper | `4` | **100.0%** | 4/0/0 | +6.21% | **+12.41 USDT** | +5.77% | 2:32:00 | 🟢 Tối ưu |
| `702 703 705 731_AI_PASS` | 🤖 Short AI Gatekeeper | `1` | **100.0%** | 1/0/0 | +5.81% | **+11.62 USDT** | +6.15% | 7:45:00 | 🟢 Tối ưu |
| `46` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +5.58% | **+11.17 USDT** | +11.97% | 0:45:00 | 🟢 Tối ưu |
| `143` | 🟢 Long Core | `5` | **100.0%** | 5/0/0 | +5.44% | **+10.88 USDT** | +5.30% | 18:36:00 | 🟢 Tối ưu |
| `141 143 163` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +4.07% | **+8.14 USDT** | +33.41% | 1:30:00 | 🟢 Tối ưu |
| `542` | 🟢 Long Core | `4` | **75.0%** | 3/0/1 | +3.89% | **+7.78 USDT** | +1.59% | 1:24:00 | 🟡 Hiệu quả |
| `703 721 741_AI_PASS` | 🤖 Short AI Gatekeeper | `2` | **100.0%** | 2/0/0 | +3.44% | **+6.88 USDT** | +4.93% | 2:32:00 | 🟢 Tối ưu |
| `1 61` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +3.42% | **+6.84 USDT** | +21.38% | 0:15:00 | 🟢 Tối ưu |
| `62 144` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +3.36% | **+6.72 USDT** | +25.85% | 1:25:00 | 🟢 Tối ưu |
| `4` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +3.33% | **+6.66 USDT** | +44.22% | 1:10:00 | 🟢 Tối ưu |
| `2 101 141` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +3.17% | **+6.35 USDT** | +36.21% | 1:00:00 | 🟢 Tối ưu |
| `6 102 141` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +2.56% | **+5.13 USDT** | +26.17% | 1:00:00 | 🟢 Tối ưu |
| `102 142` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +2.53% | **+5.07 USDT** | +19.97% | 1:40:00 | 🟢 Tối ưu |
| `2 141` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +2.26% | **+4.52 USDT** | +30.19% | 2:15:00 | 🟢 Tối ưu |
| `41` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +2.26% | **+4.52 USDT** | +11.69% | 5:00:00 | 🟢 Tối ưu |
| `4 41 61` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +1.91% | **+3.83 USDT** | +11.78% | 0:10:00 | 🟢 Tối ưu |
| `742_AI_PASS` | 🤖 Short AI Gatekeeper | `1` | **100.0%** | 1/0/0 | +1.61% | **+3.21 USDT** | +5.81% | 0:40:00 | 🟢 Tối ưu |
| `721 724 731_AI_PASS` | 🤖 Short AI Gatekeeper | `1` | **100.0%** | 1/0/0 | +1.31% | **+2.62 USDT** | +6.65% | 17:10:00 | 🟢 Tối ưu |
| `6 102` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +1.27% | **+2.54 USDT** | +1.43% | 2:05:00 | 🟢 Tối ưu |
| `702 703 706 731 743_AI_PASS` | 🤖 Short AI Gatekeeper | `1` | **100.0%** | 1/0/0 | +1.20% | **+2.41 USDT** | +1.60% | 0:45:00 | 🟢 Tối ưu |
| `702 731 743_AI_PASS` | 🤖 Short AI Gatekeeper | `1` | **100.0%** | 1/0/0 | +1.19% | **+2.38 USDT** | +6.75% | 9:05:00 | 🟢 Tối ưu |
| `703 721 731_AI_PASS` | 🤖 Short AI Gatekeeper | `1` | **100.0%** | 1/0/0 | +1.14% | **+2.28 USDT** | +5.07% | 5:00:00 | 🟢 Tối ưu |
| `711 741_AI_PASS` | 🤖 Short AI Gatekeeper | `1` | **100.0%** | 1/0/0 | +1.08% | **+2.16 USDT** | +5.45% | 5:05:00 | 🟢 Tối ưu |
| `721 724 741_AI_PASS` | 🤖 Short AI Gatekeeper | `1` | **100.0%** | 1/0/0 | +0.82% | **+1.63 USDT** | +5.13% | 4:00:00 | 🟢 Tối ưu |
| `2 63 101` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +0.81% | **+1.62 USDT** | +10.72% | 2:55:00 | 🟢 Tối ưu |
| `161` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +0.77% | **+1.54 USDT** | +2.73% | 12:05:00 | 🟢 Tối ưu |
| `701 702 703 731 743_AI_PASS` | 🤖 Short AI Gatekeeper | `1` | **100.0%** | 1/0/0 | +0.61% | **+1.23 USDT** | +4.83% | 7:35:00 | 🟢 Tối ưu |
| `721 741_AI_PASS` | 🤖 Short AI Gatekeeper | `1` | **100.0%** | 1/0/0 | +0.42% | **+0.83 USDT** | +1.74% | 7:50:00 | 🟢 Tối ưu |
| `703 705 706 731_AI_PASS` | 🤖 Short AI Gatekeeper | `1` | **100.0%** | 1/0/0 | +0.22% | **+0.43 USDT** | +1.92% | 6:05:00 | 🟢 Tối ưu |
| `3 142` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +0.09% | **+0.18 USDT** | +0.63% | 19:15:00 | 🟢 Tối ưu |
| `120` | 🟢 Long Core | `1` | **0.0%** | 0/0/1 | -5.28% | **-10.57 USDT** | -10.12% | 17 days, 22:40:00 | 🔴 Cần tinh chỉnh |
| `725 741_AI_PASS` | 🤖 Short AI Gatekeeper | `42` | **76.2%** | 32/0/10 | -16.38% | **-32.76 USDT** | +0.09% | 6:35:00 | 🔴 Cần tinh chỉnh |
| `724 741_AI_PASS` | 🤖 Short AI Gatekeeper | `4` | **50.0%** | 2/0/2 | -16.56% | **-33.11 USDT** | -7.66% | 3:56:00 | 🔴 Cần tinh chỉnh |
| `711 725 741_AI_PASS` | 🤖 Short AI Gatekeeper | `20` | **70.0%** | 14/0/6 | -26.42% | **-52.84 USDT** | -1.84% | 7:29:00 | 🔴 Cần tinh chỉnh |
| `741_AI_PASS` | 🤖 Short AI Gatekeeper | `146` | **71.2%** | 104/0/42 | -91.49% | **-182.98 USDT** | -1.35% | 6:30:00 | 🔴 Cần tinh chỉnh |

---

## 📑 Chi Tiết Các Lệnh Giao Dịch (Trade Execution Journal)

### 🥇 Top 10 Lệnh Lãi Cao Nhất (Top Winning Trades)
| # | Cặp giao dịch | Vị thế | Enter Tag | Thời gian Mở ➔ Đóng | Thời lượng | Lợi nhuận % | Lợi nhuận USDT | Lý do thoát |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| #1 | **BAT/USDT:USDT** | 🟢 Long | `64 ` | 2026-10-08 08:20 ➔ 2026-10-09 06:05 | 21h 45m | **+43.38%** | **+73.47 USDT** | `exit_long_rebuy_d_7_1 ( 64 )` |
| #2 | **GRASS/USDT:USDT** | 🟢 Long | `62 ` | 2026-10-14 17:45 ➔ 2026-10-15 15:05 | 21h 20m | **+33.86%** | **+67.29 USDT** | `exit_long_rebuy_d_6_1 ( 62 )` |
| #3 | **ARB/USDT:USDT** | 🟢 Long | `64 ` | 2026-09-17 21:45 ➔ 2026-09-18 01:50 | 4h 5m | **+59.20%** | **+65.09 USDT** | `exit_long_rebuy_2_1_1 ( 64 )` |
| #4 | **BTW/USDT:USDT** | 🟢 Long | `43 ` | 2026-10-05 06:45 ➔ 2026-10-05 08:05 | 1h 20m | **+71.12%** | **+62.80 USDT** | `exit_long_quick_d_11_1 ( 43 )` |
| #5 | **BTW/USDT:USDT** | 🟢 Long | `2 ` | 2026-10-23 18:30 ➔ 2026-10-23 19:10 | 40m | **+38.38%** | **+53.91 USDT** | `exit_long_normal_d_7_1 ( 2 )` |
| #6 | **WLD/USDT:USDT** | 🟢 Long | `64 ` | 2026-09-26 22:25 ➔ 2026-09-27 10:10 | 11h 45m | **+40.20%** | **+52.69 USDT** | `exit_long_rebuy_d_7_1 ( 64 )` |
| #7 | **GRASS/USDT:USDT** | 🟢 Long | `64 ` | 2026-10-05 14:55 ➔ 2026-10-05 19:15 | 4h 20m | **+32.17%** | **+49.91 USDT** | `exit_long_rebuy_d_6_1 ( 64 )` |
| #8 | **BAT/USDT:USDT** | 🟢 Long | `64 ` | 2026-10-03 06:15 ➔ 2026-10-04 07:40 | 25h 25m | **+33.11%** | **+48.10 USDT** | `exit_long_rebuy_d_6_1 ( 64 )` |
| #9 | **BTW/USDT:USDT** | 🟢 Long | `1 ` | 2026-10-22 20:45 ➔ 2026-10-22 21:40 | 55m | **+30.41%** | **+42.47 USDT** | `exit_long_normal_d_6_1 ( 1 )` |
| #10 | **QNT/USDT:USDT** | 🟢 Long | `2 ` | 2026-10-13 11:10 ➔ 2026-10-13 18:40 | 7h 30m | **+24.34%** | **+42.12 USDT** | `exit_long_normal_d_4_1 ( 2 )` |

### ⚠️ Top Lệnh Thua Lỗ / Sụt Giảm Lớn Nhất (Top Drawdown Trades)
| # | Cặp giao dịch | Vị thế | Enter Tag | Thời gian Mở ➔ Đóng | Thời lượng | Thua lỗ % | Thua lỗ USDT | Lý do thoát |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| #1 | **WLD/USDT:USDT** | 🔴 Short | `725 741_AI_PASS` | 2026-10-16 20:40 ➔ 2026-10-17 03:30 | 6h 50m | **-23.91%** | **-44.73 USDT** | `exit_short_universal_structural_cut ( 725 741_AI_PASS)` |
| #2 | **RAYSOL/USDT:USDT** | 🔴 Short | `741_AI_PASS` | 2026-10-20 01:05 ➔ 2026-10-20 14:15 | 13h 10m | **-24.05%** | **-36.84 USDT** | `exit_short_universal_structural_cut ( 741_AI_PASS)` |
| #3 | **VVV/USDT:USDT** | 🔴 Short | `741_AI_PASS` | 2026-10-26 11:45 ➔ 2026-10-26 15:00 | 3h 15m | **-18.24%** | **-35.23 USDT** | `exit_ai_early_structural_cut ( 741_AI_PASS)` |
| #4 | **ZEC/USDT:USDT** | 🔴 Short | `724 741_AI_PASS` | 2026-10-20 09:05 ➔ 2026-10-20 13:55 | 4h 50m | **-17.88%** | **-34.61 USDT** | `exit_ai_early_structural_cut ( 724 741_AI_PASS)` |
| #5 | **ZHIPU/USDT:USDT** | 🔴 Short | `741_AI_PASS` | 2026-10-26 06:00 ➔ 2026-10-26 08:35 | 2h 35m | **-17.61%** | **-34.32 USDT** | `exit_ai_early_structural_cut ( 741_AI_PASS)` |
| #6 | **QNT/USDT:USDT** | 🔴 Short | `741_AI_PASS` | 2026-10-20 10:25 ➔ 2026-10-20 14:15 | 3h 50m | **-20.27%** | **-31.31 USDT** | `exit_ai_early_structural_cut ( 741_AI_PASS)` |
| #7 | **PENGU/USDT:USDT** | 🔴 Short | `711 725 741_AI_PASS` | 2026-10-22 19:30 ➔ 2026-10-23 08:50 | 13h 20m | **-20.80%** | **-30.82 USDT** | `exit_ai_early_structural_cut ( 711 725 741_AI_PASS)` |
| #8 | **ENA/USDT:USDT** | 🔴 Short | `741_AI_PASS` | 2026-10-23 01:05 ➔ 2026-10-23 13:45 | 12h 40m | **-17.99%** | **-28.00 USDT** | `exit_ai_early_structural_cut ( 741_AI_PASS)` |
| #9 | **DOGE/USDT:USDT** | 🔴 Short | `741_AI_PASS` | 2026-10-20 11:45 ➔ 2026-10-20 15:00 | 3h 15m | **-17.63%** | **-27.79 USDT** | `exit_ai_early_structural_cut ( 741_AI_PASS)` |
| #10 | **BCH/USDT:USDT** | 🔴 Short | `711 725 741_AI_PASS` | 2026-10-02 22:05 ➔ 2026-10-03 23:40 | 25h 35m | **-19.73%** | **-27.29 USDT** | `exit_ai_early_structural_cut ( 711 725 741_AI_PASS)` |

### ⏱️ Nhật Ký 15 Lệnh Giao Dịch Gần Nhất (Recent Trades Log)
| # | Cặp giao dịch | Vị thế | Enter Tag | Thời gian Đóng | Thời lượng | Lợi nhuận % | Lợi nhuận USDT | Lý do thoát |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| #1 | **RAYSOL/USDT:USDT** | 🔴 Short | `741_AI_PASS` | 2026-10-26 23:10 | 1h 15m | **+5.60%** | **+10.81 USDT** | `exit_ai_reversal_harvest ( 741_AI_PASS)` |
| #2 | **CHIP/USDT:USDT** | 🔴 Short | `542 ` | 2026-10-26 18:40 | 1h 0m | **+8.67%** | **+12.47 USDT** | `exit_short_adaptive_trailing_scalp ( 542 )` |
| #3 | **VVV/USDT:USDT** | 🔴 Short | `741_AI_PASS` | 2026-10-26 15:00 | 3h 15m | **-18.24%** | **-35.23 USDT** | `exit_ai_early_structural_cut ( 741_AI_PASS)` |
| #4 | **CBRS/USDT:USDT** | 🔴 Short | `741_AI_PASS` | 2026-10-26 13:35 | 4h 25m | **+11.22%** | **+21.67 USDT** | `exit_ai_reversal_harvest ( 741_AI_PASS)` |
| #5 | **ZHIPU/USDT:USDT** | 🔴 Short | `741_AI_PASS` | 2026-10-26 08:35 | 2h 35m | **-17.61%** | **-34.32 USDT** | `exit_ai_early_structural_cut ( 741_AI_PASS)` |
| #6 | **VVV/USDT:USDT** | 🔴 Short | `741_AI_PASS` | 2026-10-26 07:40 | 1h 35m | **+8.36%** | **+16.30 USDT** | `exit_ai_reversal_harvest ( 741_AI_PASS)` |
| #7 | **XRP/USDT:USDT** | 🔴 Short | `741_AI_PASS` | 2026-10-23 22:50 | 6h 10m | **+6.94%** | **+12.99 USDT** | `exit_ai_reversal_harvest ( 741_AI_PASS)` |
| #8 | **FET/USDT:USDT** | 🔴 Short | `741_AI_PASS` | 2026-10-23 19:25 | 2h 45m | **+5.67%** | **+10.62 USDT** | `exit_ai_reversal_harvest ( 741_AI_PASS)` |
| #9 | **BTW/USDT:USDT** | 🟢 Long | `2 ` | 2026-10-23 19:10 | 40m | **+38.38%** | **+53.91 USDT** | `exit_long_normal_d_7_1 ( 2 )` |
| #10 | **AAVE/USDT:USDT** | 🔴 Short | `741_AI_PASS` | 2026-10-23 14:15 | 10m | **+2.07%** | **+3.86 USDT** | `exit_ai_profit_lock ( 741_AI_PASS)` |
| #11 | **ENA/USDT:USDT** | 🔴 Short | `741_AI_PASS` | 2026-10-23 13:45 | 12h 40m | **-17.99%** | **-28.00 USDT** | `exit_ai_early_structural_cut ( 741_AI_PASS)` |
| #12 | **PENGU/USDT:USDT** | 🔴 Short | `711 725 741_AI_PASS` | 2026-10-23 08:50 | 13h 20m | **-20.80%** | **-30.82 USDT** | `exit_ai_early_structural_cut ( 711 725 741_AI_PASS)` |
| #13 | **PUMP/USDT:USDT** | 🔴 Short | `741_AI_PASS` | 2026-10-23 08:00 | 1h 35m | **+5.74%** | **+8.81 USDT** | `exit_ai_reversal_harvest ( 741_AI_PASS)` |
| #14 | **CHIP/USDT:USDT** | 🔴 Short | `741_AI_PASS` | 2026-10-23 06:25 | 6h 20m | **-17.58%** | **-27.02 USDT** | `exit_ai_early_structural_cut ( 741_AI_PASS)` |
| #15 | **SAMSUNG/USDT:USDT** | 🔴 Short | `562 ` | 2026-10-23 00:15 | 11h 20m | **+10.74%** | **+15.78 USDT** | `exit_short_adaptive_trailing_scalp ( 562 )` |

---
*Báo cáo được khởi tạo tự động bởi `scripts/export_report.py` phục vụ chu trình Tối ưu hóa Tự động Agentic AI.*
