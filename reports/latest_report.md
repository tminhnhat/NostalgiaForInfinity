# 📈 Báo Cáo Đánh Giá Hiệu Suất Backtest Toàn Diện (Comprehensive Quantitative Report)

| Thông Tin Phiên Chạy | Chi Tiết | Đánh Dấu / Định Danh |
| :--- | :--- | :--- |
| 🏷️ **Phiên bản Chiến lược (Version)** | **`v7.2`** | `v7.2` |
| 🔖 **Git Commit** | `9c41eeb` | `chore(report): latest 180-day quantitative backtest evaluation on 101 pairs` |
| 🚀 **Đánh dấu lần chạy (Run Marker)** | **`v7.2-latest-180d-101pairs`** | `Workflow #local` |
| 🤖 **Chiến lược (Strategy)** | `NostalgiaForInfinityX8_Combined_AI` | `Combined AI Engine` |
| 📅 **Thời gian đánh giá (Evaluation Date)** | `2026-10-28 09:57:01 UTC` | `UTC` |
| ⏱️ **Cửa sổ Backtest (Timerange)** | `20260501-20261028` | `179 ngày` |
| 📁 **Tệp kết quả (Source File)** | `backtest-result-2026-10-28_16-47-01.zip` | `Binance Futures 5m` |

---

## ⚖️ So Sánh Hiệu Suất Với Lần Backtest Trước (Benchmark Comparison)

| Chỉ số định lượng | Lần chạy này [v7.2-latest-180d-101pairs - 9c41eeb] | Lần trước [v7.2-upstream163-101pairs - b2b4429] | Chênh lệch (Δ Delta) | Xu hướng |
| :--- | :--- | :--- | :--- | :--- |
| **Tỷ lệ thắng (Winrate)** | **84.77%** | **85.02%** | `-0.25%` | 🔴 Suy giảm |
| **Lợi nhuận ròng (Net Profit %)** | **+923.80%** | **+881.20%** | `+42.60%` | 🟢 Cải thiện |
| **Lợi nhuận tuyệt đối (USDT)** | **+1,847.60 USDT** | **+1,762.39 USDT** | `+85.21 USDT` | 🟢 Cải thiện |
| **Hệ số Sharpe (Sharpe Ratio)** | **14.53** | **14.39** | `+0.13` | 🟢 Cải thiện |
| **Hệ số Sortino (Sortino Ratio)** | **19.39** | **18.52** | `+0.87` | 🟢 Cải thiện |
| **Sụt giảm tối đa (Max Drawdown %)** | **6.57%** | **6.56%** | `+0.01%` | 🔴 Suy giảm |
| **Hệ số lãi/lỗ (Profit Factor)** | **2.97** | **2.98** | `-0.02` | 🔴 Suy giảm |
| **Tổng số lệnh (Total Trades)** | **440** | **434** | `+6.00 lệnh` | 🟢 Cải thiện |
| **Chuỗi lệnh thua dài nhất** | **4 trades** | **4 trades** | 0.00 lệnh | ⚪ Tương đương |
| **Kỳ vọng toán học (Expectancy)** | **4.1991** | **4.0608** | `+0.14` | 🟢 Cải thiện |
| **Hệ số Calmar (Calmar Ratio)** | **1500.38** | **1442.44** | `+57.95` | 🟢 Cải thiện |

---

## 🏛️ Ma Trận Lịch Sử Đối Soát Giữa Các Lần Chạy (Multi-Run Version History Matrix)

> *Bảng tổng hợp đối chiếu kết quả backtest qua từng phiên bản và lần chạy để tiện theo dõi tiến trình tối ưu hóa.*

| Đánh dấu lần chạy (Run Marker) | Phiên bản | Commit | Ngày chạy | Tỷ lệ thắng (Winrate) | Lợi nhuận ròng | Max DD % | Sharpe | Profit Factor | Tổng lệnh | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `20261027` | **`v7.0`** | `-` | 20261027 | **89.93%** | +838.73 USDT (+419.4%) | 2.97% | 10.43 | 15.48 | `139` | ⚪ Đã lưu |
| `20261027` | **`v7.0`** | `-` | 20261027 | **76.01%** | +1,056.87 USDT (+528.4%) | 23.23% | 13.55 | 1.74 | `717` | ⚪ Đã lưu |
| `v7.0-baseline` | **`v7.0`** | `1911385` | 20261027 | **95.59%** | +988.89 USDT (+494.4%) | 2.03% | 11.24 | 26.38 | `136` | ⚪ Đã lưu |
| `v7.1-relief-rejection` | **`v7.1`** | `56b0067` | 20261027 | **97.06%** | +1,037.73 USDT (+518.9%) | 2.03% | 11.55 | 39.79 | `136` | ⚪ Đã lưu |
| `20261027` | **`v7.0`** | `-` | 20261027 | **97.08%** | +1,044.41 USDT (+522.2%) | 2.03% | 11.59 | 39.95 | `137` | ⚪ Đã lưu |
| `v7.2-new-short-tags` | **`v7.2`** | `12c4e69` | 20261027 | **97.08%** | +1,044.41 USDT (+522.2%) | 2.03% | 11.59 | 39.95 | `137` | ⚪ Đã lưu |
| `v7.2-upstream163-101pairs` | **`v7.2`** | `b2b4429` | 20261027 | **85.02%** | +1,762.39 USDT (+881.2%) | 6.56% | 14.39 | 2.98 | `434` | ⚪ Đã lưu |
| `v7.2-latest-180d-101pairs` | **`v7.2`** | `9c41eeb` | 20261028 | **84.77%** | +1,847.60 USDT (+923.8%) | 6.57% | 14.53 | 2.97 | `440` | 🎯 **HIỆN TẠI** |

---

## 🎯 Chỉ Số Hiệu Suất Cốt Lõi (Executive Performance Metrics)

| Chỉ số định lượng | Giá trị thực tế | Đánh giá Benchmark | Tiêu chuẩn chất lượng |
| :--- | :--- | :--- | :--- |
| **Tỷ lệ thắng (Winrate)** | **84.77%** | 🟢 Robust | Ngưỡng an toàn >= 70% |
| **Hệ số Sharpe (Sharpe Ratio)** | **14.53** | 🟢 Exceptional | Chuẩn Alpha quỹ >= 2.0 |
| **Hệ số Sortino (Sortino Ratio)** | **19.39** | 🟢 Excellent | Đo lường rủi ro sụt giảm âm |
| **Sụt giảm tài khoản tối đa (Max Drawdown %)** | **6.57%** | 🟢 Defended | Giới hạn rủi ro < 15% |
| **Sụt giảm tuyệt đối (Max Drawdown Abs)** | **+132.92 USDT** | 🟢 Đã kiểm soát | Độ sâu drawdown danh mục |
| **Hệ số lãi/lỗ (Profit Factor)** | **2.97** | 🟢 High | Chuẩn định lượng >= 1.5 |
| **Chuỗi thua dài nhất (Longest Loss Streak)** | **4 trades** | 🟡 Elevated | Kiểm soát chuỗi sụt giảm |

