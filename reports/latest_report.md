# 📈 Báo Cáo Đánh Giá Hiệu Suất Backtest Toàn Diện (Comprehensive Quantitative Report)

| Thông Tin Phiên Chạy | Chi Tiết | Đánh Dấu / Định Danh |
| :--- | :--- | :--- |
| 🏷️ **Phiên bản Chiến lược (Version)** | **`v10.0`** | `v10.0` |
| 🔖 **Git Commit** | `4659b4e` | `fix(colab): force git reset hard on main in Step 3 and set 240 days in daily_backtest.yml` |
| 🚀 **Đánh dấu lần chạy (Run Marker)** | **`v10.0-c4-240d`** | `Workflow #local` |
| 🤖 **Chiến lược (Strategy)** | `NostalgiaForInfinityX8_Combined_AI` | `Combined AI Engine` |
| 📅 **Thời gian đánh giá (Evaluation Date)** | `2026-11-15 02:18:27 UTC` | `UTC` |
| ⏱️ **Cửa sổ Backtest (Timerange)** | `20260317-20261112` | `237 ngày` |
| 📁 **Tệp kết quả (Source File)** | `backtest-result-2026-11-15_02-18-23.zip` | `Binance Futures 5m` |

---

## ⚖️ So Sánh Hiệu Suất Với Lần Backtest Trước (Benchmark Comparison)

| Chỉ số định lượng | Lần chạy này [v10.0-c4-240d - 4659b4e] | Lần trước [v10.0-c3-240d - 4659b4e] | Chênh lệch (Δ Delta) | Xu hướng |
| :--- | :--- | :--- | :--- | :--- |
| **Tỷ lệ thắng (Winrate)** | **96.72%** | **96.72%** | 0.00% | ⚪ Tương đương |
| **Lợi nhuận ròng (Net Profit %)** | **+2023.21%** | **+2463.13%** | `-439.92%` | 🔴 Suy giảm |
| **Lợi nhuận tuyệt đối (USDT)** | **+4,046.42 USDT** | **+4,926.26 USDT** | `-879.84 USDT` | 🔴 Suy giảm |
| **Hệ số Sharpe (Sharpe Ratio)** | **9.66** | **9.09** | `+0.57` | 🟢 Cải thiện |
| **Hệ số Sortino (Sortino Ratio)** | **4.94** | **4.32** | `+0.62` | 🟢 Cải thiện |
| **Sụt giảm tối đa (Max Drawdown %)** | **6.63%** | **7.42%** | `-0.79%` | 🟢 Cải thiện |
| **Hệ số lãi/lỗ (Profit Factor)** | **11.14** | **10.64** | `+0.50` | 🟢 Cải thiện |
| **Tổng số lệnh (Total Trades)** | **244** | **244** | 0.00 lệnh | ⚪ Tương đương |
| **Chuỗi lệnh thua dài nhất** | **1 trades** | **1 trades** | 0.00 lệnh | ⚪ Tương đương |
| **Kỳ vọng toán học (Expectancy)** | **16.5837** | **20.1896** | `-3.61` | 🔴 Suy giảm |
| **Hệ số Calmar (Calmar Ratio)** | **2459.43** | **2674.34** | `-214.91` | 🔴 Suy giảm |

---

## 🏛️ Ma Trận Lịch Sử Đối Soát Giữa Các Lần Chạy (Multi-Run Version History Matrix)

> *Bảng tổng hợp đối chiếu kết quả backtest qua từng phiên bản và lần chạy để tiện theo dõi tiến trình tối ưu hóa.*

| Đánh dấu lần chạy (Run Marker) | Phiên bản | Commit | Ngày chạy | Tỷ lệ thắng (Winrate) | Lợi nhuận ròng | Max DD % | Sharpe | Profit Factor | Tổng lệnh | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `v9.0-ed1b346` | **`v9.0`** | `ed1b346` | 20261107 | **95.40%** | +2,775.00 USDT (+1387.5%) | 16.83% | 8.96 | 4.67 | `261` | ⚪ Đã lưu |
| `Upstream_NFIX8_Merge_Eval` | **`v9.0`** | `96a8884` | 20261109 | **95.31%** | +2,605.18 USDT (+1302.6%) | 16.82% | 8.79 | 4.62 | `256` | ⚪ Đã lưu |
| `Upstream_v18_0_237_Eval` | **`v9.0`** | `8c68073` | 20261111 | **95.29%** | +2,589.67 USDT (+1294.8%) | 16.83% | 8.77 | 4.61 | `255` | ⚪ Đã lưu |
| `v9.0-baseline-240d` | **`v9.0`** | `4659b4e` | 20261115 | **96.41%** | +2,918.55 USDT (+1459.3%) | 7.85% | 9.56 | 9.52 | `251` | ⚪ Đã lưu |
| `v10.0-c1-240d` | **`v10.0`** | `4659b4e` | 20261115 | **95.49%** | +3,042.86 USDT (+1521.4%) | 7.11% | 8.79 | 7.23 | `244` | ⚪ Đã lưu |
| `v10.0-c2-240d` | **`v10.0`** | `4659b4e` | 20261115 | **96.71%** | +6,055.14 USDT (+3027.6%) | 7.72% | 8.76 | 10.38 | `243` | ⚪ Đã lưu |
| `v10.0-c3-240d` | **`v10.0`** | `4659b4e` | 20261115 | **96.72%** | +4,926.26 USDT (+2463.1%) | 7.42% | 9.09 | 10.64 | `244` | ⚪ Đã lưu |
| `v10.0-c4-240d` | **`v10.0`** | `4659b4e` | 20261115 | **96.72%** | +4,046.42 USDT (+2023.2%) | 6.63% | 9.66 | 11.14 | `244` | 🎯 **HIỆN TẠI** |

---

## 🎯 Chỉ Số Hiệu Suất Cốt Lõi (Executive Performance Metrics)

| Chỉ số định lượng | Giá trị thực tế | Đánh giá Benchmark | Tiêu chuẩn chất lượng |
| :--- | :--- | :--- | :--- |
| **Tỷ lệ thắng (Winrate)** | **96.72%** | 🟢 Robust | Ngưỡng an toàn >= 70% |
| **Hệ số Sharpe (Sharpe Ratio)** | **9.66** | 🟢 Exceptional | Chuẩn Alpha quỹ >= 2.0 |
| **Hệ số Sortino (Sortino Ratio)** | **4.94** | 🟢 Excellent | Đo lường rủi ro sụt giảm âm |
| **Sụt giảm tài khoản tối đa (Max Drawdown %)** | **6.63%** | 🟢 Defended | Giới hạn rủi ro < 15% |
| **Sụt giảm tuyệt đối (Max Drawdown Abs)** | **+301.60 USDT** | 🟢 Đã kiểm soát | Độ sâu drawdown danh mục |
| **Hệ số lãi/lỗ (Profit Factor)** | **11.14** | 🟢 High | Chuẩn định lượng >= 1.5 |
| **Chuỗi thua dài nhất (Longest Loss Streak)** | **1 trades** | 🟢 Safe | Kiểm soát chuỗi sụt giảm |

