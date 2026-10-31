# 📈 Báo Cáo Đánh Giá Hiệu Suất Backtest Toàn Diện (Comprehensive Quantitative Report)

| Thông Tin Phiên Chạy | Chi Tiết | Đánh Dấu / Định Danh |
| :--- | :--- | :--- |
| 🏷️ **Phiên bản Chiến lược (Version)** | **`v8.2`** | `v8.2` |
| 🔖 **Git Commit** | `23648d8` | `fix(eval): auto-detect strategy version from code in workflow and prevent stale git describe tag fallback` |
| 🚀 **Đánh dấu lần chạy (Run Marker)** | **`v8.2-23648d8`** | `Workflow #local` |
| 🤖 **Chiến lược (Strategy)** | `NostalgiaForInfinityX8_Combined_AI` | `Combined AI Engine` |
| 📅 **Thời gian đánh giá (Evaluation Date)** | `2026-10-31 15:50:37 UTC` | `UTC` |
| ⏱️ **Cửa sổ Backtest (Timerange)** | `20260504-20261031` | `178 ngày` |
| 📁 **Tệp kết quả (Source File)** | `backtest-result-2026-10-31_22-50-25.zip` | `Binance Futures 5m` |

---

## ⚖️ So Sánh Hiệu Suất Với Lần Backtest Trước (Benchmark Comparison)

| Chỉ số định lượng | Lần chạy này [v8.2-23648d8 - 23648d8] | Lần trước [v8.3-23648d8 - 23648d8] | Chênh lệch (Δ Delta) | Xu hướng |
| :--- | :--- | :--- | :--- | :--- |
| **Tỷ lệ thắng (Winrate)** | **95.36%** | **95.63%** | `-0.27%` | 🔴 Suy giảm |
| **Lợi nhuận ròng (Net Profit %)** | **+1187.80%** | **+1076.51%** | `+111.29%` | 🟢 Cải thiện |
| **Lợi nhuận tuyệt đối (USDT)** | **+2,375.61 USDT** | **+2,153.03 USDT** | `+222.58 USDT` | 🟢 Cải thiện |
| **Hệ số Sharpe (Sharpe Ratio)** | **16.11** | **15.73** | `+0.37` | 🟢 Cải thiện |
| **Hệ số Sortino (Sortino Ratio)** | **39.67** | **27.61** | `+12.06` | 🟢 Cải thiện |
| **Sụt giảm tối đa (Max Drawdown %)** | **1.77%** | **9.74%** | `-7.97%` | 🟢 Cải thiện |
| **Hệ số lãi/lỗ (Profit Factor)** | **22.85** | **19.77** | `+3.08` | 🟢 Cải thiện |
| **Tổng số lệnh (Total Trades)** | **237** | **229** | `+8.00 lệnh` | 🟢 Cải thiện |
| **Chuỗi lệnh thua dài nhất** | **3 trades** | **2 trades** | `+1.00 lệnh` | 🔴 Suy giảm |
| **Kỳ vọng toán học (Expectancy)** | **10.0237** | **9.4019** | `+0.62` | 🟢 Cải thiện |
| **Hệ số Calmar (Calmar Ratio)** | **7187.89** | **1186.43** | `+6,001.46` | 🟢 Cải thiện |

---

## 🏛️ Ma Trận Lịch Sử Đối Soát Giữa Các Lần Chạy (Multi-Run Version History Matrix)

> *Bảng tổng hợp đối chiếu kết quả backtest qua từng phiên bản và lần chạy để tiện theo dõi tiến trình tối ưu hóa.*

| Đánh dấu lần chạy (Run Marker) | Phiên bản | Commit | Ngày chạy | Tỷ lệ thắng (Winrate) | Lợi nhuận ròng | Max DD % | Sharpe | Profit Factor | Tổng lệnh | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `v8.0-23648d8` | **`v8.0`** | `23648d8` | 20261031 | **95.24%** | +2,148.78 USDT (+1074.4%) | 9.88% | 15.77 | 19.35 | `231` | ⚪ Đã lưu |
| `v8.0-23648d8` | **`v8.0`** | `23648d8` | 20261031 | **95.24%** | +2,148.86 USDT (+1074.4%) | 9.88% | 15.77 | 19.35 | `231` | ⚪ Đã lưu |
| `v8.0-23648d8` | **`v8.0`** | `23648d8` | 20261031 | **95.36%** | +2,373.75 USDT (+1186.9%) | 1.77% | 16.10 | 22.84 | `237` | ⚪ Đã lưu |
| `v8.2-23648d8` | **`v8.2`** | `23648d8` | 20261031 | **96.32%** | +1,930.50 USDT (+965.2%) | 1.25% | 14.37 | 27.01 | `190` | ⚪ Đã lưu |
| `v8.2-23648d8` | **`v8.2`** | `23648d8` | 20261031 | **96.35%** | +1,995.07 USDT (+997.5%) | 1.25% | 14.47 | 27.19 | `192` | ⚪ Đã lưu |
| `v8.2-23648d8` | **`v8.2`** | `23648d8` | 20261031 | **95.36%** | +2,373.75 USDT (+1186.9%) | 1.77% | 16.10 | 22.84 | `237` | ⚪ Đã lưu |
| `v8.3-23648d8` | **`v8.3`** | `23648d8` | 20261031 | **95.63%** | +2,153.03 USDT (+1076.5%) | 9.74% | 15.73 | 19.77 | `229` | ⚪ Đã lưu |
| `v8.2-23648d8` | **`v8.2`** | `23648d8` | 20261031 | **95.36%** | +2,375.61 USDT (+1187.8%) | 1.77% | 16.11 | 22.85 | `237` | 🎯 **HIỆN TẠI** |

---

## 🎯 Chỉ Số Hiệu Suất Cốt Lõi (Executive Performance Metrics)