---

## 📊 Chỉ Số Định Lượng Mở Rộng (Secondary Quantitative Indicators)

| Chỉ số định lượng | Kết quả | Mô tả & Ý nghĩa kỹ thuật |
| :--- | :--- | :--- |
| **Tổng số lệnh (Total Trades)** | `440` | Tổng số lệnh đã hoàn tất trong timerange |
| **Tổng lệnh thắng / hòa / thua** | `373` thắng / `0` hòa / `67` thua | Phân bổ kết quả các giao dịch |
| **Lợi nhuận ròng % (Net Profit %)** | `+923.80%` | Tỷ lệ tăng trưởng toàn bộ tài khoản |
| **Lợi nhuận tuyệt đối (Net Profit Abs)** | `+1,847.60 USDT` | Lợi nhuận bằng tiền mặt (USDT) |
| **Lợi nhuận trung bình / lệnh** | `+4.20 USDT` | Hiệu quả trung bình mỗi lần vào lệnh |
| **Mật độ giao dịch (Trades Per Day)** | `2.46 lệnh / ngày` | Tần suất giao dịch bình quân |
| **Kỳ vọng toán học (Expectancy)** | `4.1991` | Lợi nhuận kỳ vọng trên mỗi 1 đơn vị rủi ro |
| **Hệ số Calmar (Calmar Ratio)** | `1500.38` | Tỷ lệ lợi nhuận trên sụt giảm vốn tối đa |
| **Tốc độ tăng trưởng kép (CAGR)** | `11379.87%` | Compound Annual Growth Rate quy năm |

---

## ⚔️ Thống Kê Phân Bổ Vị Thế (Long vs Short Performance)

| Vị thế (Position) | Số lệnh | Tỷ trọng | Tỷ lệ thắng (Winrate) | Lợi nhuận (USDT) | Lợi nhuận (%) | Đánh giá |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 **Lệnh Mua (Long)** | `168` | 38.2% | **99.40%** | **+1,964.87 USDT** | +2575.85% | 🟢 Vượt trội |
| 🔴 **Lệnh Bán (Short)** | `272` | 61.8% | **75.74%** | **-117.26 USDT** | +6.00% | 🟡 Tốt |
| 🌐 **Toàn bộ danh mục** | `440` | 100.0% | **84.77%** | **+1,847.60 USDT** | +923.80% | 🎯 Hoàn tất |

## 🚪 Phân Tích Lý Do Thoát Lệnh (Exit Reason Breakdown)