---

## 📊 Chỉ Số Định Lượng Mở Rộng (Secondary Quantitative Indicators)

| Chỉ số định lượng | Kết quả | Mô tả & Ý nghĩa kỹ thuật |
| :--- | :--- | :--- |
| **Tổng số lệnh (Total Trades)** | `244` | Tổng số lệnh đã hoàn tất trong timerange |
| **Tổng lệnh thắng / hòa / thua** | `236` thắng / `0` hòa / `8` thua | Phân bổ kết quả các giao dịch |
| **Lợi nhuận ròng % (Net Profit %)** | `+2023.21%` | Tỷ lệ tăng trưởng toàn bộ tài khoản |
| **Lợi nhuận tuyệt đối (Net Profit Abs)** | `+4,046.42 USDT` | Lợi nhuận bằng tiền mặt (USDT) |
| **Lợi nhuận trung bình / lệnh** | `+16.58 USDT` | Hiệu quả trung bình mỗi lần vào lệnh |
| **Mật độ giao dịch (Trades Per Day)** | `1.03 lệnh / ngày` | Tần suất giao dịch bình quân |
| **Kỳ vọng toán học (Expectancy)** | `16.5837` | Lợi nhuận kỳ vọng trên mỗi 1 đơn vị rủi ro |
| **Hệ số Calmar (Calmar Ratio)** | `2459.43` | Tỷ lệ lợi nhuận trên sụt giảm vốn tối đa |
| **Tốc độ tăng trưởng kép (CAGR)** | `10958.13%` | Compound Annual Growth Rate quy năm |

---

## ⚔️ Thống Kê Phân Bổ Vị Thế (Long vs Short Performance)

| Vị thế (Position) | Số lệnh | Tỷ trọng | Tỷ lệ thắng (Winrate) | Lợi nhuận (USDT) | Lợi nhuận (%) | Đánh giá |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 **Lệnh Mua (Long)** | `174` | 71.3% | **98.28%** | **+3,553.14 USDT** | +2470.69% | 🟢 Vượt trội |
| 🔴 **Lệnh Bán (Short)** | `70` | 28.7% | **92.86%** | **+493.29 USDT** | +320.56% | 🟢 Vượt trội |
| 🌐 **Toàn bộ danh mục** | `244` | 100.0% | **96.72%** | **+4,046.42 USDT** | +2023.21% | 🎯 Hoàn tất |

## 🚪 Phân Tích Lý Do Thoát Lệnh (Exit Reason Breakdown)