| Chỉ số định lượng | Giá trị thực tế | Đánh giá Benchmark | Tiêu chuẩn chất lượng |
| :--- | :--- | :--- | :--- |
| **Tỷ lệ thắng (Winrate)** | **95.36%** | 🟢 Robust | Ngưỡng an toàn >= 70% |
| **Hệ số Sharpe (Sharpe Ratio)** | **16.11** | 🟢 Exceptional | Chuẩn Alpha quỹ >= 2.0 |
| **Hệ số Sortino (Sortino Ratio)** | **39.67** | 🟢 Excellent | Đo lường rủi ro sụt giảm âm |
| **Sụt giảm tài khoản tối đa (Max Drawdown %)** | **1.77%** | 🟢 Defended | Giới hạn rủi ro < 15% |
| **Sụt giảm tuyệt đối (Max Drawdown Abs)** | **+46.51 USDT** | 🟢 Đã kiểm soát | Độ sâu drawdown danh mục |
| **Hệ số lãi/lỗ (Profit Factor)** | **22.85** | 🟢 High | Chuẩn định lượng >= 1.5 |
| **Chuỗi thua dài nhất (Longest Loss Streak)** | **3 trades** | 🟢 Safe | Kiểm soát chuỗi sụt giảm |

---

## 📊 Chỉ Số Định Lượng Mở Rộng (Secondary Quantitative Indicators)

| Chỉ số định lượng | Kết quả | Mô tả & Ý nghĩa kỹ thuật |
| :--- | :--- | :--- |
| **Tổng số lệnh (Total Trades)** | `237` | Tổng số lệnh đã hoàn tất trong timerange |
| **Tổng lệnh thắng / hòa / thua** | `226` thắng / `0` hòa / `11` thua | Phân bổ kết quả các giao dịch |
| **Lợi nhuận ròng % (Net Profit %)** | `+1187.80%` | Tỷ lệ tăng trưởng toàn bộ tài khoản |
| **Lợi nhuận tuyệt đối (Net Profit Abs)** | `+2,375.61 USDT` | Lợi nhuận bằng tiền mặt (USDT) |
| **Lợi nhuận trung bình / lệnh** | `+10.02 USDT` | Hiệu quả trung bình mỗi lần vào lệnh |
| **Mật độ giao dịch (Trades Per Day)** | `1.33 lệnh / ngày` | Tần suất giao dịch bình quân |
| **Kỳ vọng toán học (Expectancy)** | `10.0237` | Lợi nhuận kỳ vọng trên mỗi 1 đơn vị rủi ro |
| **Hệ số Calmar (Calmar Ratio)** | `7187.89` | Tỷ lệ lợi nhuận trên sụt giảm vốn tối đa |
| **Tốc độ tăng trưởng kép (CAGR)** | `18771.87%` | Compound Annual Growth Rate quy năm |

---

## ⚔️ Thống Kê Phân Bổ Vị Thế (Long vs Short Performance)

| Vị thế (Position) | Số lệnh | Tỷ trọng | Tỷ lệ thắng (Winrate) | Lợi nhuận (USDT) | Lợi nhuận (%) | Đánh giá |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 **Lệnh Mua (Long)** | `166` | 70.0% | **98.19%** | **+2,083.54 USDT** | +2542.07% | 🟢 Vượt trội |
| 🔴 **Lệnh Bán (Short)** | `71` | 30.0% | **88.73%** | **+292.06 USDT** | +300.59% | 🟢 Vượt trội |
| 🌐 **Toàn bộ danh mục** | `237` | 100.0% | **95.36%** | **+2,375.61 USDT** | +1187.80% | 🎯 Hoàn tất |

## 🚪 Phân Tích Lý Do Thoát Lệnh (Exit Reason Breakdown)