| Lý do đóng lệnh (Exit Reason) | Số lệnh | Tỷ trọng | Tỷ lệ thắng (Winrate) | Lợi nhuận (USDT) |
| :--- | :--- | :--- | :--- | :--- |
| `TOTAL` | `440` | 100.0% | **84.8%** | +1,847.60 USDT |
| `exit_ai_reversal_harvest ( 741_AI_PASS)` | `91` | 20.7% | **100.0%** | +312.55 USDT |
| `exit_ai_early_structural_cut ( 741_AI_PASS)` | `38` | 8.6% | **0.0%** | -509.33 USDT |
| `exit_ai_reversal_harvest ( 725 741_AI_PASS)` | `26` | 5.9% | **100.0%** | +119.18 USDT |
| `exit_profit_long_rebuy_t_0_1_m ( 64 )` | `14` | 3.2% | **100.0%** | +46.38 USDT |
| `exit_ai_reversal_harvest ( 702 703 731_AI_PASS)` | `12` | 2.7% | **100.0%** | +31.38 USDT |
| `exit_ai_profit_lock ( 741_AI_PASS)` | `12` | 2.7% | **100.0%** | +16.28 USDT |
| `exit_ai_reversal_harvest ( 711 725 741_AI_PASS)` | `10` | 2.3% | **100.0%** | +38.69 USDT |
| `exit_short_adaptive_trailing_scalp ( 562 )` | `9` | 2.0% | **100.0%** | +89.23 USDT |
| `exit_ai_profit_lock ( 725 741_AI_PASS)` | `7` | 1.6% | **100.0%** | +10.45 USDT |
| `exit_profit_long_tc_t_0_1_m ( 142 )` | `7` | 1.6% | **100.0%** | +7.63 USDT |
| `exit_ai_early_structural_cut ( 725 741_AI_PASS)` | `7` | 1.6% | **0.0%** | -101.33 USDT |
| `exit_long_rebuy_d_6_1 ( 64 )` | `5` | 1.1% | **100.0%** | +198.27 USDT |
| `exit_ai_early_structural_cut ( 711 725 741_AI_PASS)` | `5` | 1.1% | **0.0%** | -102.07 USDT |
| `exit_long_rebuy_e_r ( 65 )` | `4` | 0.9% | **100.0%** | +38.05 USDT |
| `exit_ai_reversal_harvest ( 702 703 731 743_AI_PASS)` | `4` | 0.9% | **100.0%** | +12.54 USDT |
| `exit_profit_long_tc_t_0_1_m ( 143 )` | `4` | 0.9% | **100.0%** | +7.28 USDT |
| `exit_profit_long_tc_t_0_1_m ( 144 )` | `4` | 0.9% | **100.0%** | +6.88 USDT |
| `exit_ai_drift_decay ( 741_AI_PASS)` | `4` | 0.9% | **0.0%** | -31.83 USDT |
| `exit_long_quick_q_9 ( 44 )` | `3` | 0.7% | **100.0%** | +56.06 USDT |
| `exit_short_adaptive_trailing_scalp ( 542 )` | `3` | 0.7% | **100.0%** | +24.88 USDT |
| `exit_profit_long_tc_t_1_1_m ( 145 )` | `3` | 0.7% | **100.0%** | +16.85 USDT |
| `exit_long_normal_u_1 ( 2 )` | `3` | 0.7% | **100.0%** | +13.13 USDT |
| `exit_profit_long_tc_t_0_1_m ( 145 )` | `3` | 0.7% | **100.0%** | +8.29 USDT |
| `exit_ai_profit_lock ( 711 725 741_AI_PASS)` | `3` | 0.7% | **100.0%** | +5.16 USDT |
| `exit_profit_long_rebuy_t_0_1_m ( 62 )` | `3` | 0.7% | **100.0%** | +3.69 USDT |
| `exit_profit_short_rebuy_t_0_1_m ( 562 )` | `3` | 0.7% | **100.0%** | +3.16 USDT |
| `exit_long_rebuy_d_7_1 ( 64 )` | `2` | 0.5% | **100.0%** | +128.20 USDT |
| `exit_long_normal_d_4_1 ( 2 )` | `2` | 0.5% | **100.0%** | +80.06 USDT |
| `exit_long_normal_d_7_1 ( 2 )` | `2` | 0.5% | **100.0%** | +61.14 USDT |
| `exit_long_rebuy_d_4_1 ( 65 )` | `2` | 0.5% | **100.0%** | +46.86 USDT |
| `exit_long_quick_q_6 ( 42 )` | `2` | 0.5% | **100.0%** | +46.13 USDT |
| `exit_long_rebuy_d_4_1 ( 64 )` | `2` | 0.5% | **100.0%** | +30.89 USDT |
| `exit_short_rebuy_1_1_1 ( 562 )` | `2` | 0.5% | **100.0%** | +27.86 USDT |
| `exit_long_normal_d_6_1 ( 2 )` | `2` | 0.5% | **100.0%** | +24.73 USDT |
| `exit_ai_reversal_harvest ( 724 741_AI_PASS)` | `2` | 0.5% | **100.0%** | +16.97 USDT |
| `exit_long_rapid_rpd_2 ( 102 )` | `2` | 0.5% | **100.0%** | +16.27 USDT |
| `exit_long_tc_u_1 ( 141 )` | `2` | 0.5% | **100.0%** | +15.24 USDT |
| `exit_long_tc_d_5_1 ( 141 142 )` | `2` | 0.5% | **100.0%** | +9.83 USDT |
| `exit_long_tc_d_5_1 ( 142 )` | `2` | 0.5% | **100.0%** | +9.76 USDT |
| `exit_profit_long_scalp_t_1_1_m ( 163 )` | `2` | 0.5% | **100.0%** | +8.99 USDT |
| `exit_short_rebuy_u_1 ( 562 )` | `2` | 0.5% | **100.0%** | +6.84 USDT |
| `exit_profit_long_tc_t_0_1_m ( 141 )` | `2` | 0.5% | **100.0%** | +3.91 USDT |
| `exit_profit_long_rebuy_t_0_1_m ( 61 )` | `2` | 0.5% | **100.0%** | +3.24 USDT |
| `exit_ai_profit_lock ( 702 703 731_AI_PASS)` | `2` | 0.5% | **100.0%** | +3.19 USDT |
| `exit_profit_long_scalp_t_0_1_m ( 163 )` | `2` | 0.5% | **100.0%** | +1.46 USDT |
| `exit_ai_drift_decay ( 725 741_AI_PASS)` | `2` | 0.5% | **0.0%** | -3.34 USDT |
| `exit_short_universal_structural_cut ( 562 )` | `2` | 0.5% | **0.0%** | -21.77 USDT |
| `exit_ai_early_structural_cut ( 724 741_AI_PASS)` | `2` | 0.5% | **0.0%** | -38.16 USDT |
| `exit_short_universal_structural_cut ( 741_AI_PASS)` | `2` | 0.5% | **0.0%** | -42.12 USDT |
| `exit_long_rebuy_d_6_1 ( 62 )` | `1` | 0.2% | **100.0%** | +68.36 USDT |
| `exit_long_rebuy_2_1_1 ( 64 )` | `1` | 0.2% | **100.0%** | +66.16 USDT |
| `exit_long_quick_d_11_1 ( 43 )` | `1` | 0.2% | **100.0%** | +63.85 USDT |
| `exit_long_tc_d_3_2 ( 141 )` | `1` | 0.2% | **100.0%** | +47.82 USDT |
| `exit_long_normal_d_6_1 ( 1 )` | `1` | 0.2% | **100.0%** | +43.13 USDT |
| `exit_long_rapid_d_5_1 ( 103 )` | `1` | 0.2% | **100.0%** | +38.55 USDT |
| `exit_long_rebuy_d_8_1 ( 64 )` | `1` | 0.2% | **100.0%** | +37.51 USDT |
| `exit_long_rebuy_w_6_1 ( 64 )` | `1` | 0.2% | **100.0%** | +34.90 USDT |
| `exit_long_normal_d_4_1 ( 6 )` | `1` | 0.2% | **100.0%** | +33.58 USDT |
| `exit_long_normal_d_7_1 ( 6 )` | `1` | 0.2% | **100.0%** | +32.46 USDT |
| `exit_long_tc_d_8_1 ( 142 )` | `1` | 0.2% | **100.0%** | +30.85 USDT |
| `exit_long_tc_d_3_1 ( 141 )` | `1` | 0.2% | **100.0%** | +29.01 USDT |
| `exit_long_tc_d_5_1 ( 141 )` | `1` | 0.2% | **100.0%** | +27.87 USDT |
| `exit_short_adaptive_trailing_mega ( 562 )` | `1` | 0.2% | **100.0%** | +25.15 USDT |
| `exit_long_scalp_d_5_1 ( 163 )` | `1` | 0.2% | **100.0%** | +24.86 USDT |
| `exit_long_normal_u_3 ( 6 141 )` | `1` | 0.2% | **100.0%** | +23.32 USDT |
| `exit_long_tc_3_1_1 ( 141 142 )` | `1` | 0.2% | **100.0%** | +22.74 USDT |
| `exit_long_rebuy_d_9_1 ( 65 )` | `1` | 0.2% | **100.0%** | +22.00 USDT |
| `exit_long_tc_d_6_1 ( 144 )` | `1` | 0.2% | **100.0%** | +18.07 USDT |
| `exit_profit_long_rebuy_t_7_1_m ( 63 )` | `1` | 0.2% | **100.0%** | +18.00 USDT |
| `exit_short_adaptive_trailing_scalp ( 711 725 741_AI_PASS)` | `1` | 0.2% | **100.0%** | +15.82 USDT |
| `exit_long_scalp_d_6_1 ( 61 162 )` | `1` | 0.2% | **100.0%** | +15.06 USDT |
| `exit_long_rebuy_d_6_1 ( 63 )` | `1` | 0.2% | **100.0%** | +14.65 USDT |
| `exit_long_rebuy_d_6_1 ( 61 )` | `1` | 0.2% | **100.0%** | +13.78 USDT |
| `exit_long_quick_q_6 ( 47 )` | `1` | 0.2% | **100.0%** | +13.74 USDT |
| `exit_long_rebuy_d_8_1 ( 61 )` | `1` | 0.2% | **100.0%** | +13.67 USDT |
| `exit_long_scalp_d_6_1 ( 162 )` | `1` | 0.2% | **100.0%** | +13.27 USDT |
| `exit_profit_long_tc_t_2_1_m ( 145 )` | `1` | 0.2% | **100.0%** | +13.14 USDT |
| `exit_long_tc_d_5_1 ( 145 )` | `1` | 0.2% | **100.0%** | +12.55 USDT |
| `exit_profit_long_normal_t_2_1_m ( 3 )` | `1` | 0.2% | **100.0%** | +11.81 USDT |
| `exit_ai_reversal_harvest ( 702 703 705 731_AI_PASS)` | `1` | 0.2% | **100.0%** | +11.80 USDT |
| `exit_long_quick_d_7_1 ( 42 )` | `1` | 0.2% | **100.0%** | +11.41 USDT |
| `exit_profit_long_quick_t_2_1_m ( 46 )` | `1` | 0.2% | **100.0%** | +11.35 USDT |
| `exit_long_tc_u_1 ( 141 142 )` | `1` | 0.2% | **100.0%** | +11.06 USDT |
| `exit_long_tc_u_1 ( 142 )` | `1` | 0.2% | **100.0%** | +10.71 USDT |
| `exit_profit_long_tc_t_2_1_m ( 142 )` | `1` | 0.2% | **100.0%** | +10.69 USDT |
| `exit_long_normal_d_3_2 ( 5 )` | `1` | 0.2% | **100.0%** | +10.66 USDT |
| `exit_profit_short_rebuy_t_1_1_m ( 562 )` | `1` | 0.2% | **100.0%** | +10.64 USDT |
| `exit_long_rebuy_d_5_1 ( 63 )` | `1` | 0.2% | **100.0%** | +9.92 USDT |
| `exit_long_tc_d_6_1 ( 141 )` | `1` | 0.2% | **100.0%** | +9.29 USDT |
| `exit_long_normal_u_1 ( 1 )` | `1` | 0.2% | **100.0%** | +9.05 USDT |
| `exit_long_tc_d_6_1 ( 141 143 163 )` | `1` | 0.2% | **100.0%** | +8.26 USDT |
| `exit_profit_long_normal_t_1_1_m ( 3 )` | `1` | 0.2% | **100.0%** | +7.80 USDT |
| `exit_profit_long_tc_t_1_1_m ( 141 )` | `1` | 0.2% | **100.0%** | +7.68 USDT |
| `exit_profit_long_rebuy_t_3_1_m ( 61 )` | `1` | 0.2% | **100.0%** | +7.61 USDT |
| `exit_profit_long_tc_t_1_1_m ( 141 142 )` | `1` | 0.2% | **100.0%** | +7.55 USDT |
| `exit_long_tc_d_4_2 ( 145 )` | `1` | 0.2% | **100.0%** | +7.37 USDT |
| `exit_long_tc_d_6_1 ( 142 )` | `1` | 0.2% | **100.0%** | +7.13 USDT |
| `exit_long_normal_u_4 ( 1 61 )` | `1` | 0.2% | **100.0%** | +6.93 USDT |
| `exit_long_tc_d_5_1 ( 62 144 )` | `1` | 0.2% | **100.0%** | +6.72 USDT |
| `exit_long_normal_d_8_1 ( 4 )` | `1` | 0.2% | **100.0%** | +6.66 USDT |
| `exit_profit_long_rebuy_t_2_1_m ( 65 )` | `1` | 0.2% | **100.0%** | +6.59 USDT |
| `exit_ai_reversal_harvest ( 703 721 741_AI_PASS)` | `1` | 0.2% | **100.0%** | +6.47 USDT |
| `exit_long_normal_d_7_1 ( 2 101 141 )` | `1` | 0.2% | **100.0%** | +6.35 USDT |
| `exit_long_normal_d_2_1 ( 1 )` | `1` | 0.2% | **100.0%** | +6.30 USDT |
| `exit_long_normal_d_5_1 ( 2 )` | `1` | 0.2% | **100.0%** | +6.01 USDT |
| `exit_long_tc_d_5_1 ( 144 )` | `1` | 0.2% | **100.0%** | +5.51 USDT |
| `exit_profit_long_normal_t_0_1_m ( 2 )` | `1` | 0.2% | **100.0%** | +5.22 USDT |
| `exit_long_normal_d_5_1 ( 6 102 141 )` | `1` | 0.2% | **100.0%** | +5.13 USDT |
| `exit_long_tc_d_3_2 ( 102 142 )` | `1` | 0.2% | **100.0%** | +5.07 USDT |
| `exit_long_normal_d_5_1 ( 5 )` | `1` | 0.2% | **100.0%** | +4.86 USDT |
| `exit_profit_long_rapid_t_1_1_m ( 102 )` | `1` | 0.2% | **100.0%** | +4.59 USDT |
| `exit_long_quick_q_2 ( 41 )` | `1` | 0.2% | **100.0%** | +4.58 USDT |
| `exit_long_normal_d_6_1 ( 2 141 )` | `1` | 0.2% | **100.0%** | +4.52 USDT |
| `exit_profit_long_tc_t_0_1_m ( 141 142 )` | `1` | 0.2% | **100.0%** | +4.41 USDT |
| `exit_long_normal_u_2 ( 4 41 61 )` | `1` | 0.2% | **100.0%** | +3.88 USDT |
| `exit_long_rapid_rpd_6 ( 102 )` | `1` | 0.2% | **100.0%** | +3.80 USDT |
| `exit_profit_long_tc_t_3_1_m ( 143 )` | `1` | 0.2% | **100.0%** | +3.75 USDT |
| `exit_profit_long_rebuy_t_1_1_m ( 62 )` | `1` | 0.2% | **100.0%** | +3.70 USDT |
| `exit_profit_long_rebuy_t_2_1_m ( 62 )` | `1` | 0.2% | **100.0%** | +3.44 USDT |
| `exit_ai_reversal_harvest ( 742_AI_PASS)` | `1` | 0.2% | **100.0%** | +3.25 USDT |
| `exit_ai_reversal_harvest ( 721 724 731_AI_PASS)` | `1` | 0.2% | **100.0%** | +2.66 USDT |
| `exit_profit_long_normal_t_0_1_m ( 6 102 )` | `1` | 0.2% | **100.0%** | +2.58 USDT |
| `exit_long_quick_u_1 ( 42 )` | `1` | 0.2% | **100.0%** | +2.51 USDT |
| `exit_ai_reversal_harvest ( 702 731 743_AI_PASS)` | `1` | 0.2% | **100.0%** | +2.41 USDT |
| `exit_ai_profit_lock ( 702 703 706 731 743_AI_PASS)` | `1` | 0.2% | **100.0%** | +2.41 USDT |
| `exit_ai_reversal_harvest ( 703 721 731_AI_PASS)` | `1` | 0.2% | **100.0%** | +2.31 USDT |
| `exit_long_normal_u_2 ( 2 )` | `1` | 0.2% | **100.0%** | +2.27 USDT |
| `exit_ai_reversal_harvest ( 711 741_AI_PASS)` | `1` | 0.2% | **100.0%** | +2.19 USDT |
| `exit_long_quick_u_1 ( 43 )` | `1` | 0.2% | **100.0%** | +1.82 USDT |
| `exit_profit_long_scalp_t_2_1_m ( 163 )` | `1` | 0.2% | **100.0%** | +1.77 USDT |
| `exit_short_adaptive_trailing_scalp ( 702 703 731_AI_PASS)` | `1` | 0.2% | **100.0%** | +1.72 USDT |
| `exit_profit_long_normal_t_0_1_m ( 6 )` | `1` | 0.2% | **100.0%** | +1.71 USDT |
| `exit_profit_long_rebuy_t_2_1_m ( 64 )` | `1` | 0.2% | **100.0%** | +1.70 USDT |
| `exit_ai_reversal_harvest ( 721 724 741_AI_PASS)` | `1` | 0.2% | **100.0%** | +1.65 USDT |
| `exit_profit_long_normal_t_2_1_m ( 2 63 101 )` | `1` | 0.2% | **100.0%** | +1.62 USDT |
| `exit_profit_long_scalp_t_0_1_m ( 161 )` | `1` | 0.2% | **100.0%** | +1.52 USDT |
| `exit_long_tc_u_1 ( 144 )` | `1` | 0.2% | **100.0%** | +1.47 USDT |
| `exit_profit_long_normal_t_0_1_m ( 3 )` | `1` | 0.2% | **100.0%** | +1.34 USDT |
| `exit_ai_reversal_harvest ( 701 702 703 731 743_AI_PASS)` | `1` | 0.2% | **100.0%** | +1.24 USDT |
| `exit_profit_long_quick_t_1_1_m ( 42 )` | `1` | 0.2% | **100.0%** | +1.17 USDT |
| `exit_profit_long_rapid_t_0_1_m ( 102 )` | `1` | 0.2% | **100.0%** | +1.13 USDT |
| `exit_profit_long_scalp_t_0_1_m ( 162 )` | `1` | 0.2% | **100.0%** | +0.95 USDT |
| `exit_profit_long_quick_t_0_1_m ( 43 )` | `1` | 0.2% | **100.0%** | +0.85 USDT |
| `exit_ai_profit_lock ( 721 741_AI_PASS)` | `1` | 0.2% | **100.0%** | +0.84 USDT |
| `exit_long_normal_w_0_1 ( 1 )` | `1` | 0.2% | **100.0%** | +0.64 USDT |
| `exit_ai_profit_lock ( 703 721 741_AI_PASS)` | `1` | 0.2% | **100.0%** | +0.52 USDT |
| `exit_ai_profit_lock ( 703 705 706 731_AI_PASS)` | `1` | 0.2% | **100.0%** | +0.43 USDT |
| `exit_ai_profit_lock ( 724 741_AI_PASS)` | `1` | 0.2% | **100.0%** | +0.42 USDT |
| `exit_long_normal_w_0_1 ( 3 )` | `1` | 0.2% | **100.0%** | +0.37 USDT |
| `exit_profit_long_normal_t_0_1_m ( 5 )` | `1` | 0.2% | **100.0%** | +0.36 USDT |
| `exit_profit_long_normal_t_0_1_m ( 3 142 )` | `1` | 0.2% | **100.0%** | +0.18 USDT |
| `exit_ai_562_aged_breakeven ( 562 )` | `1` | 0.2% | **0.0%** | -4.40 USDT |
| `exit_bad_trade_abandon_18d ( 120 )` | `1` | 0.2% | **0.0%** | -10.57 USDT |
| `exit_ai_drift_decay ( 711 725 741_AI_PASS)` | `1` | 0.2% | **0.0%** | -11.26 USDT |
| `exit_short_universal_structural_cut ( 542 )` | `1` | 0.2% | **0.0%** | -16.52 USDT |
| `exit_short_universal_structural_cut ( 725 741_AI_PASS)` | `1` | 0.2% | **0.0%** | -45.43 USDT |