| Lý do đóng lệnh (Exit Reason) | Số lệnh | Tỷ trọng | Tỷ lệ thắng (Winrate) | Lợi nhuận (USDT) |
| :--- | :--- | :--- | :--- | :--- |
| `TOTAL` | `244` | 100.0% | **96.7%** | +4,046.42 USDT |
| `exit_profit_long_rebuy_t_0_1_m ( 64 )` | `13` | 5.3% | **100.0%** | +80.60 USDT |
| `exit_ai_reversal_harvest ( 702 703 731_AI_PASS)` | `12` | 4.9% | **100.0%** | +60.45 USDT |
| `exit_short_adaptive_trailing_scalp ( 562 )` | `9` | 3.7% | **100.0%** | +105.82 USDT |
| `exit_profit_long_tc_t_0_1_m ( 142 )` | `7` | 2.9% | **100.0%** | +13.25 USDT |
| `exit_short_adaptive_trailing_scalp ( 702 703 731_AI_PASS)` | `6` | 2.5% | **100.0%** | +27.04 USDT |
| `exit_long_rebuy_d_6_1 ( 64 )` | `5` | 2.0% | **100.0%** | +385.56 USDT |
| `exit_short_adaptive_trailing_mid ( 562 )` | `4` | 1.6% | **100.0%** | +93.89 USDT |
| `exit_long_rebuy_e_r ( 65 )` | `4` | 1.6% | **100.0%** | +76.94 USDT |
| `exit_profit_long_tc_t_0_1_m ( 143 )` | `4` | 1.6% | **100.0%** | +12.96 USDT |
| `exit_long_quick_q_9 ( 44 )` | `3` | 1.2% | **100.0%** | +123.76 USDT |
| `exit_long_normal_u_1 ( 2 )` | `3` | 1.2% | **100.0%** | +24.94 USDT |
| `exit_profit_long_tc_t_1_1_m ( 145 )` | `3` | 1.2% | **100.0%** | +23.73 USDT |
| `exit_ai_reversal_harvest ( 702 703 731 743_AI_PASS)` | `3` | 1.2% | **100.0%** | +20.05 USDT |
| `exit_profit_long_tc_t_0_1_m ( 145 )` | `3` | 1.2% | **100.0%** | +15.13 USDT |
| `exit_profit_long_rebuy_t_0_1_m ( 61 )` | `3` | 1.2% | **100.0%** | +9.91 USDT |
| `exit_profit_long_tc_t_0_1_m ( 144 )` | `3` | 1.2% | **100.0%** | +8.86 USDT |
| `force_exit` | `3` | 1.2% | **33.3%** | -151.89 USDT |
| `exit_long_normal_d_4_1 ( 2 )` | `2` | 0.8% | **100.0%** | +184.88 USDT |
| `exit_long_normal_d_7_1 ( 2 )` | `2` | 0.8% | **100.0%** | +164.21 USDT |
| `exit_long_rebuy_d_4_1 ( 65 )` | `2` | 0.8% | **100.0%** | +113.33 USDT |
| `exit_long_rebuy_d_4_1 ( 64 )` | `2` | 0.8% | **100.0%** | +60.92 USDT |
| `exit_long_normal_d_6_1 ( 2 )` | `2` | 0.8% | **100.0%** | +43.53 USDT |
| `exit_long_tc_d_6_1 ( 144 )` | `2` | 0.8% | **100.0%** | +37.41 USDT |
| `exit_profit_long_tc_t_0_1_m ( 141 142 )` | `2` | 0.8% | **100.0%** | +32.33 USDT |
| `exit_ai_reversal_harvest ( 721 724 742_AI_PASS)` | `2` | 0.8% | **100.0%** | +31.55 USDT |
| `exit_long_tc_u_1 ( 141 )` | `2` | 0.8% | **100.0%** | +29.80 USDT |
| `exit_long_tc_d_6_1 ( 142 )` | `2` | 0.8% | **100.0%** | +24.44 USDT |
| `exit_long_rapid_rpd_2 ( 102 )` | `2` | 0.8% | **100.0%** | +24.21 USDT |
| `exit_short_adaptive_trailing_scalp ( 542 )` | `2` | 0.8% | **100.0%** | +21.24 USDT |
| `exit_short_adaptive_trailing_mid ( 542 )` | `2` | 0.8% | **100.0%** | +19.21 USDT |
| `exit_long_tc_d_5_1 ( 141 142 )` | `2` | 0.8% | **100.0%** | +16.12 USDT |
| `exit_profit_long_scalp_t_1_1_m ( 163 )` | `2` | 0.8% | **100.0%** | +11.34 USDT |
| `exit_profit_long_tc_t_0_1_m ( 141 )` | `2` | 0.8% | **100.0%** | +8.69 USDT |
| `exit_profit_long_rebuy_t_0_1_m ( 62 )` | `2` | 0.8% | **100.0%** | +5.13 USDT |
| `exit_profit_long_normal_t_0_1_m ( 3 )` | `2` | 0.8% | **100.0%** | +2.91 USDT |
| `exit_profit_long_scalp_t_0_1_m ( 163 )` | `2` | 0.8% | **100.0%** | +2.64 USDT |
| `exit_short_adaptive_trailing_scalp ( 703 731 745_AI_PASS)` | `2` | 0.8% | **100.0%** | +2.31 USDT |
| `exit_ai_profit_lock ( 721 724 745_AI_PASS)` | `2` | 0.8% | **100.0%** | +2.02 USDT |
| `exit_ai_drift_decay ( 702 703 731_AI_PASS)` | `2` | 0.8% | **0.0%** | -7.44 USDT |
| `exit_long_quick_d_11_1 ( 43 )` | `1` | 0.4% | **100.0%** | +157.85 USDT |
| `exit_long_rebuy_d_7_1 ( 64 )` | `1` | 0.4% | **100.0%** | +153.70 USDT |
| `exit_long_rebuy_d_6_1 ( 62 )` | `1` | 0.4% | **100.0%** | +144.60 USDT |
| `exit_long_rebuy_2_1_1 ( 64 )` | `1` | 0.4% | **100.0%** | +121.55 USDT |
| `exit_long_normal_d_6_1 ( 1 )` | `1` | 0.4% | **100.0%** | +118.27 USDT |
| `exit_long_tc_d_3_2 ( 141 )` | `1` | 0.4% | **100.0%** | +111.01 USDT |
| `exit_long_quick_q_6 ( 42 )` | `1` | 0.4% | **100.0%** | +106.43 USDT |
| `exit_long_rapid_d_5_1 ( 103 )` | `1` | 0.4% | **100.0%** | +89.67 USDT |
| `exit_long_normal_d_6_1 ( 3 )` | `1` | 0.4% | **100.0%** | +86.04 USDT |
| `exit_long_normal_d_7_1 ( 6 )` | `1` | 0.4% | **100.0%** | +74.52 USDT |
| `exit_long_tc_d_8_1 ( 142 )` | `1` | 0.4% | **100.0%** | +71.12 USDT |
| `exit_long_tc_d_3_1 ( 141 )` | `1` | 0.4% | **100.0%** | +64.64 USDT |
| `exit_long_normal_d_4_1 ( 6 )` | `1` | 0.4% | **100.0%** | +62.69 USDT |
| `exit_long_quick_q_6 ( 44 )` | `1` | 0.4% | **100.0%** | +60.05 USDT |
| `exit_long_rebuy_d_8_1 ( 64 )` | `1` | 0.4% | **100.0%** | +55.00 USDT |
| `exit_short_adaptive_trailing_mega ( 562 )` | `1` | 0.4% | **100.0%** | +49.43 USDT |
| `exit_long_tc_3_1_1 ( 141 142 )` | `1` | 0.4% | **100.0%** | +47.14 USDT |
| `exit_long_scalp_d_5_1 ( 163 )` | `1` | 0.4% | **100.0%** | +38.34 USDT |
| `exit_long_normal_u_3 ( 6 141 )` | `1` | 0.4% | **100.0%** | +35.95 USDT |
| `exit_long_rebuy_d_9_1 ( 65 )` | `1` | 0.4% | **100.0%** | +35.21 USDT |
| `exit_ai_reversal_harvest ( 721 724 745_AI_PASS)` | `1` | 0.4% | **100.0%** | +35.01 USDT |
| `exit_profit_long_quick_t_1_1_m ( 43 )` | `1` | 0.4% | **100.0%** | +33.99 USDT |
| `exit_long_normal_8_1_1 ( 1 )` | `1` | 0.4% | **100.0%** | +25.14 USDT |
| `exit_long_normal_u_1 ( 1 )` | `1` | 0.4% | **100.0%** | +24.81 USDT |
| `exit_profit_long_tc_t_2_1_m ( 142 )` | `1` | 0.4% | **100.0%** | +24.55 USDT |
| `exit_profit_long_rebuy_t_7_1_m ( 63 )` | `1` | 0.4% | **100.0%** | +23.59 USDT |
| `exit_long_tc_u_1 ( 141 142 )` | `1` | 0.4% | **100.0%** | +22.62 USDT |
| `exit_long_tc_u_1 ( 142 )` | `1` | 0.4% | **100.0%** | +21.70 USDT |
| `exit_long_quick_q_6 ( 47 )` | `1` | 0.4% | **100.0%** | +21.56 USDT |
| `exit_profit_long_tc_t_2_1_m ( 145 )` | `1` | 0.4% | **100.0%** | +20.86 USDT |
| `exit_long_scalp_d_6_1 ( 61 162 )` | `1` | 0.4% | **100.0%** | +19.79 USDT |
| `exit_long_rebuy_d_6_1 ( 63 )` | `1` | 0.4% | **100.0%** | +19.28 USDT |
| `exit_long_quick_d_7_1 ( 42 )` | `1` | 0.4% | **100.0%** | +19.27 USDT |
| `exit_long_rebuy_d_8_1 ( 61 )` | `1` | 0.4% | **100.0%** | +19.13 USDT |
| `exit_long_rebuy_d_6_1 ( 61 )` | `1` | 0.4% | **100.0%** | +18.56 USDT |
| `exit_profit_long_quick_t_2_1_m ( 46 )` | `1` | 0.4% | **100.0%** | +17.87 USDT |
| `exit_long_scalp_d_6_1 ( 162 )` | `1` | 0.4% | **100.0%** | +17.54 USDT |
| `exit_profit_long_tc_t_1_1_m ( 141 142 )` | `1` | 0.4% | **100.0%** | +17.04 USDT |
| `exit_profit_long_normal_t_2_1_m ( 3 )` | `1` | 0.4% | **100.0%** | +17.00 USDT |
| `exit_long_normal_d_3_2 ( 5 )` | `1` | 0.4% | **100.0%** | +16.68 USDT |
| `exit_long_tc_d_6_1 ( 141 )` | `1` | 0.4% | **100.0%** | +16.17 USDT |
| `exit_profit_long_tc_t_1_1_m ( 141 )` | `1` | 0.4% | **100.0%** | +14.47 USDT |
| `exit_long_tc_d_6_1 ( 141 143 163 )` | `1` | 0.4% | **100.0%** | +14.43 USDT |
| `exit_short_adaptive_trailing_scalp ( 702 703 705 731_AI_PASS)` | `1` | 0.4% | **100.0%** | +14.10 USDT |
| `exit_long_tc_d_5_1 ( 145 )` | `1` | 0.4% | **100.0%** | +13.53 USDT |
| `exit_long_rebuy_d_5_1 ( 63 )` | `1` | 0.4% | **100.0%** | +13.36 USDT |
| `exit_ai_profit_lock ( 703 721 724 731_AI_PASS)` | `1` | 0.4% | **100.0%** | +12.50 USDT |
| `exit_profit_long_rebuy_t_2_1_m ( 65 )` | `1` | 0.4% | **100.0%** | +12.29 USDT |
| `exit_long_normal_u_4 ( 1 61 )` | `1` | 0.4% | **100.0%** | +11.82 USDT |
| `exit_profit_long_normal_t_0_1_m ( 2 )` | `1` | 0.4% | **100.0%** | +11.80 USDT |
| `exit_long_tc_d_5_1 ( 62 144 )` | `1` | 0.4% | **100.0%** | +11.25 USDT |
| `exit_profit_long_normal_t_1_1_m ( 3 )` | `1` | 0.4% | **100.0%** | +11.06 USDT |
| `exit_short_rebuy_1_1_1 ( 562 )` | `1` | 0.4% | **100.0%** | +10.42 USDT |
| `exit_long_rebuy_d_10_1 ( 62 )` | `1` | 0.4% | **100.0%** | +10.15 USDT |
| `exit_profit_long_rebuy_t_3_1_m ( 61 )` | `1` | 0.4% | **100.0%** | +9.98 USDT |
| `exit_long_normal_d_5_1 ( 2 )` | `1` | 0.4% | **100.0%** | +9.61 USDT |
| `exit_profit_long_rapid_t_1_1_m ( 102 )` | `1` | 0.4% | **100.0%** | +9.29 USDT |
| `exit_long_tc_d_4_2 ( 145 )` | `1` | 0.4% | **100.0%** | +9.07 USDT |
| `exit_long_normal_d_2_1 ( 1 )` | `1` | 0.4% | **100.0%** | +8.76 USDT |
| `exit_long_tc_d_3_2 ( 102 142 )` | `1` | 0.4% | **100.0%** | +8.18 USDT |
| `exit_long_tc_d_5_1 ( 144 )` | `1` | 0.4% | **100.0%** | +7.64 USDT |
| `exit_profit_long_normal_t_0_1_m ( 5 )` | `1` | 0.4% | **100.0%** | +7.60 USDT |
| `exit_long_tc_d_3_2 ( 142 )` | `1` | 0.4% | **100.0%** | +7.42 USDT |
| `exit_long_normal_d_6_1 ( 2 141 )` | `1` | 0.4% | **100.0%** | +7.25 USDT |
| `exit_long_rapid_rpd_6 ( 102 )` | `1` | 0.4% | **100.0%** | +6.75 USDT |
| `exit_long_normal_d_5_1 ( 6 102 141 )` | `1` | 0.4% | **100.0%** | +6.70 USDT |
| `exit_long_normal_d_5_1 ( 5 )` | `1` | 0.4% | **100.0%** | +6.47 USDT |
| `exit_long_tc_d_5_1 ( 142 )` | `1` | 0.4% | **100.0%** | +6.27 USDT |
| `exit_long_quick_q_2 ( 41 )` | `1` | 0.4% | **100.0%** | +6.24 USDT |
| `exit_long_normal_d_8_1 ( 4 )` | `1` | 0.4% | **100.0%** | +6.10 USDT |
| `exit_profit_long_rebuy_t_1_1_m ( 62 )` | `1` | 0.4% | **100.0%** | +5.96 USDT |
| `exit_profit_long_rebuy_t_2_1_m ( 62 )` | `1` | 0.4% | **100.0%** | +5.91 USDT |
| `exit_profit_long_normal_t_0_1_m ( 6 102 )` | `1` | 0.4% | **100.0%** | +5.84 USDT |
| `exit_ai_profit_lock ( 702 703 731_AI_PASS)` | `1` | 0.4% | **100.0%** | +5.51 USDT |
| `exit_profit_long_tc_t_3_1_m ( 143 )` | `1` | 0.4% | **100.0%** | +5.36 USDT |
| `exit_long_rebuy_u_1 ( 61 )` | `1` | 0.4% | **100.0%** | +5.32 USDT |
| `exit_ai_reversal_harvest ( 721 724 741 745_AI_PASS)` | `1` | 0.4% | **100.0%** | +5.03 USDT |
| `exit_ai_reversal_harvest ( 721 742_AI_PASS)` | `1` | 0.4% | **100.0%** | +3.88 USDT |
| `exit_long_normal_u_2 ( 4 41 61 )` | `1` | 0.4% | **100.0%** | +3.82 USDT |
| `exit_ai_reversal_harvest ( 745_AI_PASS)` | `1` | 0.4% | **100.0%** | +3.76 USDT |
| `exit_long_normal_u_2 ( 2 )` | `1` | 0.4% | **100.0%** | +3.66 USDT |
| `exit_ai_reversal_harvest ( 703 731 745_AI_PASS)` | `1` | 0.4% | **100.0%** | +3.42 USDT |
| `exit_long_quick_u_1 ( 43 )` | `1` | 0.4% | **100.0%** | +3.04 USDT |
| `exit_profit_long_rebuy_t_2_1_m ( 64 )` | `1` | 0.4% | **100.0%** | +2.73 USDT |
| `exit_short_adaptive_trailing_mid ( 702 703 731_AI_PASS)` | `1` | 0.4% | **100.0%** | +2.53 USDT |
| `exit_profit_long_scalp_t_2_1_m ( 163 )` | `1` | 0.4% | **100.0%** | +2.31 USDT |
| `exit_long_tc_u_1 ( 141 143 )` | `1` | 0.4% | **100.0%** | +2.26 USDT |
| `exit_profit_long_normal_t_2_1_m ( 2 63 101 )` | `1` | 0.4% | **100.0%** | +2.12 USDT |
| `exit_ai_reversal_harvest ( 702 703 724 731_AI_PASS)` | `1` | 0.4% | **100.0%** | +1.92 USDT |
| `exit_profit_long_quick_t_1_1_m ( 42 )` | `1` | 0.4% | **100.0%** | +1.90 USDT |
| `exit_ai_profit_lock ( 745_AI_PASS)` | `1` | 0.4% | **100.0%** | +1.82 USDT |
| `exit_long_tc_u_1 ( 144 )` | `1` | 0.4% | **100.0%** | +1.67 USDT |
| `exit_short_adaptive_trailing_scalp ( 721 724 742_AI_PASS)` | `1` | 0.4% | **100.0%** | +1.60 USDT |
| `exit_short_adaptive_trailing_scalp ( 703 705 706 731_AI_PASS)` | `1` | 0.4% | **100.0%** | +1.59 USDT |
| `exit_ai_profit_lock ( 721 724 742_AI_PASS)` | `1` | 0.4% | **100.0%** | +1.53 USDT |
| `exit_profit_long_rapid_t_0_1_m ( 102 )` | `1` | 0.4% | **100.0%** | +1.52 USDT |
| `exit_ai_reversal_harvest ( 724 742_AI_PASS)` | `1` | 0.4% | **100.0%** | +1.43 USDT |
| `exit_profit_long_quick_t_0_1_m ( 43 )` | `1` | 0.4% | **100.0%** | +1.36 USDT |
| `exit_profit_long_scalp_t_0_1_m ( 162 )` | `1` | 0.4% | **100.0%** | +1.33 USDT |
| `exit_profit_long_scalp_t_0_1_m ( 161 )` | `1` | 0.4% | **100.0%** | +1.15 USDT |
| `exit_short_adaptive_trailing_scalp ( 702 703 731 743_AI_PASS)` | `1` | 0.4% | **100.0%** | +1.09 USDT |
| `exit_short_adaptive_trailing_scalp ( 745_AI_PASS)` | `1` | 0.4% | **100.0%** | +1.03 USDT |
| `exit_profit_long_normal_t_0_1_m ( 3 142 )` | `1` | 0.4% | **100.0%** | +0.98 USDT |
| `exit_short_adaptive_trailing_scalp ( 724 745_AI_PASS)` | `1` | 0.4% | **100.0%** | +0.85 USDT |
| `exit_long_normal_d_7_1 ( 2 101 141 )` | `1` | 0.4% | **100.0%** | +0.70 USDT |
| `exit_ai_profit_lock ( 703 705 706 731_AI_PASS)` | `1` | 0.4% | **100.0%** | +0.54 USDT |
| `exit_long_tc_d_1_1 ( 141 )` | `1` | 0.4% | **100.0%** | +0.38 USDT |
| `exit_long_normal_u_1 ( 2 6 )` | `1` | 0.4% | **100.0%** | +0.27 USDT |
| `exit_ai_562_aged_breakeven ( 562 )` | `1` | 0.4% | **0.0%** | -7.28 USDT |
| `exit_short_universal_structural_cut ( 562 )` | `1` | 0.4% | **0.0%** | -14.90 USDT |
| `exit_hard_preemptive_liquidation_guard ( 120 )` | `1` | 0.4% | **0.0%** | -25.96 USDT |
| `exit_hard_preemptive_liquidation_guard ( 4 )` | `1` | 0.4% | **0.0%** | -184.18 USDT |