| Lý do đóng lệnh (Exit Reason) | Số lệnh | Tỷ trọng | Tỷ lệ thắng (Winrate) | Lợi nhuận (USDT) |
| :--- | :--- | :--- | :--- | :--- |
| `TOTAL` | `237` | 100.0% | **95.4%** | +2,375.61 USDT |
| `exit_ai_reversal_harvest ( 702 703 731_AI_PASS)` | `15` | 6.3% | **100.0%** | +51.77 USDT |
| `exit_profit_long_rebuy_t_0_1_m ( 64 )` | `12` | 5.1% | **100.0%** | +39.29 USDT |
| `exit_short_adaptive_trailing_scalp ( 562 )` | `9` | 3.8% | **100.0%** | +104.89 USDT |
| `exit_profit_long_tc_t_0_1_m ( 142 )` | `7` | 3.0% | **100.0%** | +7.91 USDT |
| `exit_long_rebuy_d_6_1 ( 64 )` | `5` | 2.1% | **100.0%** | +217.56 USDT |
| `exit_long_rebuy_e_r ( 65 )` | `4` | 1.7% | **100.0%** | +36.98 USDT |
| `exit_profit_long_tc_t_0_1_m ( 143 )` | `4` | 1.7% | **100.0%** | +8.06 USDT |
| `exit_profit_long_tc_t_0_1_m ( 144 )` | `4` | 1.7% | **100.0%** | +7.19 USDT |
| `exit_long_quick_q_9 ( 44 )` | `3` | 1.3% | **100.0%** | +60.61 USDT |
| `exit_short_adaptive_trailing_scalp ( 542 )` | `3` | 1.3% | **100.0%** | +28.85 USDT |
| `exit_profit_long_tc_t_1_1_m ( 145 )` | `3` | 1.3% | **100.0%** | +18.07 USDT |
| `exit_long_normal_u_1 ( 2 )` | `3` | 1.3% | **100.0%** | +14.41 USDT |
| `exit_ai_reversal_harvest ( 702 703 731 743_AI_PASS)` | `3` | 1.3% | **100.0%** | +12.17 USDT |
| `exit_ai_reversal_harvest ( 744_AI_PASS)` | `3` | 1.3% | **100.0%** | +9.91 USDT |
| `exit_profit_long_tc_t_0_1_m ( 145 )` | `3` | 1.3% | **100.0%** | +9.47 USDT |
| `exit_ai_profit_lock ( 702 703 731_AI_PASS)` | `3` | 1.3% | **100.0%** | +4.80 USDT |
| `exit_profit_short_rebuy_t_0_1_m ( 562 )` | `3` | 1.3% | **100.0%** | +3.42 USDT |
| `exit_ai_profit_lock ( 744_AI_PASS)` | `3` | 1.3% | **100.0%** | +2.51 USDT |
| `exit_long_normal_d_4_1 ( 2 )` | `2` | 0.8% | **100.0%** | +92.04 USDT |
| `exit_long_rebuy_d_6_1 ( 62 )` | `2` | 0.8% | **100.0%** | +81.60 USDT |
| `exit_long_normal_d_7_1 ( 2 )` | `2` | 0.8% | **100.0%** | +75.36 USDT |
| `exit_long_rebuy_d_4_1 ( 64 )` | `2` | 0.8% | **100.0%** | +33.92 USDT |
| `exit_short_rebuy_1_1_1 ( 562 )` | `2` | 0.8% | **100.0%** | +32.59 USDT |
| `exit_long_normal_d_6_1 ( 2 )` | `2` | 0.8% | **100.0%** | +24.91 USDT |
| `exit_ai_reversal_harvest ( 743 744_AI_PASS)` | `2` | 0.8% | **100.0%** | +22.24 USDT |
| `exit_long_rapid_rpd_2 ( 102 )` | `2` | 0.8% | **100.0%** | +17.36 USDT |
| `exit_long_tc_u_1 ( 141 )` | `2` | 0.8% | **100.0%** | +16.93 USDT |
| `exit_long_tc_d_5_1 ( 141 142 )` | `2` | 0.8% | **100.0%** | +10.51 USDT |
| `exit_long_tc_d_5_1 ( 142 )` | `2` | 0.8% | **100.0%** | +10.37 USDT |
| `exit_profit_long_scalp_t_1_1_m ( 163 )` | `2` | 0.8% | **100.0%** | +9.11 USDT |
| `exit_profit_long_tc_t_0_1_m ( 141 )` | `2` | 0.8% | **100.0%** | +4.34 USDT |
| `exit_ai_reversal_harvest ( 721 724 742_AI_PASS)` | `2` | 0.8% | **100.0%** | +4.08 USDT |
| `exit_profit_long_rebuy_t_0_1_m ( 61 )` | `2` | 0.8% | **100.0%** | +3.69 USDT |
| `exit_profit_long_rebuy_t_0_1_m ( 62 )` | `2` | 0.8% | **100.0%** | +3.34 USDT |
| `exit_profit_long_scalp_t_0_1_m ( 163 )` | `2` | 0.8% | **100.0%** | +1.62 USDT |
| `exit_ai_drift_decay ( 702 703 731_AI_PASS)` | `2` | 0.8% | **0.0%** | -5.94 USDT |
| `exit_short_universal_structural_cut ( 562 )` | `2` | 0.8% | **0.0%** | -21.89 USDT |
| `force_exit` | `2` | 0.8% | **0.0%** | -32.49 USDT |
| `exit_long_rebuy_d_7_1 ( 64 )` | `1` | 0.4% | **100.0%** | +86.72 USDT |
| `exit_long_rebuy_2_1_1 ( 64 )` | `1` | 0.4% | **100.0%** | +75.31 USDT |
| `exit_long_quick_d_11_1 ( 43 )` | `1` | 0.4% | **100.0%** | +74.56 USDT |
| `exit_long_tc_d_3_2 ( 141 )` | `1` | 0.4% | **100.0%** | +59.08 USDT |
| `exit_long_normal_d_6_1 ( 1 )` | `1` | 0.4% | **100.0%** | +52.02 USDT |
| `exit_long_rapid_d_5_1 ( 103 )` | `1` | 0.4% | **100.0%** | +48.09 USDT |
| `exit_long_quick_q_6 ( 42 )` | `1` | 0.4% | **100.0%** | +47.75 USDT |
| `exit_long_rebuy_w_6_1 ( 64 )` | `1` | 0.4% | **100.0%** | +40.03 USDT |
| `exit_long_normal_d_7_1 ( 6 )` | `1` | 0.4% | **100.0%** | +37.57 USDT |
| `exit_long_rebuy_d_8_1 ( 64 )` | `1` | 0.4% | **100.0%** | +37.10 USDT |
| `exit_long_normal_d_4_1 ( 6 )` | `1` | 0.4% | **100.0%** | +36.80 USDT |
| `exit_long_tc_d_8_1 ( 142 )` | `1` | 0.4% | **100.0%** | +35.69 USDT |
| `exit_long_tc_d_3_1 ( 141 )` | `1` | 0.4% | **100.0%** | +33.69 USDT |
| `exit_long_tc_d_5_1 ( 141 )` | `1` | 0.4% | **100.0%** | +32.37 USDT |
| `exit_long_rebuy_d_4_1 ( 65 )` | `1` | 0.4% | **100.0%** | +31.30 USDT |
| `exit_long_normal_u_3 ( 6 141 )` | `1` | 0.4% | **100.0%** | +27.20 USDT |
| `exit_long_tc_3_1_1 ( 141 142 )` | `1` | 0.4% | **100.0%** | +26.26 USDT |
| `exit_long_scalp_d_5_1 ( 163 )` | `1` | 0.4% | **100.0%** | +25.93 USDT |
| `exit_short_adaptive_trailing_mega ( 562 )` | `1` | 0.4% | **100.0%** | +25.03 USDT |
| `exit_long_rebuy_d_5_1 ( 65 )` | `1` | 0.4% | **100.0%** | +23.50 USDT |
| `exit_long_rebuy_d_9_1 ( 65 )` | `1` | 0.4% | **100.0%** | +21.12 USDT |
| `exit_long_tc_d_6_1 ( 144 )` | `1` | 0.4% | **100.0%** | +17.86 USDT |
| `exit_profit_long_rebuy_t_7_1_m ( 63 )` | `1` | 0.4% | **100.0%** | +17.00 USDT |
| `exit_long_rebuy_d_8_1 ( 61 )` | `1` | 0.4% | **100.0%** | +14.43 USDT |
| `exit_long_scalp_d_6_1 ( 61 162 )` | `1` | 0.4% | **100.0%** | +14.42 USDT |
| `exit_long_rebuy_d_6_1 ( 63 )` | `1` | 0.4% | **100.0%** | +14.01 USDT |
| `exit_profit_long_normal_t_2_1_m ( 3 )` | `1` | 0.4% | **100.0%** | +13.62 USDT |
| `exit_long_quick_q_6 ( 47 )` | `1` | 0.4% | **100.0%** | +13.58 USDT |
| `exit_long_rebuy_d_6_1 ( 61 )` | `1` | 0.4% | **100.0%** | +13.48 USDT |
| `exit_ai_reversal_harvest ( 702 703 705 731_AI_PASS)` | `1` | 0.4% | **100.0%** | +13.39 USDT |
| `exit_long_tc_d_5_1 ( 145 )` | `1` | 0.4% | **100.0%** | +13.27 USDT |
| `exit_profit_long_tc_t_2_1_m ( 145 )` | `1` | 0.4% | **100.0%** | +12.88 USDT |
| `exit_long_scalp_d_6_1 ( 162 )` | `1` | 0.4% | **100.0%** | +12.74 USDT |
| `exit_long_tc_u_1 ( 141 142 )` | `1` | 0.4% | **100.0%** | +12.51 USDT |
| `exit_profit_long_tc_t_2_1_m ( 142 )` | `1` | 0.4% | **100.0%** | +12.37 USDT |
| `exit_long_tc_u_1 ( 142 )` | `1` | 0.4% | **100.0%** | +12.11 USDT |
| `exit_profit_short_rebuy_t_1_1_m ( 562 )` | `1` | 0.4% | **100.0%** | +12.06 USDT |
| `exit_long_quick_d_7_1 ( 42 )` | `1` | 0.4% | **100.0%** | +11.75 USDT |
| `exit_profit_long_quick_t_2_1_m ( 46 )` | `1` | 0.4% | **100.0%** | +11.62 USDT |
| `exit_long_normal_u_1 ( 1 )` | `1` | 0.4% | **100.0%** | +10.93 USDT |
| `exit_long_normal_d_3_2 ( 5 )` | `1` | 0.4% | **100.0%** | +10.54 USDT |
| `exit_long_tc_d_6_1 ( 141 )` | `1` | 0.4% | **100.0%** | +10.02 USDT |
| `exit_long_rebuy_d_5_1 ( 63 )` | `1` | 0.4% | **100.0%** | +9.77 USDT |
| `exit_long_tc_d_6_1 ( 141 143 163 )` | `1` | 0.4% | **100.0%** | +8.93 USDT |
| `exit_profit_long_normal_t_1_1_m ( 3 )` | `1` | 0.4% | **100.0%** | +8.67 USDT |
| `exit_profit_long_tc_t_1_1_m ( 141 )` | `1` | 0.4% | **100.0%** | +8.51 USDT |
| `exit_profit_long_tc_t_1_1_m ( 141 142 )` | `1` | 0.4% | **100.0%** | +8.27 USDT |
| `exit_long_tc_d_4_2 ( 145 )` | `1` | 0.4% | **100.0%** | +7.94 USDT |
| `exit_long_tc_d_6_1 ( 142 )` | `1` | 0.4% | **100.0%** | +7.70 USDT |
| `exit_long_normal_d_3_1 ( 1 )` | `1` | 0.4% | **100.0%** | +7.39 USDT |
| `exit_profit_long_rebuy_t_3_1_m ( 61 )` | `1` | 0.4% | **100.0%** | +7.27 USDT |
| `exit_ai_profit_lock ( 703 721 724 731_AI_PASS)` | `1` | 0.4% | **100.0%** | +7.24 USDT |
| `exit_long_normal_u_4 ( 1 61 )` | `1` | 0.4% | **100.0%** | +7.18 USDT |
| `exit_long_tc_d_5_1 ( 62 144 )` | `1` | 0.4% | **100.0%** | +7.15 USDT |
| `exit_long_normal_d_8_1 ( 4 )` | `1` | 0.4% | **100.0%** | +7.14 USDT |
| `exit_long_normal_d_7_1 ( 2 101 141 )` | `1` | 0.4% | **100.0%** | +6.83 USDT |
| `exit_profit_long_rebuy_t_2_1_m ( 65 )` | `1` | 0.4% | **100.0%** | +6.51 USDT |
| `exit_long_normal_d_5_1 ( 2 )` | `1` | 0.4% | **100.0%** | +6.45 USDT |
| `exit_long_normal_d_6_1 ( 3 142 )` | `1` | 0.4% | **100.0%** | +6.39 USDT |
| `exit_profit_long_normal_t_0_1_m ( 2 )` | `1` | 0.4% | **100.0%** | +6.06 USDT |
| `exit_long_normal_d_5_1 ( 6 102 141 )` | `1` | 0.4% | **100.0%** | +5.91 USDT |
| `exit_long_tc_d_5_1 ( 144 )` | `1` | 0.4% | **100.0%** | +5.87 USDT |
| `exit_long_tc_d_3_2 ( 102 142 )` | `1` | 0.4% | **100.0%** | +5.42 USDT |
| `exit_profit_long_rapid_t_1_1_m ( 102 )` | `1` | 0.4% | **100.0%** | +5.36 USDT |
| `exit_long_normal_d_5_1 ( 5 )` | `1` | 0.4% | **100.0%** | +5.20 USDT |
| `exit_profit_long_tc_t_0_1_m ( 141 142 )` | `1` | 0.4% | **100.0%** | +5.10 USDT |
| `exit_long_normal_d_6_1 ( 2 141 )` | `1` | 0.4% | **100.0%** | +4.86 USDT |
| `exit_long_quick_q_2 ( 41 )` | `1` | 0.4% | **100.0%** | +4.54 USDT |
| `exit_long_rapid_rpd_6 ( 102 )` | `1` | 0.4% | **100.0%** | +4.41 USDT |
| `exit_profit_long_tc_t_3_1_m ( 143 )` | `1` | 0.4% | **100.0%** | +4.05 USDT |
| `exit_long_normal_u_2 ( 4 41 61 )` | `1` | 0.4% | **100.0%** | +4.02 USDT |
| `exit_long_rebuy_u_1 ( 61 )` | `1` | 0.4% | **100.0%** | +3.88 USDT |
| `exit_profit_long_rebuy_t_2_1_m ( 62 )` | `1` | 0.4% | **100.0%** | +3.61 USDT |
| `exit_profit_long_rebuy_t_1_1_m ( 62 )` | `1` | 0.4% | **100.0%** | +3.55 USDT |
| `exit_ai_reversal_harvest ( 721 724 741_AI_PASS)` | `1` | 0.4% | **100.0%** | +3.19 USDT |
| `exit_short_rebuy_u_1 ( 562 )` | `1` | 0.4% | **100.0%** | +3.02 USDT |
| `exit_profit_long_normal_t_0_1_m ( 6 102 )` | `1` | 0.4% | **100.0%** | +2.98 USDT |
| `exit_ai_reversal_harvest ( 721 742_AI_PASS)` | `1` | 0.4% | **100.0%** | +2.87 USDT |
| `exit_ai_profit_lock ( 702 703 706 731 743_AI_PASS)` | `1` | 0.4% | **100.0%** | +2.78 USDT |
| `exit_long_normal_u_2 ( 2 )` | `1` | 0.4% | **100.0%** | +2.43 USDT |
| `exit_ai_reversal_harvest ( 703 721 731_AI_PASS)` | `1` | 0.4% | **100.0%** | +2.34 USDT |
| `exit_short_adaptive_trailing_scalp ( 702 703 731_AI_PASS)` | `1` | 0.4% | **100.0%** | +2.29 USDT |
| `exit_profit_long_normal_t_0_1_m ( 6 )` | `1` | 0.4% | **100.0%** | +1.99 USDT |
| `exit_profit_long_scalp_t_2_1_m ( 163 )` | `1` | 0.4% | **100.0%** | +1.92 USDT |
| `exit_long_normal_w_0_1 ( 1 )` | `1` | 0.4% | **100.0%** | +1.89 USDT |
| `exit_profit_long_rebuy_t_2_1_m ( 64 )` | `1` | 0.4% | **100.0%** | +1.85 USDT |
| `exit_long_quick_u_1 ( 43 )` | `1` | 0.4% | **100.0%** | +1.82 USDT |
| `exit_profit_long_normal_t_2_1_m ( 2 63 101 )` | `1` | 0.4% | **100.0%** | +1.73 USDT |
| `exit_long_tc_u_1 ( 144 )` | `1` | 0.4% | **100.0%** | +1.57 USDT |
| `exit_profit_long_scalp_t_0_1_m ( 161 )` | `1` | 0.4% | **100.0%** | +1.57 USDT |
| `exit_long_normal_w_1_1 ( 3 )` | `1` | 0.4% | **100.0%** | +1.56 USDT |
| `exit_ai_reversal_harvest ( 702 703 724 731_AI_PASS)` | `1` | 0.4% | **100.0%** | +1.52 USDT |
| `exit_ai_reversal_harvest ( 703 705 706 731_AI_PASS)` | `1` | 0.4% | **100.0%** | +1.46 USDT |
| `exit_profit_long_normal_t_0_1_m ( 3 )` | `1` | 0.4% | **100.0%** | +1.39 USDT |
| `exit_profit_long_quick_t_1_1_m ( 42 )` | `1` | 0.4% | **100.0%** | +1.26 USDT |
| `exit_ai_reversal_harvest ( 724 742_AI_PASS)` | `1` | 0.4% | **100.0%** | +1.22 USDT |
| `exit_profit_long_rapid_t_0_1_m ( 102 )` | `1` | 0.4% | **100.0%** | +1.11 USDT |
| `exit_ai_profit_lock ( 721 724 742_AI_PASS)` | `1` | 0.4% | **100.0%** | +1.09 USDT |
| `exit_profit_long_scalp_t_0_1_m ( 162 )` | `1` | 0.4% | **100.0%** | +1.03 USDT |
| `exit_profit_long_quick_t_0_1_m ( 43 )` | `1` | 0.4% | **100.0%** | +0.81 USDT |
| `exit_ai_profit_lock ( 703 705 706 731_AI_PASS)` | `1` | 0.4% | **100.0%** | +0.47 USDT |
| `exit_profit_long_normal_t_0_1_m ( 5 )` | `1` | 0.4% | **100.0%** | +0.35 USDT |
| `exit_ai_drift_decay ( 703 721 731_AI_PASS)` | `1` | 0.4% | **0.0%** | -2.84 USDT |
| `exit_ai_562_aged_breakeven ( 562 )` | `1` | 0.4% | **0.0%** | -4.16 USDT |
| `exit_bad_trade_abandon_18d ( 120 )` | `1` | 0.4% | **0.0%** | -11.05 USDT |
| `exit_ai_drift_decay ( 744_AI_PASS)` | `1` | 0.4% | **0.0%** | -14.02 USDT |
| `exit_short_universal_structural_cut ( 542 )` | `1` | 0.4% | **0.0%** | -16.32 USDT |