## 🔍 Bảng Phân Tích Đầy Đủ Tất Cả Các Entry Tags (Full Enter Tag Breakdown)

> *Bảng tổng hợp chi tiết 100% tất cả các tag tín hiệu vào lệnh (Entry Tags) đã hoạt động trong phiên backtest.*

| Enter Tag | Vị thế | Số lệnh | Tỷ lệ thắng (Winrate) | Thắng/Hòa/Thua | Tổng LN % | Tổng LN (USDT) | LN TB/Lệnh | Thời lượng TB | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `TOTAL` | 🟢 Long Core | `440` | **84.8%** | 373/0/67 | +923.80% | **+1,847.60 USDT** | +5.87% | 10:01:00 | 🟢 Tối ưu |
| `64` | 🟢 Long Core | `27` | **100.0%** | 27/0/0 | +272.01% | **+544.02 USDT** | +18.22% | 10:41:00 | 🟢 Tối ưu |
| `2` | 🟢 Long Core | `12` | **100.0%** | 12/0/0 | +96.28% | **+192.56 USDT** | +20.29% | 2:08:00 | 🟢 Tối ưu |
| `141` | 🟢 Long Core | `9` | **100.0%** | 9/0/0 | +70.41% | **+140.83 USDT** | +13.21% | 9:31:00 | 🟢 Tối ưu |
| `562` | 🟢 Long Core | `21` | **85.7%** | 18/0/3 | +68.35% | **+136.70 USDT** | +5.75% | 1 day, 6:33:00 | 🟢 Tối ưu |
| `65` | 🟢 Long Core | `8` | **100.0%** | 8/0/0 | +56.75% | **+113.50 USDT** | +20.10% | 2:26:00 | 🟢 Tối ưu |
| `62` | 🟢 Long Core | `6` | **100.0%** | 6/0/0 | +39.60% | **+79.19 USDT** | +8.42% | 14:27:00 | 🟢 Tối ưu |
| `142` | 🟢 Long Core | `13` | **100.0%** | 13/0/0 | +38.39% | **+76.77 USDT** | +11.81% | 8:32:00 | 🟢 Tối ưu |
| `6` | 🟢 Long Core | `3` | **100.0%** | 3/0/0 | +33.88% | **+67.75 USDT** | +18.75% | 17:13:00 | 🟢 Tối ưu |
| `43` | 🟢 Long Core | `3` | **100.0%** | 3/0/0 | +33.27% | **+66.53 USDT** | +26.00% | 0:35:00 | 🟢 Tối ưu |
| `42` | 🟢 Long Core | `5` | **100.0%** | 5/0/0 | +30.61% | **+61.23 USDT** | +15.36% | 2 days, 5:12:00 | 🟢 Tối ưu |
| `1` | 🟢 Long Core | `4` | **100.0%** | 4/0/0 | +29.56% | **+59.11 USDT** | +10.99% | 1 day, 20:39:00 | 🟢 Tối ưu |
| `145` | 🟢 Long Core | `9` | **100.0%** | 9/0/0 | +29.10% | **+58.20 USDT** | +10.61% | 8:46:00 | 🟢 Tối ưu |
| `44` | 🟢 Long Core | `3` | **100.0%** | 3/0/0 | +28.03% | **+56.06 USDT** | +22.49% | 2:32:00 | 🟢 Tối ưu |
| `141 142` | 🟢 Long Core | `6` | **100.0%** | 6/0/0 | +27.79% | **+55.59 USDT** | +13.96% | 9:57:00 | 🟢 Tối ưu |
| `63` | 🟢 Long Core | `3` | **100.0%** | 3/0/0 | +21.29% | **+42.57 USDT** | +33.10% | 3:02:00 | 🟢 Tối ưu |
| `103` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +19.27% | **+38.55 USDT** | +25.41% | 2:30:00 | 🟢 Tối ưu |
| `61` | 🟢 Long Core | `5` | **100.0%** | 5/0/0 | +19.15% | **+38.29 USDT** | +20.53% | 2:10:00 | 🟢 Tối ưu |
| `163` | 🟢 Long Core | `6` | **100.0%** | 6/0/0 | +18.54% | **+37.08 USDT** | +9.34% | 2:25:00 | 🟢 Tối ưu |
| `702 703 731_AI_PASS` | 🤖 Short AI Gatekeeper | `15` | **100.0%** | 15/0/0 | +18.14% | **+36.28 USDT** | +5.55% | 5:03:00 | 🟢 Tối ưu |
| `144` | 🟢 Long Core | `7` | **100.0%** | 7/0/0 | +15.96% | **+31.92 USDT** | +11.44% | 12:38:00 | 🟢 Tối ưu |
| `102` | 🟢 Long Core | `5` | **100.0%** | 5/0/0 | +12.89% | **+25.79 USDT** | +5.24% | 2:58:00 | 🟢 Tối ưu |
| `6 141` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +11.66% | **+23.32 USDT** | +16.21% | 19:20:00 | 🟢 Tối ưu |
| `3` | 🟢 Long Core | `4` | **100.0%** | 4/0/0 | +10.66% | **+21.33 USDT** | +5.10% | 19:42:00 | 🟢 Tối ưu |
| `5` | 🟢 Long Core | `3` | **100.0%** | 3/0/0 | +7.94% | **+15.88 USDT** | +14.52% | 3:03:00 | 🟢 Tối ưu |
| `61 162` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +7.53% | **+15.06 USDT** | +32.22% | 4:05:00 | 🟢 Tối ưu |
| `162` | 🟢 Long Core | `2` | **100.0%** | 2/0/0 | +7.11% | **+14.21 USDT** | +17.33% | 0:52:00 | 🟢 Tối ưu |
| `47` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +6.87% | **+13.74 USDT** | +13.38% | 1 day, 2:00:00 | 🟢 Tối ưu |
| `702 703 731 743_AI_PASS` | 🤖 Short AI Gatekeeper | `4` | **100.0%** | 4/0/0 | +6.27% | **+12.54 USDT** | +5.77% | 2:32:00 | 🟢 Tối ưu |
| `702 703 705 731_AI_PASS` | 🤖 Short AI Gatekeeper | `1` | **100.0%** | 1/0/0 | +5.90% | **+11.80 USDT** | +6.15% | 7:45:00 | 🟢 Tối ưu |
| `46` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +5.67% | **+11.35 USDT** | +11.97% | 0:45:00 | 🟢 Tối ưu |
| `143` | 🟢 Long Core | `5` | **100.0%** | 5/0/0 | +5.52% | **+11.03 USDT** | +5.30% | 18:36:00 | 🟢 Tối ưu |
| `542` | 🟢 Long Core | `4` | **75.0%** | 3/0/1 | +4.18% | **+8.36 USDT** | +1.59% | 1:24:00 | 🟡 Hiệu quả |
| `141 143 163` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +4.13% | **+8.26 USDT** | +33.41% | 1:30:00 | 🟢 Tối ưu |
| `703 721 741_AI_PASS` | 🤖 Short AI Gatekeeper | `2` | **100.0%** | 2/0/0 | +3.49% | **+6.99 USDT** | +4.93% | 2:32:00 | 🟢 Tối ưu |
| `1 61` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +3.47% | **+6.93 USDT** | +21.38% | 0:15:00 | 🟢 Tối ưu |
| `62 144` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +3.36% | **+6.72 USDT** | +25.85% | 1:25:00 | 🟢 Tối ưu |
| `4` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +3.33% | **+6.66 USDT** | +44.22% | 1:10:00 | 🟢 Tối ưu |
| `2 101 141` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +3.17% | **+6.35 USDT** | +36.21% | 1:00:00 | 🟢 Tối ưu |
| `6 102 141` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +2.56% | **+5.13 USDT** | +26.17% | 1:00:00 | 🟢 Tối ưu |
| `102 142` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +2.53% | **+5.07 USDT** | +19.97% | 1:40:00 | 🟢 Tối ưu |
| `41` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +2.29% | **+4.58 USDT** | +11.69% | 5:00:00 | 🟢 Tối ưu |
| `2 141` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +2.26% | **+4.52 USDT** | +30.19% | 2:15:00 | 🟢 Tối ưu |
| `4 41 61` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +1.94% | **+3.88 USDT** | +11.78% | 0:10:00 | 🟢 Tối ưu |
| `742_AI_PASS` | 🤖 Short AI Gatekeeper | `1` | **100.0%** | 1/0/0 | +1.63% | **+3.25 USDT** | +5.81% | 0:40:00 | 🟢 Tối ưu |
| `721 724 731_AI_PASS` | 🤖 Short AI Gatekeeper | `1` | **100.0%** | 1/0/0 | +1.33% | **+2.66 USDT** | +6.65% | 17:10:00 | 🟢 Tối ưu |
| `6 102` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +1.29% | **+2.58 USDT** | +1.43% | 2:05:00 | 🟢 Tối ưu |
| `702 731 743_AI_PASS` | 🤖 Short AI Gatekeeper | `1` | **100.0%** | 1/0/0 | +1.21% | **+2.41 USDT** | +6.75% | 9:05:00 | 🟢 Tối ưu |
| `702 703 706 731 743_AI_PASS` | 🤖 Short AI Gatekeeper | `1` | **100.0%** | 1/0/0 | +1.20% | **+2.41 USDT** | +1.60% | 0:45:00 | 🟢 Tối ưu |
| `703 721 731_AI_PASS` | 🤖 Short AI Gatekeeper | `1` | **100.0%** | 1/0/0 | +1.16% | **+2.31 USDT** | +5.07% | 5:00:00 | 🟢 Tối ưu |
| `711 741_AI_PASS` | 🤖 Short AI Gatekeeper | `1` | **100.0%** | 1/0/0 | +1.10% | **+2.19 USDT** | +5.45% | 5:05:00 | 🟢 Tối ưu |
| `721 724 741_AI_PASS` | 🤖 Short AI Gatekeeper | `1` | **100.0%** | 1/0/0 | +0.83% | **+1.65 USDT** | +5.13% | 4:00:00 | 🟢 Tối ưu |
| `2 63 101` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +0.81% | **+1.62 USDT** | +10.72% | 2:55:00 | 🟢 Tối ưu |
| `161` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +0.76% | **+1.52 USDT** | +2.68% | 12:05:00 | 🟢 Tối ưu |
| `701 702 703 731 743_AI_PASS` | 🤖 Short AI Gatekeeper | `1` | **100.0%** | 1/0/0 | +0.62% | **+1.24 USDT** | +4.83% | 7:35:00 | 🟢 Tối ưu |
| `721 741_AI_PASS` | 🤖 Short AI Gatekeeper | `1` | **100.0%** | 1/0/0 | +0.42% | **+0.84 USDT** | +1.74% | 7:50:00 | 🟢 Tối ưu |
| `703 705 706 731_AI_PASS` | 🤖 Short AI Gatekeeper | `1` | **100.0%** | 1/0/0 | +0.22% | **+0.43 USDT** | +1.92% | 6:05:00 | 🟢 Tối ưu |
| `3 142` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +0.09% | **+0.18 USDT** | +0.63% | 19:15:00 | 🟢 Tối ưu |
| `120` | 🟢 Long Core | `1` | **0.0%** | 0/0/1 | -5.28% | **-10.57 USDT** | -10.12% | 17 days, 22:40:00 | 🔴 Cần tinh chỉnh |
| `725 741_AI_PASS` | 🤖 Short AI Gatekeeper | `43` | **76.7%** | 33/0/10 | -10.24% | **-20.47 USDT** | +0.27% | 6:32:00 | 🔴 Cần tinh chỉnh |
| `724 741_AI_PASS` | 🤖 Short AI Gatekeeper | `5` | **60.0%** | 3/0/2 | -10.38% | **-20.77 USDT** | -4.86% | 7:42:00 | 🔴 Cần tinh chỉnh |
| `711 725 741_AI_PASS` | 🤖 Short AI Gatekeeper | `20` | **70.0%** | 14/0/6 | -26.83% | **-53.67 USDT** | -1.84% | 7:29:00 | 🔴 Cần tinh chỉnh |
| `741_AI_PASS` | 🤖 Short AI Gatekeeper | `147` | **70.1%** | 103/0/44 | -127.22% | **-254.44 USDT** | -1.63% | 6:54:00 | 🔴 Cần tinh chỉnh |