## 🔍 Bảng Phân Tích Đầy Đủ Tất Cả Các Entry Tags (Full Enter Tag Breakdown)

> *Bảng tổng hợp chi tiết 100% tất cả các tag tín hiệu vào lệnh (Entry Tags) đã hoạt động trong phiên backtest.*

| Enter Tag | Vị thế | Số lệnh | Tỷ lệ thắng (Winrate) | Thắng/Hòa/Thua | Tổng LN % | Tổng LN (USDT) | LN TB/Lệnh | Thời lượng TB | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `TOTAL` | 🟢 Long Core | `244` | **96.7%** | 236/0/8 | +2023.21% | **+4,046.42 USDT** | +11.44% | 8:46:00 | 🟢 Tối ưu |
| `64` | 🟢 Long Core | `24` | **100.0%** | 24/0/0 | +430.02% | **+860.04 USDT** | +17.16% | 8:17:00 | 🟢 Tối ưu |
| `2` | 🟢 Long Core | `12` | **100.0%** | 12/0/0 | +221.32% | **+442.65 USDT** | +20.29% | 2:08:00 | 🟢 Tối ưu |
| `141` | 🟢 Long Core | `9` | **100.0%** | 9/0/0 | +122.58% | **+245.16 USDT** | +10.94% | 9:33:00 | 🟢 Tối ưu |
| `65` | 🟢 Long Core | `8` | **100.0%** | 8/0/0 | +118.89% | **+237.78 USDT** | +19.27% | 2:26:00 | 🟢 Tối ưu |
| `562` | 🟢 Long Core | `18` | **83.3%** | 15/0/3 | +108.87% | **+217.73 USDT** | +4.95% | 23:52:00 | 🟢 Tối ưu |
| `43` | 🟢 Long Core | `4` | **100.0%** | 4/0/0 | +98.12% | **+196.25 USDT** | +21.31% | 0:48:00 | 🟢 Tối ưu |
| `44` | 🟢 Long Core | `5` | **100.0%** | 5/0/0 | +95.61% | **+191.22 USDT** | +16.39% | 2:41:00 | 🟢 Tối ưu |
| `1` | 🟢 Long Core | `4` | **100.0%** | 4/0/0 | +88.49% | **+176.98 USDT** | +12.38% | 2 days, 7:31:00 | 🟢 Tối ưu |
| `62` | 🟢 Long Core | `6` | **100.0%** | 6/0/0 | +85.87% | **+171.74 USDT** | +9.33% | 17:46:00 | 🟢 Tối ưu |
| `142` | 🟢 Long Core | `14` | **100.0%** | 14/0/0 | +84.37% | **+168.75 USDT** | +12.83% | 8:12:00 | 🟢 Tối ưu |
| `6` | 🟢 Long Core | `2` | **100.0%** | 2/0/0 | +68.60% | **+137.21 USDT** | +26.50% | 16:15:00 | 🟢 Tối ưu |
| `141 142` | 🟢 Long Core | `7` | **100.0%** | 7/0/0 | +67.63% | **+135.26 USDT** | +12.50% | 8:41:00 | 🟢 Tối ưu |
| `42` | 🟢 Long Core | `3` | **100.0%** | 3/0/0 | +63.79% | **+127.59 USDT** | +22.44% | 1:15:00 | 🟢 Tối ưu |
| `3` | 🟢 Long Core | `5` | **100.0%** | 5/0/0 | +58.51% | **+117.02 USDT** | +10.75% | 3:02:00 | 🟢 Tối ưu |
| `103` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +44.83% | **+89.67 USDT** | +25.41% | 2:30:00 | 🟢 Tối ưu |
| `702 703 731_AI_PASS` | 🤖 Short AI Gatekeeper | `22` | **90.9%** | 20/0/2 | +44.04% | **+88.09 USDT** | +4.10% | 4:05:00 | 🟢 Tối ưu |
| `145` | 🟢 Long Core | `9` | **100.0%** | 9/0/0 | +41.16% | **+82.32 USDT** | +10.60% | 8:46:00 | 🟢 Tối ưu |
| `61` | 🟢 Long Core | `7` | **100.0%** | 7/0/0 | +31.45% | **+62.90 USDT** | +16.25% | 1:54:00 | 🟢 Tối ưu |
| `63` | 🟢 Long Core | `3` | **100.0%** | 3/0/0 | +28.12% | **+56.23 USDT** | +33.10% | 3:02:00 | 🟢 Tối ưu |
| `144` | 🟢 Long Core | `7` | **100.0%** | 7/0/0 | +27.79% | **+55.58 USDT** | +14.95% | 14:22:00 | 🟢 Tối ưu |
| `163` | 🟢 Long Core | `6` | **100.0%** | 6/0/0 | +27.31% | **+54.62 USDT** | +9.34% | 2:25:00 | 🟢 Tối ưu |
| `102` | 🟢 Long Core | `5` | **100.0%** | 5/0/0 | +20.89% | **+41.77 USDT** | +5.08% | 2:58:00 | 🟢 Tối ưu |
| `542` | 🟢 Long Core | `4` | **100.0%** | 4/0/0 | +20.22% | **+40.45 USDT** | +6.46% | 0:45:00 | 🟢 Tối ưu |
| `721 724 745_AI_PASS` | 🤖 Short AI Gatekeeper | `3` | **100.0%** | 3/0/0 | +18.51% | **+37.03 USDT** | +3.24% | 2:02:00 | 🟢 Tối ưu |
| `6 141` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +17.97% | **+35.95 USDT** | +16.21% | 19:20:00 | 🟢 Tối ưu |
| `721 724 742_AI_PASS` | 🤖 Short AI Gatekeeper | `4` | **100.0%** | 4/0/0 | +17.34% | **+34.68 USDT** | +4.15% | 1:35:00 | 🟢 Tối ưu |
| `5` | 🟢 Long Core | `3` | **100.0%** | 3/0/0 | +15.37% | **+30.75 USDT** | +14.95% | 3:00:00 | 🟢 Tối ưu |
| `47` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +10.78% | **+21.56 USDT** | +13.38% | 1 day, 2:00:00 | 🟢 Tối ưu |
| `702 703 731 743_AI_PASS` | 🤖 Short AI Gatekeeper | `4` | **100.0%** | 4/0/0 | +10.57% | **+21.15 USDT** | +5.44% | 2:08:00 | 🟢 Tối ưu |
| `61 162` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +9.89% | **+19.79 USDT** | +32.22% | 4:05:00 | 🟢 Tối ưu |
| `162` | 🟢 Long Core | `2` | **100.0%** | 2/0/0 | +9.44% | **+18.88 USDT** | +17.33% | 0:52:00 | 🟢 Tối ưu |
| `143` | 🟢 Long Core | `5` | **100.0%** | 5/0/0 | +9.16% | **+18.32 USDT** | +5.30% | 18:36:00 | 🟢 Tối ưu |
| `46` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +8.94% | **+17.87 USDT** | +11.97% | 0:45:00 | 🟢 Tối ưu |
| `141 143 163` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +7.21% | **+14.43 USDT** | +33.41% | 1:30:00 | 🟢 Tối ưu |
| `702 703 705 731_AI_PASS` | 🤖 Short AI Gatekeeper | `1` | **100.0%** | 1/0/0 | +7.05% | **+14.10 USDT** | +3.68% | 7:50:00 | 🟢 Tối ưu |
| `703 721 724 731_AI_PASS` | 🤖 Short AI Gatekeeper | `1` | **100.0%** | 1/0/0 | +6.25% | **+12.50 USDT** | +2.29% | 0:15:00 | 🟢 Tối ưu |
| `1 61` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +5.91% | **+11.82 USDT** | +21.38% | 0:15:00 | 🟢 Tối ưu |
| `62 144` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +5.63% | **+11.25 USDT** | +25.85% | 1:25:00 | 🟢 Tối ưu |
| `102 142` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +4.09% | **+8.18 USDT** | +19.97% | 1:40:00 | 🟢 Tối ưu |
| `2 141` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +3.62% | **+7.25 USDT** | +30.19% | 2:15:00 | 🟢 Tối ưu |
| `6 102 141` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +3.35% | **+6.70 USDT** | +26.17% | 1:00:00 | 🟢 Tối ưu |
| `745_AI_PASS` | 🤖 Short AI Gatekeeper | `3` | **100.0%** | 3/0/0 | +3.30% | **+6.60 USDT** | +4.18% | 2:30:00 | 🟢 Tối ưu |
| `41` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +3.12% | **+6.24 USDT** | +11.69% | 5:00:00 | 🟢 Tối ưu |
| `6 102` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +2.92% | **+5.84 USDT** | +1.43% | 2:05:00 | 🟢 Tối ưu |
| `703 731 745_AI_PASS` | 🤖 Short AI Gatekeeper | `3` | **100.0%** | 3/0/0 | +2.86% | **+5.72 USDT** | +4.98% | 3:43:00 | 🟢 Tối ưu |
| `721 724 741 745_AI_PASS` | 🤖 Short AI Gatekeeper | `1` | **100.0%** | 1/0/0 | +2.52% | **+5.03 USDT** | +5.62% | 7:15:00 | 🟢 Tối ưu |
| `721 742_AI_PASS` | 🤖 Short AI Gatekeeper | `1` | **100.0%** | 1/0/0 | +1.94% | **+3.88 USDT** | +4.99% | 3:30:00 | 🟢 Tối ưu |
| `4 41 61` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +1.91% | **+3.82 USDT** | +11.78% | 0:10:00 | 🟢 Tối ưu |
| `141 143` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +1.13% | **+2.26 USDT** | +5.57% | 0:05:00 | 🟢 Tối ưu |
| `703 705 706 731_AI_PASS` | 🤖 Short AI Gatekeeper | `2` | **100.0%** | 2/0/0 | +1.06% | **+2.13 USDT** | +3.69% | 3:32:00 | 🟢 Tối ưu |
| `2 63 101` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +1.06% | **+2.12 USDT** | +10.72% | 2:55:00 | 🟢 Tối ưu |
| `702 703 724 731_AI_PASS` | 🤖 Short AI Gatekeeper | `1` | **100.0%** | 1/0/0 | +0.96% | **+1.92 USDT** | +6.18% | 0:30:00 | 🟢 Tối ưu |
| `724 742_AI_PASS` | 🤖 Short AI Gatekeeper | `1` | **100.0%** | 1/0/0 | +0.71% | **+1.43 USDT** | +4.95% | 4:10:00 | 🟢 Tối ưu |
| `161` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +0.57% | **+1.15 USDT** | +1.56% | 12:05:00 | 🟢 Tối ưu |
| `3 142` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +0.49% | **+0.98 USDT** | +3.03% | 1 day, 20:25:00 | 🟢 Tối ưu |
| `724 745_AI_PASS` | 🤖 Short AI Gatekeeper | `1` | **100.0%** | 1/0/0 | +0.42% | **+0.85 USDT** | +4.84% | 0:30:00 | 🟢 Tối ưu |
| `2 101 141` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +0.35% | **+0.70 USDT** | +36.21% | 1:00:00 | 🟢 Tối ưu |
| `2 6` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +0.13% | **+0.27 USDT** | +7.15% | 0:15:00 | 🟢 Tối ưu |
| `120` | 🟢 Long Core | `1` | **0.0%** | 0/0/1 | -12.98% | **-25.96 USDT** | -50.11% | 6 days, 9:45:00 | 🔴 Cần tinh chỉnh |
| `3 6` | 🟢 Long Core | `1` | **0.0%** | 0/0/1 | -69.82% | **-139.64 USDT** | -29.06% | 3:05:00 | 🔴 Cần tinh chỉnh |
| `4` | 🟢 Long Core | `2` | **50.0%** | 1/0/1 | -89.04% | **-178.08 USDT** | -8.95% | 12:05:00 | 🔴 Cần tinh chỉnh |