## 🔍 Bảng Phân Tích Đầy Đủ Tất Cả Các Entry Tags (Full Enter Tag Breakdown)

> *Bảng tổng hợp chi tiết 100% tất cả các tag tín hiệu vào lệnh (Entry Tags) đã hoạt động trong phiên backtest.*

| Enter Tag | Vị thế | Số lệnh | Tỷ lệ thắng (Winrate) | Thắng/Hòa/Thua | Tổng LN % | Tổng LN (USDT) | LN TB/Lệnh | Thời lượng TB | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `TOTAL` | 🟢 Long Core | `237` | **95.4%** | 226/0/11 | +1187.80% | **+2,375.61 USDT** | +11.99% | 10:57:00 | 🟢 Tối ưu |
| `64` | 🟢 Long Core | `25` | **96.0%** | 24/0/1 | +253.80% | **+507.60 USDT** | +17.43% | 9:34:00 | 🟢 Tối ưu |
| `2` | 🟢 Long Core | `12` | **100.0%** | 12/0/0 | +110.83% | **+221.66 USDT** | +20.29% | 2:08:00 | 🟢 Tối ưu |
| `141` | 🟢 Long Core | `9` | **100.0%** | 9/0/0 | +82.47% | **+164.95 USDT** | +13.19% | 10:27:00 | 🟢 Tối ưu |
| `562` | 🟢 Long Core | `20` | **85.0%** | 17/0/3 | +77.49% | **+154.97 USDT** | +5.75% | 1 day, 4:38:00 | 🟢 Tối ưu |
| `65` | 🟢 Long Core | `8` | **100.0%** | 8/0/0 | +59.70% | **+119.41 USDT** | +19.45% | 2:26:00 | 🟢 Tối ưu |
| `62` | 🟢 Long Core | `6` | **100.0%** | 6/0/0 | +46.05% | **+92.10 USDT** | +8.86% | 14:39:00 | 🟢 Tối ưu |
| `142` | 🟢 Long Core | `13` | **100.0%** | 13/0/0 | +43.07% | **+86.15 USDT** | +11.82% | 8:32:00 | 🟢 Tối ưu |
| `43` | 🟢 Long Core | `3` | **100.0%** | 3/0/0 | +38.60% | **+77.20 USDT** | +26.00% | 0:35:00 | 🟢 Tối ưu |
| `6` | 🟢 Long Core | `3` | **100.0%** | 3/0/0 | +38.18% | **+76.36 USDT** | +18.75% | 17:13:00 | 🟢 Tối ưu |
| `1` | 🟢 Long Core | `4` | **100.0%** | 4/0/0 | +36.11% | **+72.23 USDT** | +11.54% | 1 day, 20:39:00 | 🟢 Tối ưu |
| `141 142` | 🟢 Long Core | `6` | **100.0%** | 6/0/0 | +31.32% | **+62.65 USDT** | +13.96% | 9:57:00 | 🟢 Tối ưu |
| `145` | 🟢 Long Core | `9` | **100.0%** | 9/0/0 | +30.82% | **+61.63 USDT** | +10.60% | 8:46:00 | 🟢 Tối ưu |
| `42` | 🟢 Long Core | `3` | **100.0%** | 3/0/0 | +30.38% | **+60.76 USDT** | +22.44% | 1:15:00 | 🟢 Tối ưu |
| `44` | 🟢 Long Core | `3` | **100.0%** | 3/0/0 | +30.30% | **+60.61 USDT** | +22.49% | 2:32:00 | 🟢 Tối ưu |
| `702 703 731_AI_PASS` | 🤖 Short AI Gatekeeper | `21` | **90.5%** | 19/0/2 | +26.46% | **+52.92 USDT** | +4.17% | 4:08:00 | 🟢 Tối ưu |
| `103` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +24.05% | **+48.09 USDT** | +25.41% | 2:30:00 | 🟢 Tối ưu |
| `61` | 🟢 Long Core | `6` | **100.0%** | 6/0/0 | +21.37% | **+42.74 USDT** | +18.80% | 1:51:00 | 🟢 Tối ưu |
| `63` | 🟢 Long Core | `3` | **100.0%** | 3/0/0 | +20.39% | **+40.79 USDT** | +33.10% | 3:02:00 | 🟢 Tối ưu |
| `163` | 🟢 Long Core | `6` | **100.0%** | 6/0/0 | +19.29% | **+38.58 USDT** | +9.34% | 2:25:00 | 🟢 Tối ưu |
| `144` | 🟢 Long Core | `7` | **100.0%** | 7/0/0 | +16.25% | **+32.49 USDT** | +11.59% | 12:41:00 | 🟢 Tối ưu |
| `102` | 🟢 Long Core | `5` | **100.0%** | 5/0/0 | +14.12% | **+28.24 USDT** | +5.29% | 2:58:00 | 🟢 Tối ưu |
| `6 141` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +13.60% | **+27.20 USDT** | +16.21% | 19:20:00 | 🟢 Tối ưu |
| `3` | 🟢 Long Core | `4` | **100.0%** | 4/0/0 | +12.62% | **+25.24 USDT** | +5.78% | 20:10:00 | 🟢 Tối ưu |
| `743 744_AI_PASS` | 🤖 Short AI Gatekeeper | `2` | **100.0%** | 2/0/0 | +11.12% | **+22.24 USDT** | +5.47% | 3:15:00 | 🟢 Tối ưu |
| `5` | 🟢 Long Core | `3` | **100.0%** | 3/0/0 | +8.04% | **+16.08 USDT** | +14.52% | 3:03:00 | 🟢 Tối ưu |
| `61 162` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +7.21% | **+14.42 USDT** | +32.22% | 4:05:00 | 🟢 Tối ưu |
| `162` | 🟢 Long Core | `2` | **100.0%** | 2/0/0 | +6.88% | **+13.77 USDT** | +17.33% | 0:52:00 | 🟢 Tối ưu |
| `47` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +6.79% | **+13.58 USDT** | +13.38% | 1 day, 2:00:00 | 🟢 Tối ưu |
| `702 703 705 731_AI_PASS` | 🤖 Short AI Gatekeeper | `1` | **100.0%** | 1/0/0 | +6.70% | **+13.39 USDT** | +6.15% | 7:45:00 | 🟢 Tối ưu |
| `542` | 🟢 Long Core | `4` | **75.0%** | 3/0/1 | +6.27% | **+12.53 USDT** | +1.59% | 1:24:00 | 🟡 Hiệu quả |
| `702 703 731 743_AI_PASS` | 🤖 Short AI Gatekeeper | `3` | **100.0%** | 3/0/0 | +6.09% | **+12.17 USDT** | +6.26% | 2:30:00 | 🟢 Tối ưu |
| `143` | 🟢 Long Core | `5` | **100.0%** | 5/0/0 | +6.06% | **+12.12 USDT** | +5.30% | 18:36:00 | 🟢 Tối ưu |
| `141 143 163` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +4.46% | **+8.93 USDT** | +33.41% | 1:30:00 | 🟢 Tối ưu |
| `703 721 724 731_AI_PASS` | 🤖 Short AI Gatekeeper | `1` | **100.0%** | 1/0/0 | +3.62% | **+7.24 USDT** | +2.29% | 0:15:00 | 🟢 Tối ưu |
| `1 61` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +3.59% | **+7.18 USDT** | +21.38% | 0:15:00 | 🟢 Tối ưu |
| `62 144` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +3.57% | **+7.15 USDT** | +25.85% | 1:25:00 | 🟢 Tối ưu |
| `4` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +3.57% | **+7.14 USDT** | +44.22% | 1:10:00 | 🟢 Tối ưu |
| `2 101 141` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +3.41% | **+6.83 USDT** | +36.21% | 1:00:00 | 🟢 Tối ưu |
| `3 142` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +3.19% | **+6.39 USDT** | +21.64% | 1 day, 19:40:00 | 🟢 Tối ưu |
| `6 102 141` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +2.96% | **+5.91 USDT** | +26.17% | 1:00:00 | 🟢 Tối ưu |
| `102 142` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +2.71% | **+5.42 USDT** | +19.97% | 1:40:00 | 🟢 Tối ưu |
| `721 724 742_AI_PASS` | 🤖 Short AI Gatekeeper | `3` | **100.0%** | 3/0/0 | +2.59% | **+5.17 USDT** | +4.20% | 1:03:00 | 🟢 Tối ưu |
| `2 141` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +2.43% | **+4.86 USDT** | +30.19% | 2:15:00 | 🟢 Tối ưu |
| `41` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +2.27% | **+4.54 USDT** | +11.69% | 5:00:00 | 🟢 Tối ưu |
| `4 41 61` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +2.01% | **+4.02 USDT** | +11.78% | 0:10:00 | 🟢 Tối ưu |
| `46` | 🟢 Long Core | `2` | **50.0%** | 1/0/1 | +1.65% | **+3.30 USDT** | +4.48% | 0:38:00 | ⚪ Theo dõi |
| `721 724 741_AI_PASS` | 🤖 Short AI Gatekeeper | `1` | **100.0%** | 1/0/0 | +1.60% | **+3.19 USDT** | +5.01% | 7:05:00 | 🟢 Tối ưu |
| `6 102` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +1.49% | **+2.98 USDT** | +1.43% | 2:05:00 | 🟢 Tối ưu |
| `721 742_AI_PASS` | 🤖 Short AI Gatekeeper | `1` | **100.0%** | 1/0/0 | +1.44% | **+2.87 USDT** | +4.99% | 3:30:00 | 🟢 Tối ưu |
| `702 703 706 731 743_AI_PASS` | 🤖 Short AI Gatekeeper | `1` | **100.0%** | 1/0/0 | +1.39% | **+2.78 USDT** | +1.60% | 0:45:00 | 🟢 Tối ưu |
| `703 705 706 731_AI_PASS` | 🤖 Short AI Gatekeeper | `2` | **100.0%** | 2/0/0 | +0.97% | **+1.93 USDT** | +3.91% | 3:35:00 | 🟢 Tối ưu |
| `2 63 101` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +0.87% | **+1.73 USDT** | +10.72% | 2:55:00 | 🟢 Tối ưu |
| `161` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +0.78% | **+1.57 USDT** | +2.85% | 12:05:00 | 🟢 Tối ưu |
| `702 703 724 731_AI_PASS` | 🤖 Short AI Gatekeeper | `1` | **100.0%** | 1/0/0 | +0.76% | **+1.52 USDT** | +6.01% | 0:25:00 | 🟢 Tối ưu |
| `724 742_AI_PASS` | 🤖 Short AI Gatekeeper | `1` | **100.0%** | 1/0/0 | +0.61% | **+1.22 USDT** | +4.95% | 4:10:00 | 🟢 Tối ưu |
| `703 721 731_AI_PASS` | 🤖 Short AI Gatekeeper | `2` | **50.0%** | 1/0/1 | -0.25% | **-0.50 USDT** | -3.21% | 8:30:00 | 🔴 Cần tinh chỉnh |
| `744_AI_PASS` | 🤖 Short AI Gatekeeper | `7` | **85.7%** | 6/0/1 | -0.80% | **-1.60 USDT** | +2.42% | 3:33:00 | 🔴 Cần tinh chỉnh |
| `120` | 🟢 Long Core | `1` | **0.0%** | 0/0/1 | -5.53% | **-11.05 USDT** | -9.87% | 17 days, 22:40:00 | 🔴 Cần tinh chỉnh |