---

## 📑 Chi Tiết Các Lệnh Giao Dịch (Trade Execution Journal)

### 🥇 Top 10 Lệnh Lãi Cao Nhất (Top Winning Trades)
| # | Cặp giao dịch | Vị thế | Enter Tag | Thời gian Mở ➔ Đóng | Thời lượng | Lợi nhuận % | Lợi nhuận USDT | Lý do thoát |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| #1 | **BAT/USDT:USDT** | 🟢 Long | `64 ` | 2026-10-08 08:20 ➔ 2026-10-09 06:05 | 21h 45m | **+43.38%** | **+74.67 USDT** | `exit_long_rebuy_d_7_1 ( 64 )` |
| #2 | **GRASS/USDT:USDT** | 🟢 Long | `62 ` | 2026-10-14 17:45 ➔ 2026-10-15 15:05 | 21h 20m | **+33.86%** | **+68.36 USDT** | `exit_long_rebuy_d_6_1 ( 62 )` |
| #3 | **ARB/USDT:USDT** | 🟢 Long | `64 ` | 2026-09-17 21:45 ➔ 2026-09-18 01:50 | 4h 5m | **+59.20%** | **+66.16 USDT** | `exit_long_rebuy_2_1_1 ( 64 )` |
| #4 | **BTW/USDT:USDT** | 🟢 Long | `43 ` | 2026-10-05 06:45 ➔ 2026-10-05 08:05 | 1h 20m | **+71.12%** | **+63.85 USDT** | `exit_long_quick_d_11_1 ( 43 )` |
| #5 | **BTW/USDT:USDT** | 🟢 Long | `2 ` | 2026-10-23 18:30 ➔ 2026-10-23 19:10 | 40m | **+38.38%** | **+54.77 USDT** | `exit_long_normal_d_7_1 ( 2 )` |
| #6 | **WLD/USDT:USDT** | 🟢 Long | `64 ` | 2026-09-26 22:25 ➔ 2026-09-27 10:10 | 11h 45m | **+40.20%** | **+53.53 USDT** | `exit_long_rebuy_d_7_1 ( 64 )` |
| #7 | **GRASS/USDT:USDT** | 🟢 Long | `64 ` | 2026-10-05 14:55 ➔ 2026-10-05 19:15 | 4h 20m | **+32.17%** | **+50.72 USDT** | `exit_long_rebuy_d_6_1 ( 64 )` |
| #8 | **BAT/USDT:USDT** | 🟢 Long | `64 ` | 2026-10-03 06:15 ➔ 2026-10-04 07:40 | 25h 25m | **+33.11%** | **+48.88 USDT** | `exit_long_rebuy_d_6_1 ( 64 )` |
| #9 | **WLD/USDT:USDT** | 🟢 Long | `141 ` | 2026-10-25 08:55 ➔ 2026-10-25 15:40 | 6h 45m | **+19.30%** | **+47.82 USDT** | `exit_long_tc_d_3_2 ( 141 )` |
| #10 | **BTW/USDT:USDT** | 🟢 Long | `1 ` | 2026-10-22 20:45 ➔ 2026-10-22 21:40 | 55m | **+30.41%** | **+43.13 USDT** | `exit_long_normal_d_6_1 ( 1 )` |