---

## 📑 Chi Tiết Các Lệnh Giao Dịch (Trade Execution Journal)

### 🥇 Top 10 Lệnh Lãi Cao Nhất (Top Winning Trades)
| # | Cặp giao dịch | Vị thế | Enter Tag | Thời gian Mở ➔ Đóng | Thời lượng | Lợi nhuận % | Lợi nhuận USDT | Lý do thoát |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| #1 | **BTW/USDT:USDT** | 🟢 Long | `43 ` | 2026-10-05 06:45 ➔ 2026-10-05 08:05 | 1h 20m | **+71.12%** | **+157.85 USDT** | `exit_long_quick_d_11_1 ( 43 )` |
| #2 | **BTW/USDT:USDT** | 🟢 Long | `2 ` | 2026-10-23 18:30 ➔ 2026-10-23 19:10 | 40m | **+38.38%** | **+154.04 USDT** | `exit_long_normal_d_7_1 ( 2 )` |
| #3 | **BAT/USDT:USDT** | 🟢 Long | `64 ` | 2026-10-08 08:20 ➔ 2026-10-09 06:05 | 21h 45m | **+43.38%** | **+153.70 USDT** | `exit_long_rebuy_d_7_1 ( 64 )` |
| #4 | **GRASS/USDT:USDT** | 🟢 Long | `62 ` | 2026-10-14 17:45 ➔ 2026-10-15 15:05 | 21h 20m | **+33.86%** | **+144.60 USDT** | `exit_long_rebuy_d_6_1 ( 62 )` |
| #5 | **ARB/USDT:USDT** | 🟢 Long | `64 ` | 2026-09-17 21:45 ➔ 2026-09-18 01:50 | 4h 5m | **+59.20%** | **+121.55 USDT** | `exit_long_rebuy_2_1_1 ( 64 )` |
| #6 | **BTW/USDT:USDT** | 🟢 Long | `1 ` | 2026-10-22 20:45 ➔ 2026-10-22 21:40 | 55m | **+30.41%** | **+118.27 USDT** | `exit_long_normal_d_6_1 ( 1 )` |
| #7 | **WLD/USDT:USDT** | 🟢 Long | `141 ` | 2026-10-25 08:55 ➔ 2026-10-25 15:40 | 6h 45m | **+19.30%** | **+111.01 USDT** | `exit_long_tc_d_3_2 ( 141 )` |
| #8 | **STBL/USDT:USDT** | 🟢 Long | `42 ` | 2026-10-18 10:50 ➔ 2026-10-18 12:50 | 2h 0m | **+24.42%** | **+106.43 USDT** | `exit_long_quick_q_6 ( 42 )` |
| #9 | **GRASS/USDT:USDT** | 🟢 Long | `64 ` | 2026-10-05 14:55 ➔ 2026-10-05 19:15 | 4h 20m | **+32.17%** | **+105.77 USDT** | `exit_long_rebuy_d_6_1 ( 64 )` |
| #10 | **QNT/USDT:USDT** | 🟢 Long | `2 ` | 2026-10-13 11:10 ➔ 2026-10-13 18:40 | 7h 30m | **+24.34%** | **+98.28 USDT** | `exit_long_normal_d_4_1 ( 2 )` |