---

## 📑 Chi Tiết Các Lệnh Giao Dịch (Trade Execution Journal)

### 🥇 Top 10 Lệnh Lãi Cao Nhất (Top Winning Trades)
| # | Cặp giao dịch | Vị thế | Enter Tag | Thời gian Mở ➔ Đóng | Thời lượng | Lợi nhuận % | Lợi nhuận USDT | Lý do thoát |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| #1 | **BAT/USDT:USDT** | 🟢 Long | `64 ` | 2026-10-08 08:20 ➔ 2026-10-09 06:05 | 21h 45m | **+43.38%** | **+86.72 USDT** | `exit_long_rebuy_d_7_1 ( 64 )` |
| #2 | **GRASS/USDT:USDT** | 🟢 Long | `62 ` | 2026-10-14 17:45 ➔ 2026-10-15 15:05 | 21h 20m | **+33.86%** | **+77.78 USDT** | `exit_long_rebuy_d_6_1 ( 62 )` |
| #3 | **ARB/USDT:USDT** | 🟢 Long | `64 ` | 2026-09-17 21:45 ➔ 2026-09-18 01:50 | 4h 5m | **+59.20%** | **+75.31 USDT** | `exit_long_rebuy_2_1_1 ( 64 )` |
| #4 | **BTW/USDT:USDT** | 🟢 Long | `43 ` | 2026-10-05 06:45 ➔ 2026-10-05 08:05 | 1h 20m | **+71.12%** | **+74.56 USDT** | `exit_long_quick_d_11_1 ( 43 )` |
| #5 | **BTW/USDT:USDT** | 🟢 Long | `2 ` | 2026-10-23 18:30 ➔ 2026-10-23 19:10 | 40m | **+38.38%** | **+68.53 USDT** | `exit_long_normal_d_7_1 ( 2 )` |
| #6 | **GRASS/USDT:USDT** | 🟢 Long | `64 ` | 2026-10-05 14:55 ➔ 2026-10-05 19:15 | 4h 20m | **+32.17%** | **+59.25 USDT** | `exit_long_rebuy_d_6_1 ( 64 )` |
| #7 | **WLD/USDT:USDT** | 🟢 Long | `141 ` | 2026-10-25 08:55 ➔ 2026-10-25 15:40 | 6h 45m | **+19.30%** | **+59.08 USDT** | `exit_long_tc_d_3_2 ( 141 )` |
| #8 | **BAT/USDT:USDT** | 🟢 Long | `64 ` | 2026-10-03 06:15 ➔ 2026-10-04 07:40 | 25h 25m | **+33.11%** | **+55.31 USDT** | `exit_long_rebuy_d_6_1 ( 64 )` |
| #9 | **BTW/USDT:USDT** | 🟢 Long | `1 ` | 2026-10-22 20:45 ➔ 2026-10-22 21:40 | 55m | **+30.41%** | **+52.02 USDT** | `exit_long_normal_d_6_1 ( 1 )` |
| #10 | **QNT/USDT:USDT** | 🟢 Long | `2 ` | 2026-10-13 11:10 ➔ 2026-10-13 18:40 | 7h 30m | **+24.34%** | **+49.14 USDT** | `exit_long_normal_d_4_1 ( 2 )` |