### ⚠️ Top Lệnh Thua Lỗ / Sụt Giảm Lớn Nhất (Top Drawdown Trades)
| # | Cặp giao dịch | Vị thế | Enter Tag | Thời gian Mở ➔ Đóng | Thời lượng | Thua lỗ % | Thua lỗ USDT | Lý do thoát |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| #1 | **WLD/USDT:USDT** | 🔴 Short | `725 741_AI_PASS` | 2026-10-16 20:40 ➔ 2026-10-17 03:30 | 6h 50m | **-23.91%** | **-45.43 USDT** | `exit_short_universal_structural_cut ( 725 741_AI_PASS)` |
| #2 | **RAYSOL/USDT:USDT** | 🔴 Short | `741_AI_PASS` | 2026-10-20 01:05 ➔ 2026-10-20 14:15 | 13h 10m | **-24.05%** | **-37.42 USDT** | `exit_short_universal_structural_cut ( 741_AI_PASS)` |
| #3 | **ZEC/USDT:USDT** | 🔴 Short | `724 741_AI_PASS` | 2026-10-20 09:05 ➔ 2026-10-20 13:55 | 4h 50m | **-17.88%** | **-35.18 USDT** | `exit_ai_early_structural_cut ( 724 741_AI_PASS)` |
| #4 | **QNT/USDT:USDT** | 🔴 Short | `741_AI_PASS` | 2026-10-20 10:25 ➔ 2026-10-20 14:15 | 3h 50m | **-20.27%** | **-32.09 USDT** | `exit_ai_early_structural_cut ( 741_AI_PASS)` |
| #5 | **PENGU/USDT:USDT** | 🔴 Short | `711 725 741_AI_PASS` | 2026-10-22 19:30 ➔ 2026-10-23 08:50 | 13h 20m | **-20.80%** | **-31.31 USDT** | `exit_ai_early_structural_cut ( 711 725 741_AI_PASS)` |
| #6 | **ZAMA/USDT:USDT** | 🔴 Short | `741_AI_PASS` | 2026-10-27 04:40 ➔ 2026-10-27 12:50 | 8h 10m | **-18.66%** | **-31.11 USDT** | `exit_ai_early_structural_cut ( 741_AI_PASS)` |
| #7 | **STRK/USDT:USDT** | 🔴 Short | `741_AI_PASS` | 2026-10-27 10:50 ➔ 2026-10-27 19:20 | 8h 30m | **-18.40%** | **-30.97 USDT** | `exit_ai_early_structural_cut ( 741_AI_PASS)` |
| #8 | **ZHIPU/USDT:USDT** | 🔴 Short | `741_AI_PASS` | 2026-10-26 06:00 ➔ 2026-10-26 08:35 | 2h 35m | **-17.61%** | **-28.72 USDT** | `exit_ai_early_structural_cut ( 741_AI_PASS)` |
| #9 | **ENA/USDT:USDT** | 🔴 Short | `741_AI_PASS` | 2026-10-23 01:05 ➔ 2026-10-23 13:45 | 12h 40m | **-17.99%** | **-28.44 USDT** | `exit_ai_early_structural_cut ( 741_AI_PASS)` |
| #10 | **DOGE/USDT:USDT** | 🔴 Short | `741_AI_PASS` | 2026-10-20 11:45 ➔ 2026-10-20 15:00 | 3h 15m | **-17.63%** | **-28.23 USDT** | `exit_ai_early_structural_cut ( 741_AI_PASS)` |