### ⚠️ Top Lệnh Thua Lỗ / Sụt Giảm Lớn Nhất (Top Drawdown Trades)
| # | Cặp giao dịch | Vị thế | Enter Tag | Thời gian Mở ➔ Đóng | Thời lượng | Thua lỗ % | Thua lỗ USDT | Lý do thoát |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| #1 | **SNXX/USDT:USDT** | 🟢 Long | `4 ` | 2026-11-04 15:45 ➔ 2026-11-05 14:45 | 23h 0m | **-62.11%** | **-184.18 USDT** | `exit_hard_preemptive_liquidation_guard ( 4 )` |
| #2 | **SNXX/USDT:USDT** | 🟢 Long | `3 6 ` | 2026-11-05 20:50 ➔ 2026-11-05 23:55 | 3h 5m | **-29.06%** | **-139.64 USDT** | `force_exit` |
| #3 | **RENDER/USDT:USDT** | 🟢 Long | `120 ` | 2026-06-04 01:20 ➔ 2026-06-10 11:05 | 153h 45m | **-50.11%** | **-25.96 USDT** | `exit_hard_preemptive_liquidation_guard ( 120 )` |
| #4 | **1000SHIB/USDT:USDT** | 🔴 Short | `562 ` | 2026-11-05 23:10 ➔ 2026-11-05 23:55 | 45m | **-3.18%** | **-19.65 USDT** | `force_exit` |
| #5 | **CRCL/USDT:USDT** | 🔴 Short | `562 ` | 2026-06-17 11:10 ➔ 2026-06-17 15:50 | 4h 40m | **-23.74%** | **-14.90 USDT** | `exit_short_universal_structural_cut ( 562 )` |
| #6 | **QNT/USDT:USDT** | 🔴 Short | `562 ` | 2026-08-03 08:30 ➔ 2026-08-04 20:30 | 36h 0m | **-6.71%** | **-7.28 USDT** | `exit_ai_562_aged_breakeven ( 562 )` |
| #7 | **ETH/USDT:USDT** | 🔴 Short | `702 703 731_AI_PASS` | 2026-06-28 22:45 ➔ 2026-06-29 10:45 | 12h 0m | **-6.31%** | **-4.90 USDT** | `exit_ai_drift_decay ( 702 703 731_AI_PASS)` |
| #8 | **CRV/USDT:USDT** | 🔴 Short | `702 703 731_AI_PASS` | 2026-06-01 08:30 ➔ 2026-06-01 20:30 | 12h 0m | **-9.48%** | **-2.54 USDT** | `exit_ai_drift_decay ( 702 703 731_AI_PASS)` |