### ⚠️ Top Lệnh Thua Lỗ / Sụt Giảm Lớn Nhất (Top Drawdown Trades)
| # | Cặp giao dịch | Vị thế | Enter Tag | Thời gian Mở ➔ Đóng | Thời lượng | Thua lỗ % | Thua lỗ USDT | Lý do thoát |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| #1 | **XMR/USDT:USDT** | 🟢 Long | `64 ` | 2026-10-29 23:05 ➔ 2026-10-29 23:55 | 50m | **-8.27%** | **-24.17 USDT** | `force_exit` |
| #2 | **MVLL/USDT:USDT** | 🔴 Short | `542 ` | 2026-08-20 17:15 ➔ 2026-08-20 20:05 | 2h 50m | **-23.02%** | **-16.32 USDT** | `exit_short_universal_structural_cut ( 542 )` |
| #3 | **OP/USDT:USDT** | 🔴 Short | `744_AI_PASS` | 2026-10-27 09:50 ➔ 2026-10-27 21:50 | 12h 0m | **-10.17%** | **-14.02 USDT** | `exit_ai_drift_decay ( 744_AI_PASS)` |
| #4 | **ZEC/USDT:USDT** | 🔴 Short | `562 ` | 2026-07-29 03:35 ➔ 2026-07-30 05:50 | 26h 15m | **-22.91%** | **-12.80 USDT** | `exit_short_universal_structural_cut ( 562 )` |
| #5 | **RENDER/USDT:USDT** | 🟢 Long | `120 ` | 2026-06-04 01:20 ➔ 2026-06-22 00:00 | 430h 40m | **-9.87%** | **-11.05 USDT** | `exit_bad_trade_abandon_18d ( 120 )` |
| #6 | **CRCL/USDT:USDT** | 🔴 Short | `562 ` | 2026-06-17 11:10 ➔ 2026-06-17 15:50 | 4h 40m | **-23.74%** | **-9.09 USDT** | `exit_short_universal_structural_cut ( 562 )` |
| #7 | **ZAMA/USDT:USDT** | 🟢 Long | `46 ` | 2026-10-29 23:25 ➔ 2026-10-29 23:55 | 30m | **-3.01%** | **-8.32 USDT** | `force_exit` |
| #8 | **QNT/USDT:USDT** | 🔴 Short | `562 ` | 2026-08-03 08:30 ➔ 2026-08-04 20:30 | 36h 0m | **-6.71%** | **-4.16 USDT** | `exit_ai_562_aged_breakeven ( 562 )` |
| #9 | **ETH/USDT:USDT** | 🔴 Short | `702 703 731_AI_PASS` | 2026-06-28 22:45 ➔ 2026-06-29 10:45 | 12h 0m | **-6.31%** | **-3.62 USDT** | `exit_ai_drift_decay ( 702 703 731_AI_PASS)` |
| #10 | **COIN/USDT:USDT** | 🔴 Short | `703 721 731_AI_PASS` | 2026-05-21 14:00 ➔ 2026-05-22 02:00 | 12h 0m | **-11.49%** | **-2.84 USDT** | `exit_ai_drift_decay ( 703 721 731_AI_PASS)` |