### ⏱️ Nhật Ký 15 Lệnh Giao Dịch Gần Nhất (Recent Trades Log)
| # | Cặp giao dịch | Vị thế | Enter Tag | Thời gian Đóng | Thời lượng | Lợi nhuận % | Lợi nhuận USDT | Lý do thoát |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| #1 | **STRK/USDT:USDT** | 🔴 Short | `741_AI_PASS` | 2026-10-27 19:20 | 8h 30m | **-18.40%** | **-30.97 USDT** | `exit_ai_early_structural_cut ( 741_AI_PASS)` |
| #2 | **DOGE/USDT:USDT** | 🔴 Short | `741_AI_PASS` | 2026-10-27 15:10 | 36h 0m | **-8.41%** | **-17.06 USDT** | `exit_ai_drift_decay ( 741_AI_PASS)` |
| #3 | **ZAMA/USDT:USDT** | 🔴 Short | `741_AI_PASS` | 2026-10-27 12:50 | 8h 10m | **-18.66%** | **-31.11 USDT** | `exit_ai_early_structural_cut ( 741_AI_PASS)` |
| #4 | **ARB/USDT:USDT** | 🔴 Short | `725 741_AI_PASS` | 2026-10-27 09:45 | 3h 50m | **+7.76%** | **+12.99 USDT** | `exit_ai_reversal_harvest ( 725 741_AI_PASS)` |
| #5 | **SOL/USDT:USDT** | 🔴 Short | `741_AI_PASS` | 2026-10-27 05:35 | 21h 0m | **+4.85%** | **+7.80 USDT** | `exit_ai_reversal_harvest ( 741_AI_PASS)` |
| #6 | **FET/USDT:USDT** | 🔴 Short | `702 703 731_AI_PASS` | 2026-10-27 03:10 | 7h 5m | **+6.13%** | **+9.93 USDT** | `exit_ai_reversal_harvest ( 702 703 731_AI_PASS)` |
| #7 | **RAYSOL/USDT:USDT** | 🔴 Short | `724 741_AI_PASS` | 2026-10-27 03:05 | 22h 45m | **+6.31%** | **+12.86 USDT** | `exit_ai_reversal_harvest ( 724 741_AI_PASS)` |
| #8 | **BTW/USDT:USDT** | 🟢 Long | `103 ` | 2026-10-26 21:45 | 2h 30m | **+25.41%** | **+38.55 USDT** | `exit_long_rapid_d_5_1 ( 103 )` |
| #9 | **CHIP/USDT:USDT** | 🔴 Short | `542 ` | 2026-10-26 18:40 | 1h 0m | **+8.67%** | **+13.07 USDT** | `exit_short_adaptive_trailing_scalp ( 542 )` |
| #10 | **ZHIPU/USDT:USDT** | 🔴 Short | `741_AI_PASS` | 2026-10-26 08:35 | 2h 35m | **-17.61%** | **-28.72 USDT** | `exit_ai_early_structural_cut ( 741_AI_PASS)` |
| #11 | **ARB/USDT:USDT** | 🔴 Short | `741_AI_PASS` | 2026-10-26 03:55 | 45m | **+5.26%** | **+10.67 USDT** | `exit_ai_reversal_harvest ( 741_AI_PASS)` |
| #12 | **WLD/USDT:USDT** | 🟢 Long | `141 ` | 2026-10-25 15:40 | 6h 45m | **+19.30%** | **+47.82 USDT** | `exit_long_tc_d_3_2 ( 141 )` |
| #13 | **XRP/USDT:USDT** | 🔴 Short | `741_AI_PASS` | 2026-10-23 22:50 | 6h 10m | **+6.94%** | **+13.20 USDT** | `exit_ai_reversal_harvest ( 741_AI_PASS)` |
| #14 | **FET/USDT:USDT** | 🔴 Short | `741_AI_PASS` | 2026-10-23 19:25 | 2h 45m | **+5.67%** | **+10.79 USDT** | `exit_ai_reversal_harvest ( 741_AI_PASS)` |
| #15 | **BTW/USDT:USDT** | 🟢 Long | `2 ` | 2026-10-23 19:10 | 40m | **+38.38%** | **+54.77 USDT** | `exit_long_normal_d_7_1 ( 2 )` |

---
*Báo cáo được khởi tạo tự động bởi `scripts/export_report.py` phục vụ chu trình Tối ưu hóa Tự động Agentic AI.*