### ⏱️ Nhật Ký 15 Lệnh Giao Dịch Gần Nhất (Recent Trades Log)
| # | Cặp giao dịch | Vị thế | Enter Tag | Thời gian Đóng | Thời lượng | Lợi nhuận % | Lợi nhuận USDT | Lý do thoát |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| #1 | **1000SHIB/USDT:USDT** | 🔴 Short | `562 ` | 2026-11-05 23:55 | 45m | **-3.18%** | **-19.65 USDT** | `force_exit` |
| #2 | **SOXL/USDT:USDT** | 🟢 Long | `44 ` | 2026-11-05 23:55 | 40m | **+1.62%** | **+7.41 USDT** | `force_exit` |
| #3 | **SNXX/USDT:USDT** | 🟢 Long | `3 6 ` | 2026-11-05 23:55 | 3h 5m | **-29.06%** | **-139.64 USDT** | `force_exit` |
| #4 | **MVLL/USDT:USDT** | 🟢 Long | `5 ` | 2026-11-05 22:15 | 1h 0m | **+2.03%** | **+7.60 USDT** | `exit_profit_long_normal_t_0_1_m ( 5 )` |
| #5 | **SNXX/USDT:USDT** | 🟢 Long | `61 ` | 2026-11-05 20:10 | 2h 15m | **+0.98%** | **+3.67 USDT** | `exit_profit_long_rebuy_t_0_1_m ( 61 )` |
| #6 | **CRV/USDT:USDT** | 🟢 Long | `141 142 ` | 2026-11-05 17:05 | 1h 10m | **+3.70%** | **+23.21 USDT** | `exit_profit_long_tc_t_0_1_m ( 141 142 )` |
| #7 | **SNXX/USDT:USDT** | 🟢 Long | `4 ` | 2026-11-05 14:45 | 23h 0m | **-62.11%** | **-184.18 USDT** | `exit_hard_preemptive_liquidation_guard ( 4 )` |
| #8 | **QNT/USDT:USDT** | 🟢 Long | `64 ` | 2026-11-05 06:05 | 11h 25m | **+0.95%** | **+6.18 USDT** | `exit_profit_long_rebuy_t_0_1_m ( 64 )` |
| #9 | **AXTI/USDT:USDT** | 🟢 Long | `43 ` | 2026-11-04 17:20 | 1h 25m | **+7.24%** | **+33.99 USDT** | `exit_profit_long_quick_t_1_1_m ( 43 )` |
| #10 | **DOT/USDT:USDT** | 🔴 Short | `721 724 742_AI_PASS` | 2026-11-03 08:30 | 3h 15m | **+4.95%** | **+28.42 USDT** | `exit_ai_reversal_harvest ( 721 724 742_AI_PASS)` |
| #11 | **ANTHROPIC/USDT:USDT** | 🔴 Short | `562 ` | 2026-11-03 04:30 | 5h 10m | **+4.68%** | **+29.23 USDT** | `exit_short_adaptive_trailing_scalp ( 562 )` |
| #12 | **RLC/USDT:USDT** | 🔴 Short | `721 724 745_AI_PASS` | 2026-11-01 01:25 | 1h 10m | **+5.64%** | **+35.01 USDT** | `exit_ai_reversal_harvest ( 721 724 745_AI_PASS)` |
| #13 | **BTW/USDT:USDT** | 🟢 Long | `3 ` | 2026-10-31 02:20 | 5h 5m | **+33.25%** | **+86.04 USDT** | `exit_long_normal_d_6_1 ( 3 )` |
| #14 | **BTW/USDT:USDT** | 🟢 Long | `3 ` | 2026-10-30 21:00 | 50m | **+0.58%** | **+1.49 USDT** | `exit_profit_long_normal_t_0_1_m ( 3 )` |
| #15 | **BTW/USDT:USDT** | 🟢 Long | `44 ` | 2026-10-30 19:30 | 5h 10m | **+12.86%** | **+60.05 USDT** | `exit_long_quick_q_6 ( 44 )` |

---
*Báo cáo được khởi tạo tự động bởi `scripts/export_report.py` phục vụ chu trình Tối ưu hóa Tự động Agentic AI.*