### ⏱️ Nhật Ký 15 Lệnh Giao Dịch Gần Nhất (Recent Trades Log)
| # | Cặp giao dịch | Vị thế | Enter Tag | Thời gian Đóng | Thời lượng | Lợi nhuận % | Lợi nhuận USDT | Lý do thoát |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| #1 | **XMR/USDT:USDT** | 🟢 Long | `64 ` | 2026-10-29 23:55 | 50m | **-8.27%** | **-24.17 USDT** | `force_exit` |
| #2 | **ZAMA/USDT:USDT** | 🟢 Long | `46 ` | 2026-10-29 23:55 | 30m | **-3.01%** | **-8.32 USDT** | `force_exit` |
| #3 | **OP/USDT:USDT** | 🔴 Short | `744_AI_PASS` | 2026-10-27 21:50 | 12h 0m | **-10.17%** | **-14.02 USDT** | `exit_ai_drift_decay ( 744_AI_PASS)` |
| #4 | **ARB/USDT:USDT** | 🔴 Short | `703 721 724 731_AI_PASS` | 2026-10-27 09:40 | 15m | **+2.29%** | **+7.24 USDT** | `exit_ai_profit_lock ( 703 721 724 731_AI_PASS)` |
| #5 | **FET/USDT:USDT** | 🔴 Short | `702 703 731_AI_PASS` | 2026-10-27 03:10 | 7h 5m | **+6.13%** | **+18.90 USDT** | `exit_ai_reversal_harvest ( 702 703 731_AI_PASS)` |
| #6 | **BTW/USDT:USDT** | 🟢 Long | `103 ` | 2026-10-26 21:45 | 2h 30m | **+25.41%** | **+48.09 USDT** | `exit_long_rapid_d_5_1 ( 103 )` |
| #7 | **CHIP/USDT:USDT** | 🔴 Short | `542 ` | 2026-10-26 18:40 | 1h 0m | **+8.67%** | **+16.29 USDT** | `exit_short_adaptive_trailing_scalp ( 542 )` |
| #8 | **WLD/USDT:USDT** | 🟢 Long | `141 ` | 2026-10-25 15:40 | 6h 45m | **+19.30%** | **+59.08 USDT** | `exit_long_tc_d_3_2 ( 141 )` |
| #9 | **BTW/USDT:USDT** | 🟢 Long | `2 ` | 2026-10-23 19:10 | 40m | **+38.38%** | **+68.53 USDT** | `exit_long_normal_d_7_1 ( 2 )` |
| #10 | **SAMSUNG/USDT:USDT** | 🔴 Short | `562 ` | 2026-10-23 00:15 | 11h 20m | **+10.74%** | **+24.36 USDT** | `exit_short_adaptive_trailing_scalp ( 562 )` |
| #11 | **SKHYNIX/USDT:USDT** | 🔴 Short | `562 ` | 2026-10-22 22:15 | 9h 20m | **+10.27%** | **+23.31 USDT** | `exit_short_adaptive_trailing_scalp ( 562 )` |
| #12 | **BTW/USDT:USDT** | 🟢 Long | `1 ` | 2026-10-22 21:40 | 55m | **+30.41%** | **+52.02 USDT** | `exit_long_normal_d_6_1 ( 1 )` |
| #13 | **BTW/USDT:USDT** | 🟢 Long | `1 ` | 2026-10-22 20:30 | 5m | **+6.42%** | **+10.93 USDT** | `exit_long_normal_u_1 ( 1 )` |
| #14 | **BTW/USDT:USDT** | 🟢 Long | `44 ` | 2026-10-20 09:30 | 1h 0m | **+22.21%** | **+37.19 USDT** | `exit_long_quick_q_9 ( 44 )` |
| #15 | **COIN/USDT:USDT** | 🔴 Short | `562 ` | 2026-10-20 03:10 | 53h 45m | **+10.44%** | **+17.64 USDT** | `exit_short_adaptive_trailing_scalp ( 562 )` |

---
*Báo cáo được khởi tạo tự động bởi `scripts/export_report.py` phục vụ chu trình Tối ưu hóa Tự động Agentic AI.*
