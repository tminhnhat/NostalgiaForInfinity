# 📈 Báo Cáo Đánh Giá Hiệu Suất Backtest Toàn Diện (Comprehensive Quantitative Report)

| Thông Tin Phiên Chạy | Chi Tiết | Đánh Dấu / Định Danh |
| :--- | :--- | :--- |
| 🏷️ **Phiên bản Chiến lược (Version)** | **`v7.4`** | `v7.4` |
| 🔖 **Git Commit** | `23648d8` | `fix(eval): auto-detect strategy version from code in workflow and prevent stale git describe tag fallback` |
| 🚀 **Đánh dấu lần chạy (Run Marker)** | **[v7.4-23648d80a-run-18](https://github.com/tminhnhat/NostalgiaForInfinity/actions/runs/41184027227)** | `Workflow #18` |
| 🤖 **Chiến lược (Strategy)** | `NostalgiaForInfinityX8_Combined_AI` | `Combined AI Engine` |
| 📅 **Thời gian đánh giá (Evaluation Date)** | `2026-10-31 08:26:05 UTC` | `UTC` |
| ⏱️ **Cửa sổ Backtest (Timerange)** | `20260504-20261031` | `176 ngày` |
| 📁 **Tệp kết quả (Source File)** | `backtest-result-2026-10-31_08-26-03.zip` | `Binance Futures 5m` |

---

## ⚖️ So Sánh Hiệu Suất Với Lần Backtest Trước (Benchmark Comparison)

| Chỉ số định lượng | Lần chạy này [v7.4-23648d80a-run-18 - 23648d8] | Lần trước [v7.4-5f68de4 - 5f68de4] | Chênh lệch (Δ Delta) | Xu hướng |
| :--- | :--- | :--- | :--- | :--- |
| **Tỷ lệ thắng (Winrate)** | **95.73%** | **96.61%** | `-0.88%` | 🔴 Suy giảm |
| **Lợi nhuận ròng (Net Profit %)** | **+1091.27%** | **+1160.20%** | `-68.93%` | 🔴 Suy giảm |
| **Lợi nhuận tuyệt đối (USDT)** | **+2,182.53 USDT** | **+2,320.39 USDT** | `-137.86 USDT` | 🔴 Suy giảm |
| **Hệ số Sharpe (Sharpe Ratio)** | **15.36** | **15.12** | `+0.24` | 🟢 Cải thiện |
| **Hệ số Sortino (Sortino Ratio)** | **15.85** | **14.79** | `+1.06` | 🟢 Cải thiện |
| **Sụt giảm tối đa (Max Drawdown %)** | **2.38%** | **2.38%** | 0.00% | ⚪ Tương đương |
| **Hệ số lãi/lỗ (Profit Factor)** | **17.46** | **16.04** | `+1.43` | 🟢 Cải thiện |
| **Tổng số lệnh (Total Trades)** | **234** | **236** | `-2.00 lệnh` | 🔴 Suy giảm |
| **Chuỗi lệnh thua dài nhất** | **2 trades** | **1 trades** | `+1.00 lệnh` | 🔴 Suy giảm |
| **Kỳ vọng toán học (Expectancy)** | **9.3271** | **9.8322** | `-0.51` | 🔴 Suy giảm |
| **Hệ số Calmar (Calmar Ratio)** | **4984.26** | **5239.52** | `-255.26` | 🔴 Suy giảm |

---

## 🏛️ Ma Trận Lịch Sử Đối Soát Giữa Các Lần Chạy (Multi-Run Version History Matrix)

> *Bảng tổng hợp đối chiếu kết quả backtest qua từng phiên bản và lần chạy để tiện theo dõi tiến trình tối ưu hóa.*

| Đánh dấu lần chạy (Run Marker) | Phiên bản | Commit | Ngày chạy | Tỷ lệ thắng (Winrate) | Lợi nhuận ròng | Max DD % | Sharpe | Profit Factor | Tổng lệnh | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `v7.2-latest-180d-101pairs` | **`v7.2`** | `d003c7e` | 20261028 | **84.77%** | +1,847.60 USDT (+923.8%) | 6.57% | 14.53 | 2.97 | `440` | ⚪ Đã lưu |
| `v7.2-a5dc0a8` | **`v7.2`** | `a5dc0a8` | 20261028 | **84.77%** | +1,837.45 USDT (+918.7%) | 6.58% | 14.52 | 2.97 | `440` | ⚪ Đã lưu |
| `v7.2-a5dc0a8` | **`v7.2`** | `a5dc0a8` | 20261028 | **96.96%** | +2,329.34 USDT (+1164.7%) | 2.38% | 15.01 | 17.68 | `230` | ⚪ Đã lưu |
| `v7.3-a995ec9` | **`v7.3`** | `a995ec9` | 20261029 | **96.96%** | +2,318.05 USDT (+1159.0%) | 2.38% | 15.11 | 17.63 | `230` | ⚪ Đã lưu |
| `v7.3-a995ec9` | **`v7.3`** | `a995ec9` | 20261029 | **96.61%** | +2,330.07 USDT (+1165.0%) | 2.38% | 14.91 | 14.35 | `236` | ⚪ Đã lưu |
| `v7.4-2f4a055` | **`v7.4`** | `2f4a055` | 20261029 | **96.19%** | +1,951.64 USDT (+975.8%) | 10.92% | 14.33 | 11.94 | `236` | ⚪ Đã lưu |
| `v7.4-5f68de4` | **`v7.4`** | `5f68de4` | 20261029 | **96.61%** | +2,320.39 USDT (+1160.2%) | 2.38% | 15.12 | 16.04 | `236` | ⚪ Đã lưu |
| `v7.4-23648d80a-run-18` | **`v7.4`** | `23648d8` | 20261031 | **95.73%** | +2,182.53 USDT (+1091.3%) | 2.38% | 15.36 | 17.46 | `234` | 🎯 **HIỆN TẠI** |

---

## 🎯 Chỉ Số Hiệu Suất Cốt Lõi (Executive Performance Metrics)

| Chỉ số định lượng | Giá trị thực tế | Đánh giá Benchmark | Tiêu chuẩn chất lượng |
| :--- | :--- | :--- | :--- |
| **Tỷ lệ thắng (Winrate)** | **95.73%** | 🟢 Robust | Ngưỡng an toàn >= 70% |
| **Hệ số Sharpe (Sharpe Ratio)** | **15.36** | 🟢 Exceptional | Chuẩn Alpha quỹ >= 2.0 |
| **Hệ số Sortino (Sortino Ratio)** | **15.85** | 🟢 Excellent | Đo lường rủi ro sụt giảm âm |
| **Sụt giảm tài khoản tối đa (Max Drawdown %)** | **2.38%** | 🟢 Defended | Giới hạn rủi ro < 15% |
| **Sụt giảm tuyệt đối (Max Drawdown Abs)** | **+56.32 USDT** | 🟢 Đã kiểm soát | Độ sâu drawdown danh mục |
| **Hệ số lãi/lỗ (Profit Factor)** | **17.46** | 🟢 High | Chuẩn định lượng >= 1.5 |
| **Chuỗi thua dài nhất (Longest Loss Streak)** | **2 trades** | 🟢 Safe | Kiểm soát chuỗi sụt giảm |

---

## 📊 Chỉ Số Định Lượng Mở Rộng (Secondary Quantitative Indicators)

| Chỉ số định lượng | Kết quả | Mô tả & Ý nghĩa kỹ thuật |
| :--- | :--- | :--- |
| **Tổng số lệnh (Total Trades)** | `234` | Tổng số lệnh đã hoàn tất trong timerange |
| **Tổng lệnh thắng / hòa / thua** | `224` thắng / `0` hòa / `10` thua | Phân bổ kết quả các giao dịch |
| **Lợi nhuận ròng % (Net Profit %)** | `+1091.27%` | Tỷ lệ tăng trưởng toàn bộ tài khoản |
| **Lợi nhuận tuyệt đối (Net Profit Abs)** | `+2,182.53 USDT` | Lợi nhuận bằng tiền mặt (USDT) |
| **Lợi nhuận trung bình / lệnh** | `+9.33 USDT` | Hiệu quả trung bình mỗi lần vào lệnh |
| **Mật độ giao dịch (Trades Per Day)** | `1.33 lệnh / ngày` | Tần suất giao dịch bình quân |
| **Kỳ vọng toán học (Expectancy)** | `9.3271` | Lợi nhuận kỳ vọng trên mỗi 1 đơn vị rủi ro |
| **Hệ số Calmar (Calmar Ratio)** | `4984.26` | Tỷ lệ lợi nhuận trên sụt giảm vốn tối đa |
| **Tốc độ tăng trưởng kép (CAGR)** | `16941.00%` | Compound Annual Growth Rate quy năm |

---

## ⚔️ Thống Kê Phân Bổ Vị Thế (Long vs Short Performance)

| Vị thế (Position) | Số lệnh | Tỷ trọng | Tỷ lệ thắng (Winrate) | Lợi nhuận (USDT) | Lợi nhuận (%) | Đánh giá |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 **Lệnh Mua (Long)** | `163` | 69.7% | **99.39%** | **+1,984.07 USDT** | +2518.17% | 🟢 Vượt trội |
| 🔴 **Lệnh Bán (Short)** | `71` | 30.3% | **87.32%** | **+198.46 USDT** | +256.67% | 🟢 Vượt trội |
| 🌐 **Toàn bộ danh mục** | `234` | 100.0% | **95.73%** | **+2,182.53 USDT** | +1091.27% | 🎯 Hoàn tất |

## 🚪 Phân Tích Lý Do Thoát Lệnh (Exit Reason Breakdown)

| Lý do đóng lệnh (Exit Reason) | Số lệnh | Tỷ trọng | Tỷ lệ thắng (Winrate) | Lợi nhuận (USDT) |
| :--- | :--- | :--- | :--- | :--- |
| `TOTAL` | `234` | 100.0% | **95.7%** | +2,182.53 USDT |
| `exit_ai_reversal_harvest ( 702 703 731_AI_PASS)` | `17` | 7.3% | **100.0%** | +50.70 USDT |
| `exit_profit_long_rebuy_t_0_1_m ( 64 )` | `12` | 5.1% | **100.0%** | +37.03 USDT |
| `exit_short_adaptive_trailing_scalp ( 562 )` | `9` | 3.8% | **100.0%** | +98.37 USDT |
| `exit_profit_long_tc_t_0_1_m ( 142 )` | `7` | 3.0% | **100.0%** | +7.48 USDT |
| `exit_long_rebuy_d_6_1 ( 64 )` | `5` | 2.1% | **100.0%** | +205.56 USDT |
| `exit_long_rebuy_e_r ( 65 )` | `4` | 1.7% | **100.0%** | +34.92 USDT |
| `exit_ai_reversal_harvest ( 702 703 731 743_AI_PASS)` | `4` | 1.7% | **100.0%** | +13.76 USDT |
| `exit_profit_long_tc_t_0_1_m ( 143 )` | `4` | 1.7% | **100.0%** | +7.62 USDT |
| `exit_profit_long_tc_t_0_1_m ( 144 )` | `4` | 1.7% | **100.0%** | +7.05 USDT |
| `exit_long_quick_q_9 ( 44 )` | `3` | 1.3% | **100.0%** | +56.86 USDT |
| `exit_short_adaptive_trailing_scalp ( 542 )` | `3` | 1.3% | **100.0%** | +26.72 USDT |
| `exit_profit_long_tc_t_1_1_m ( 145 )` | `3` | 1.3% | **100.0%** | +17.03 USDT |
| `exit_long_normal_u_1 ( 2 )` | `3` | 1.3% | **100.0%** | +13.61 USDT |
| `exit_ai_reversal_harvest ( 744_AI_PASS)` | `3` | 1.3% | **100.0%** | +9.38 USDT |
| `exit_profit_long_tc_t_0_1_m ( 145 )` | `3` | 1.3% | **100.0%** | +8.92 USDT |
| `exit_profit_long_rebuy_t_0_1_m ( 62 )` | `3` | 1.3% | **100.0%** | +3.41 USDT |
| `exit_profit_short_rebuy_t_0_1_m ( 562 )` | `3` | 1.3% | **100.0%** | +3.21 USDT |
| `exit_long_normal_d_4_1 ( 2 )` | `2` | 0.9% | **100.0%** | +86.54 USDT |
| `exit_long_normal_d_7_1 ( 2 )` | `2` | 0.9% | **100.0%** | +70.60 USDT |
| `exit_long_rebuy_d_4_1 ( 65 )` | `2` | 0.9% | **100.0%** | +50.49 USDT |
| `exit_long_rebuy_d_4_1 ( 64 )` | `2` | 0.9% | **100.0%** | +31.94 USDT |
| `exit_short_rebuy_1_1_1 ( 562 )` | `2` | 0.9% | **100.0%** | +30.78 USDT |
| `exit_long_normal_d_6_1 ( 2 )` | `2` | 0.9% | **100.0%** | +23.61 USDT |
| `exit_long_rapid_rpd_2 ( 102 )` | `2` | 0.9% | **100.0%** | +16.50 USDT |
| `exit_long_tc_u_1 ( 141 )` | `2` | 0.9% | **100.0%** | +16.23 USDT |
| `exit_long_tc_d_5_1 ( 141 142 )` | `2` | 0.9% | **100.0%** | +10.06 USDT |
| `exit_long_tc_d_5_1 ( 142 )` | `2` | 0.9% | **100.0%** | +9.93 USDT |
| `exit_profit_long_scalp_t_1_1_m ( 163 )` | `2` | 0.9% | **100.0%** | +8.54 USDT |
| `exit_ai_reversal_harvest ( 703 721 731_AI_PASS)` | `2` | 0.9% | **100.0%** | +4.11 USDT |
| `exit_profit_long_tc_t_0_1_m ( 141 )` | `2` | 0.9% | **100.0%** | +4.11 USDT |
| `exit_profit_long_rebuy_t_0_1_m ( 61 )` | `2` | 0.9% | **100.0%** | +3.49 USDT |
| `exit_ai_profit_lock ( 702 703 731_AI_PASS)` | `2` | 0.9% | **100.0%** | +3.48 USDT |
| `exit_profit_long_scalp_t_0_1_m ( 163 )` | `2` | 0.9% | **100.0%** | +1.53 USDT |
| `exit_ai_profit_lock ( 744_AI_PASS)` | `2` | 0.9% | **100.0%** | +1.01 USDT |
| `exit_ai_early_structural_cut ( 702 703 731_AI_PASS)` | `2` | 0.9% | **0.0%** | -8.43 USDT |
| `exit_short_universal_structural_cut ( 562 )` | `2` | 0.9% | **0.0%** | -20.50 USDT |
| `exit_long_rebuy_d_7_1 ( 64 )` | `1` | 0.4% | **100.0%** | +81.70 USDT |
| `exit_long_rebuy_d_6_1 ( 62 )` | `1` | 0.4% | **100.0%** | +73.26 USDT |
| `exit_long_rebuy_2_1_1 ( 64 )` | `1` | 0.4% | **100.0%** | +71.16 USDT |
| `exit_long_quick_d_11_1 ( 43 )` | `1` | 0.4% | **100.0%** | +70.46 USDT |
| `exit_long_tc_d_3_2 ( 141 )` | `1` | 0.4% | **100.0%** | +55.29 USDT |
| `exit_long_normal_d_6_1 ( 1 )` | `1` | 0.4% | **100.0%** | +48.73 USDT |
| `exit_long_quick_q_6 ( 42 )` | `1` | 0.4% | **100.0%** | +44.70 USDT |
| `exit_long_rapid_d_5_1 ( 103 )` | `1` | 0.4% | **100.0%** | +43.90 USDT |
| `exit_long_rebuy_w_6_1 ( 64 )` | `1` | 0.4% | **100.0%** | +37.88 USDT |
| `exit_long_normal_d_7_1 ( 6 )` | `1` | 0.4% | **100.0%** | +35.49 USDT |
| `exit_long_rebuy_d_8_1 ( 64 )` | `1` | 0.4% | **100.0%** | +35.05 USDT |
| `exit_long_normal_d_4_1 ( 6 )` | `1` | 0.4% | **100.0%** | +34.75 USDT |
| `exit_long_tc_d_8_1 ( 142 )` | `1` | 0.4% | **100.0%** | +33.91 USDT |
| `exit_long_tc_d_3_1 ( 141 )` | `1` | 0.4% | **100.0%** | +31.74 USDT |
| `exit_long_tc_d_5_1 ( 141 )` | `1` | 0.4% | **100.0%** | +30.49 USDT |
| `exit_long_normal_u_3 ( 6 141 )` | `1` | 0.4% | **100.0%** | +25.58 USDT |
| `exit_long_tc_3_1_1 ( 141 142 )` | `1` | 0.4% | **100.0%** | +24.81 USDT |
| `exit_long_scalp_d_5_1 ( 163 )` | `1` | 0.4% | **100.0%** | +24.49 USDT |
| `exit_short_adaptive_trailing_mega ( 562 )` | `1` | 0.4% | **100.0%** | +23.66 USDT |
| `exit_long_rebuy_d_9_1 ( 65 )` | `1` | 0.4% | **100.0%** | +19.82 USDT |
| `exit_long_tc_d_6_1 ( 144 )` | `1` | 0.4% | **100.0%** | +16.87 USDT |
| `exit_profit_long_rebuy_t_7_1_m ( 63 )` | `1` | 0.4% | **100.0%** | +16.03 USDT |
| `exit_long_scalp_d_6_1 ( 61 162 )` | `1` | 0.4% | **100.0%** | +13.66 USDT |
| `exit_long_rebuy_d_8_1 ( 61 )` | `1` | 0.4% | **100.0%** | +13.53 USDT |
| `exit_long_rebuy_d_6_1 ( 63 )` | `1` | 0.4% | **100.0%** | +13.22 USDT |
| `exit_profit_long_normal_t_2_1_m ( 3 )` | `1` | 0.4% | **100.0%** | +12.87 USDT |
| `exit_long_quick_q_6 ( 47 )` | `1` | 0.4% | **100.0%** | +12.84 USDT |
| `exit_long_rebuy_d_6_1 ( 61 )` | `1` | 0.4% | **100.0%** | +12.65 USDT |
| `exit_ai_reversal_harvest ( 702 703 705 731_AI_PASS)` | `1` | 0.4% | **100.0%** | +12.54 USDT |
| `exit_long_tc_d_5_1 ( 145 )` | `1` | 0.4% | **100.0%** | +12.45 USDT |
| `exit_profit_long_tc_t_2_1_m ( 145 )` | `1` | 0.4% | **100.0%** | +12.17 USDT |
| `exit_long_scalp_d_6_1 ( 162 )` | `1` | 0.4% | **100.0%** | +11.95 USDT |
| `exit_long_tc_u_1 ( 141 142 )` | `1` | 0.4% | **100.0%** | +11.78 USDT |
| `exit_profit_long_tc_t_2_1_m ( 142 )` | `1` | 0.4% | **100.0%** | +11.69 USDT |
| `exit_profit_short_rebuy_t_1_1_m ( 562 )` | `1` | 0.4% | **100.0%** | +11.41 USDT |
| `exit_long_tc_u_1 ( 142 )` | `1` | 0.4% | **100.0%** | +11.41 USDT |
| `exit_long_quick_d_7_1 ( 42 )` | `1` | 0.4% | **100.0%** | +11.02 USDT |
| `exit_profit_long_quick_t_2_1_m ( 46 )` | `1` | 0.4% | **100.0%** | +10.99 USDT |
| `exit_long_normal_u_1 ( 1 )` | `1` | 0.4% | **100.0%** | +10.23 USDT |
| `exit_long_normal_d_3_2 ( 5 )` | `1` | 0.4% | **100.0%** | +9.96 USDT |
| `exit_long_tc_d_6_1 ( 141 )` | `1` | 0.4% | **100.0%** | +9.38 USDT |
| `exit_long_rebuy_d_5_1 ( 63 )` | `1` | 0.4% | **100.0%** | +9.23 USDT |
| `exit_long_normal_d_4_1 ( 1 )` | `1` | 0.4% | **100.0%** | +8.84 USDT |
| `exit_long_tc_d_6_1 ( 141 143 163 )` | `1` | 0.4% | **100.0%** | +8.36 USDT |
| `exit_profit_long_normal_t_1_1_m ( 3 )` | `1` | 0.4% | **100.0%** | +8.16 USDT |
| `exit_profit_long_tc_t_1_1_m ( 141 )` | `1` | 0.4% | **100.0%** | +8.04 USDT |
| `exit_profit_long_tc_t_1_1_m ( 141 142 )` | `1` | 0.4% | **100.0%** | +7.81 USDT |
| `exit_long_tc_d_4_2 ( 145 )` | `1` | 0.4% | **100.0%** | +7.37 USDT |
| `exit_long_tc_d_6_1 ( 142 )` | `1` | 0.4% | **100.0%** | +7.20 USDT |
| `exit_profit_long_rebuy_t_3_1_m ( 61 )` | `1` | 0.4% | **100.0%** | +6.88 USDT |
| `exit_long_tc_d_5_1 ( 62 144 )` | `1` | 0.4% | **100.0%** | +6.84 USDT |
| `exit_long_normal_d_8_1 ( 4 )` | `1` | 0.4% | **100.0%** | +6.84 USDT |
| `exit_long_normal_u_4 ( 1 61 )` | `1` | 0.4% | **100.0%** | +6.74 USDT |
| `exit_ai_profit_lock ( 703 721 724 731_AI_PASS)` | `1` | 0.4% | **100.0%** | +6.62 USDT |
| `exit_long_normal_d_7_1 ( 2 101 141 )` | `1` | 0.4% | **100.0%** | +6.52 USDT |
| `exit_long_normal_d_5_1 ( 2 )` | `1` | 0.4% | **100.0%** | +6.17 USDT |
| `exit_profit_long_rebuy_t_2_1_m ( 65 )` | `1` | 0.4% | **100.0%** | +6.16 USDT |
| `exit_profit_long_normal_t_0_1_m ( 2 )` | `1` | 0.4% | **100.0%** | +5.71 USDT |
| `exit_long_tc_d_5_1 ( 144 )` | `1` | 0.4% | **100.0%** | +5.61 USDT |
| `exit_long_normal_d_5_1 ( 6 102 141 )` | `1` | 0.4% | **100.0%** | +5.52 USDT |
| `exit_long_tc_d_3_2 ( 102 142 )` | `1` | 0.4% | **100.0%** | +5.18 USDT |
| `exit_profit_long_rapid_t_1_1_m ( 102 )` | `1` | 0.4% | **100.0%** | +5.06 USDT |
| `exit_long_normal_d_5_1 ( 5 )` | `1` | 0.4% | **100.0%** | +4.97 USDT |
| `exit_profit_long_tc_t_0_1_m ( 141 142 )` | `1` | 0.4% | **100.0%** | +4.80 USDT |
| `exit_long_normal_d_6_1 ( 2 141 )` | `1` | 0.4% | **100.0%** | +4.66 USDT |
| `exit_ai_reversal_harvest ( 743 744_AI_PASS)` | `1` | 0.4% | **100.0%** | +4.50 USDT |
| `exit_long_quick_q_2 ( 41 )` | `1` | 0.4% | **100.0%** | +4.26 USDT |
| `exit_long_rapid_rpd_6 ( 102 )` | `1` | 0.4% | **100.0%** | +4.15 USDT |
| `exit_profit_long_tc_t_3_1_m ( 143 )` | `1` | 0.4% | **100.0%** | +3.79 USDT |
| `exit_long_normal_u_2 ( 4 41 61 )` | `1` | 0.4% | **100.0%** | +3.77 USDT |
| `exit_long_rebuy_u_1 ( 61 )` | `1` | 0.4% | **100.0%** | +3.64 USDT |
| `exit_profit_long_rebuy_t_2_1_m ( 62 )` | `1` | 0.4% | **100.0%** | +3.39 USDT |
| `exit_profit_long_rebuy_t_1_1_m ( 62 )` | `1` | 0.4% | **100.0%** | +3.36 USDT |
| `exit_long_normal_w_1_1 ( 1 )` | `1` | 0.4% | **100.0%** | +3.24 USDT |
| `exit_ai_reversal_harvest ( 721 724 741_AI_PASS)` | `1` | 0.4% | **100.0%** | +3.01 USDT |
| `exit_short_rebuy_u_1 ( 562 )` | `1` | 0.4% | **100.0%** | +2.84 USDT |
| `exit_profit_long_normal_t_0_1_m ( 6 102 )` | `1` | 0.4% | **100.0%** | +2.81 USDT |
| `exit_ai_reversal_harvest ( 721 724 731_AI_PASS)` | `1` | 0.4% | **100.0%** | +2.66 USDT |
| `exit_ai_profit_lock ( 702 703 706 731 743_AI_PASS)` | `1` | 0.4% | **100.0%** | +2.59 USDT |
| `exit_ai_reversal_harvest ( 702 731 743_AI_PASS)` | `1` | 0.4% | **100.0%** | +2.39 USDT |
| `exit_long_normal_u_2 ( 2 )` | `1` | 0.4% | **100.0%** | +2.32 USDT |
| `exit_ai_reversal_harvest ( 702 703 724 731_AI_PASS)` | `1` | 0.4% | **100.0%** | +2.24 USDT |
| `exit_profit_long_normal_t_0_1_m ( 6 )` | `1` | 0.4% | **100.0%** | +1.87 USDT |
| `exit_profit_long_scalp_t_2_1_m ( 163 )` | `1` | 0.4% | **100.0%** | +1.86 USDT |
| `exit_short_adaptive_trailing_scalp ( 702 703 731_AI_PASS)` | `1` | 0.4% | **100.0%** | +1.80 USDT |
| `exit_long_quick_u_1 ( 43 )` | `1` | 0.4% | **100.0%** | +1.71 USDT |
| `exit_profit_long_normal_t_2_1_m ( 2 63 101 )` | `1` | 0.4% | **100.0%** | +1.66 USDT |
| `exit_ai_reversal_harvest ( 731 743_AI_PASS)` | `1` | 0.4% | **100.0%** | +1.63 USDT |
| `exit_profit_long_scalp_t_0_1_m ( 161 )` | `1` | 0.4% | **100.0%** | +1.62 USDT |
| `exit_long_tc_u_1 ( 144 )` | `1` | 0.4% | **100.0%** | +1.51 USDT |
| `exit_profit_long_normal_t_0_1_m ( 3 )` | `1` | 0.4% | **100.0%** | +1.45 USDT |
| `exit_profit_long_quick_t_1_1_m ( 42 )` | `1` | 0.4% | **100.0%** | +1.20 USDT |
| `exit_profit_long_rapid_t_0_1_m ( 102 )` | `1` | 0.4% | **100.0%** | +1.05 USDT |
| `exit_profit_long_scalp_t_0_1_m ( 162 )` | `1` | 0.4% | **100.0%** | +0.96 USDT |
| `exit_profit_long_quick_t_0_1_m ( 43 )` | `1` | 0.4% | **100.0%** | +0.77 USDT |
| `exit_ai_profit_lock ( 702 703 731 743_AI_PASS)` | `1` | 0.4% | **100.0%** | +0.49 USDT |
| `exit_long_normal_w_0_1 ( 3 )` | `1` | 0.4% | **100.0%** | +0.37 USDT |
| `exit_ai_profit_lock ( 703 705 706 731_AI_PASS)` | `1` | 0.4% | **100.0%** | +0.36 USDT |
| `exit_profit_long_normal_t_0_1_m ( 5 )` | `1` | 0.4% | **100.0%** | +0.33 USDT |
| `exit_profit_long_normal_t_0_1_m ( 3 142 )` | `1` | 0.4% | **100.0%** | +0.14 USDT |
| `exit_ai_early_structural_cut ( 724 731_AI_PASS)` | `1` | 0.4% | **0.0%** | -3.60 USDT |
| `exit_ai_562_aged_breakeven ( 562 )` | `1` | 0.4% | **0.0%** | -3.92 USDT |
| `exit_bad_trade_abandon_18d ( 120 )` | `1` | 0.4% | **0.0%** | -10.77 USDT |
| `force_exit` | `1` | 0.4% | **0.0%** | -13.61 USDT |
| `exit_short_universal_structural_cut ( 542 )` | `1` | 0.4% | **0.0%** | -15.42 USDT |
| `exit_ai_early_structural_cut ( 703 721 724 731_AI_PASS)` | `1` | 0.4% | **0.0%** | -56.32 USDT |

## 🔍 Bảng Phân Tích Đầy Đủ Tất Cả Các Entry Tags (Full Enter Tag Breakdown)

> *Bảng tổng hợp chi tiết 100% tất cả các tag tín hiệu vào lệnh (Entry Tags) đã hoạt động trong phiên backtest.*

| Enter Tag | Vị thế | Số lệnh | Tỷ lệ thắng (Winrate) | Thắng/Hòa/Thua | Tổng LN % | Tổng LN (USDT) | LN TB/Lệnh | Thời lượng TB | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `TOTAL` | 🟢 Long Core | `234` | **95.7%** | 224/0/10 | +1091.27% | **+2,182.53 USDT** | +11.86% | 11:15:00 | 🟢 Tối ưu |
| `64` | 🟢 Long Core | `23` | **100.0%** | 23/0/0 | +250.16% | **+500.31 USDT** | +18.81% | 10:14:00 | 🟢 Tối ưu |
| `2` | 🟢 Long Core | `12` | **100.0%** | 12/0/0 | +104.28% | **+208.57 USDT** | +20.29% | 2:08:00 | 🟢 Tối ưu |
| `141` | 🟢 Long Core | `9` | **100.0%** | 9/0/0 | +77.64% | **+155.27 USDT** | +13.21% | 9:31:00 | 🟢 Tối ưu |
| `562` | 🟢 Long Core | `20` | **85.0%** | 17/0/3 | +72.92% | **+145.85 USDT** | +5.75% | 1 day, 4:38:00 | 🟢 Tối ưu |
| `65` | 🟢 Long Core | `8` | **100.0%** | 8/0/0 | +55.69% | **+111.39 USDT** | +19.27% | 2:26:00 | 🟢 Tối ưu |
| `62` | 🟢 Long Core | `6` | **100.0%** | 6/0/0 | +41.71% | **+83.42 USDT** | +8.40% | 14:27:00 | 🟢 Tối ưu |
| `142` | 🟢 Long Core | `13` | **100.0%** | 13/0/0 | +40.80% | **+81.61 USDT** | +11.81% | 8:32:00 | 🟢 Tối ưu |
| `43` | 🟢 Long Core | `3` | **100.0%** | 3/0/0 | +36.47% | **+72.94 USDT** | +26.00% | 0:35:00 | 🟢 Tối ưu |
| `6` | 🟢 Long Core | `3` | **100.0%** | 3/0/0 | +36.05% | **+72.11 USDT** | +18.75% | 17:13:00 | 🟢 Tối ưu |
| `1` | 🟢 Long Core | `4` | **100.0%** | 4/0/0 | +35.52% | **+71.04 USDT** | +12.27% | 1 day, 20:39:00 | 🟢 Tối ưu |
| `141 142` | 🟢 Long Core | `6` | **100.0%** | 6/0/0 | +29.63% | **+59.25 USDT** | +13.96% | 9:57:00 | 🟢 Tối ưu |
| `145` | 🟢 Long Core | `9` | **100.0%** | 9/0/0 | +28.97% | **+57.95 USDT** | +10.60% | 8:46:00 | 🟢 Tối ưu |
| `42` | 🟢 Long Core | `3` | **100.0%** | 3/0/0 | +28.46% | **+56.92 USDT** | +22.44% | 1:15:00 | 🟢 Tối ưu |
| `44` | 🟢 Long Core | `3` | **100.0%** | 3/0/0 | +28.43% | **+56.86 USDT** | +22.49% | 2:32:00 | 🟢 Tối ưu |
| `702 703 731_AI_PASS` | 🤖 Short AI Gatekeeper | `22` | **90.9%** | 20/0/2 | +23.78% | **+47.56 USDT** | +3.47% | 4:57:00 | 🟢 Tối ưu |
| `103` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +21.95% | **+43.90 USDT** | +25.41% | 2:30:00 | 🟢 Tối ưu |
| `61` | 🟢 Long Core | `6` | **100.0%** | 6/0/0 | +20.09% | **+40.19 USDT** | +18.80% | 1:51:00 | 🟢 Tối ưu |
| `63` | 🟢 Long Core | `3` | **100.0%** | 3/0/0 | +19.24% | **+38.48 USDT** | +33.10% | 3:02:00 | 🟢 Tối ưu |
| `163` | 🟢 Long Core | `6` | **100.0%** | 6/0/0 | +18.21% | **+36.42 USDT** | +9.34% | 2:25:00 | 🟢 Tối ưu |
| `144` | 🟢 Long Core | `7` | **100.0%** | 7/0/0 | +15.52% | **+31.04 USDT** | +11.67% | 12:41:00 | 🟢 Tối ưu |
| `102` | 🟢 Long Core | `5` | **100.0%** | 5/0/0 | +13.39% | **+26.77 USDT** | +5.32% | 2:58:00 | 🟢 Tối ưu |
| `6 141` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +12.79% | **+25.58 USDT** | +16.21% | 19:20:00 | 🟢 Tối ưu |
| `3` | 🟢 Long Core | `4` | **100.0%** | 4/0/0 | +11.42% | **+22.85 USDT** | +5.20% | 19:42:00 | 🟢 Tối ưu |
| `5` | 🟢 Long Core | `3` | **100.0%** | 3/0/0 | +7.63% | **+15.26 USDT** | +14.52% | 3:03:00 | 🟢 Tối ưu |
| `702 703 731 743_AI_PASS` | 🤖 Short AI Gatekeeper | `5` | **100.0%** | 5/0/0 | +7.12% | **+14.25 USDT** | +5.30% | 3:34:00 | 🟢 Tối ưu |
| `61 162` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +6.83% | **+13.66 USDT** | +32.22% | 4:05:00 | 🟢 Tối ưu |
| `162` | 🟢 Long Core | `2` | **100.0%** | 2/0/0 | +6.46% | **+12.91 USDT** | +17.33% | 0:52:00 | 🟢 Tối ưu |
| `47` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +6.42% | **+12.84 USDT** | +13.38% | 1 day, 2:00:00 | 🟢 Tối ưu |
| `702 703 705 731_AI_PASS` | 🤖 Short AI Gatekeeper | `1` | **100.0%** | 1/0/0 | +6.27% | **+12.54 USDT** | +6.15% | 7:45:00 | 🟢 Tối ưu |
| `143` | 🟢 Long Core | `5` | **100.0%** | 5/0/0 | +5.71% | **+11.42 USDT** | +5.30% | 18:36:00 | 🟢 Tối ưu |
| `542` | 🟢 Long Core | `4` | **75.0%** | 3/0/1 | +5.65% | **+11.30 USDT** | +1.59% | 1:24:00 | 🟡 Hiệu quả |
| `46` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +5.49% | **+10.99 USDT** | +11.97% | 0:45:00 | 🟢 Tối ưu |
| `141 143 163` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +4.18% | **+8.36 USDT** | +33.41% | 1:30:00 | 🟢 Tối ưu |
| `62 144` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +3.42% | **+6.84 USDT** | +25.85% | 1:25:00 | 🟢 Tối ưu |
| `4` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +3.42% | **+6.84 USDT** | +44.22% | 1:10:00 | 🟢 Tối ưu |
| `1 61` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +3.37% | **+6.74 USDT** | +21.38% | 0:15:00 | 🟢 Tối ưu |
| `2 101 141` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +3.26% | **+6.52 USDT** | +36.21% | 1:00:00 | 🟢 Tối ưu |
| `6 102 141` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +2.76% | **+5.52 USDT** | +26.17% | 1:00:00 | 🟢 Tối ưu |
| `102 142` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +2.59% | **+5.18 USDT** | +19.97% | 1:40:00 | 🟢 Tối ưu |
| `2 141` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +2.33% | **+4.66 USDT** | +30.19% | 2:15:00 | 🟢 Tối ưu |
| `743 744_AI_PASS` | 🤖 Short AI Gatekeeper | `1` | **100.0%** | 1/0/0 | +2.25% | **+4.50 USDT** | +5.77% | 0:30:00 | 🟢 Tối ưu |
| `41` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +2.13% | **+4.26 USDT** | +11.69% | 5:00:00 | 🟢 Tối ưu |
| `703 721 731_AI_PASS` | 🤖 Short AI Gatekeeper | `2` | **100.0%** | 2/0/0 | +2.05% | **+4.11 USDT** | +5.50% | 14:42:00 | 🟢 Tối ưu |
| `4 41 61` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +1.89% | **+3.77 USDT** | +11.78% | 0:10:00 | 🟢 Tối ưu |
| `721 724 741_AI_PASS` | 🤖 Short AI Gatekeeper | `1` | **100.0%** | 1/0/0 | +1.51% | **+3.01 USDT** | +5.01% | 7:05:00 | 🟢 Tối ưu |
| `6 102` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +1.40% | **+2.81 USDT** | +1.43% | 2:05:00 | 🟢 Tối ưu |
| `721 724 731_AI_PASS` | 🤖 Short AI Gatekeeper | `1` | **100.0%** | 1/0/0 | +1.33% | **+2.66 USDT** | +6.65% | 17:10:00 | 🟢 Tối ưu |
| `702 703 706 731 743_AI_PASS` | 🤖 Short AI Gatekeeper | `1` | **100.0%** | 1/0/0 | +1.30% | **+2.59 USDT** | +1.60% | 0:45:00 | 🟢 Tối ưu |
| `702 731 743_AI_PASS` | 🤖 Short AI Gatekeeper | `1` | **100.0%** | 1/0/0 | +1.19% | **+2.39 USDT** | +6.75% | 9:05:00 | 🟢 Tối ưu |
| `702 703 724 731_AI_PASS` | 🤖 Short AI Gatekeeper | `1` | **100.0%** | 1/0/0 | +1.12% | **+2.24 USDT** | +6.01% | 0:25:00 | 🟢 Tối ưu |
| `2 63 101` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +0.83% | **+1.66 USDT** | +10.72% | 2:55:00 | 🟢 Tối ưu |
| `731 743_AI_PASS` | 🤖 Short AI Gatekeeper | `1` | **100.0%** | 1/0/0 | +0.82% | **+1.63 USDT** | +5.56% | 2:40:00 | 🟢 Tối ưu |
| `161` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +0.81% | **+1.62 USDT** | +3.08% | 12:05:00 | 🟢 Tối ưu |
| `703 705 706 731_AI_PASS` | 🤖 Short AI Gatekeeper | `1` | **100.0%** | 1/0/0 | +0.18% | **+0.36 USDT** | +1.92% | 6:05:00 | 🟢 Tối ưu |
| `3 142` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +0.07% | **+0.14 USDT** | +0.50% | 19:15:00 | 🟢 Tối ưu |
| `744_AI_PASS` | 🤖 Short AI Gatekeeper | `6` | **83.3%** | 5/0/1 | -1.61% | **-3.23 USDT** | +2.01% | 4:21:00 | 🔴 Cần tinh chỉnh |
| `724 731_AI_PASS` | 🤖 Short AI Gatekeeper | `1` | **0.0%** | 0/0/1 | -1.80% | **-3.60 USDT** | -18.56% | 9:25:00 | 🔴 Cần tinh chỉnh |
| `120` | 🟢 Long Core | `1` | **0.0%** | 0/0/1 | -5.38% | **-10.77 USDT** | -10.04% | 17 days, 22:40:00 | 🔴 Cần tinh chỉnh |
| `703 721 724 731_AI_PASS` | 🤖 Short AI Gatekeeper | `2` | **50.0%** | 1/0/1 | -24.85% | **-49.71 USDT** | -8.68% | 3:45:00 | 🔴 Cần tinh chỉnh |

---

## 📑 Chi Tiết Các Lệnh Giao Dịch (Trade Execution Journal)

### 🥇 Top 10 Lệnh Lãi Cao Nhất (Top Winning Trades)
| # | Cặp giao dịch | Vị thế | Enter Tag | Thời gian Mở ➔ Đóng | Thời lượng | Lợi nhuận % | Lợi nhuận USDT | Lý do thoát |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| #1 | **BAT/USDT:USDT** | 🟢 Long | `64 ` | 2026-10-08 08:20 ➔ 2026-10-09 06:05 | 21h 45m | **+43.38%** | **+81.70 USDT** | `exit_long_rebuy_d_7_1 ( 64 )` |
| #2 | **GRASS/USDT:USDT** | 🟢 Long | `62 ` | 2026-10-14 17:45 ➔ 2026-10-15 15:05 | 21h 20m | **+33.86%** | **+73.26 USDT** | `exit_long_rebuy_d_6_1 ( 62 )` |
| #3 | **ARB/USDT:USDT** | 🟢 Long | `64 ` | 2026-09-17 21:45 ➔ 2026-09-18 01:50 | 4h 5m | **+59.20%** | **+71.16 USDT** | `exit_long_rebuy_2_1_1 ( 64 )` |
| #4 | **BTW/USDT:USDT** | 🟢 Long | `43 ` | 2026-10-05 06:45 ➔ 2026-10-05 08:05 | 1h 20m | **+71.12%** | **+70.46 USDT** | `exit_long_quick_d_11_1 ( 43 )` |
| #5 | **BTW/USDT:USDT** | 🟢 Long | `2 ` | 2026-10-23 18:30 ➔ 2026-10-23 19:10 | 40m | **+38.38%** | **+64.07 USDT** | `exit_long_normal_d_7_1 ( 2 )` |
| #6 | **GRASS/USDT:USDT** | 🟢 Long | `64 ` | 2026-10-05 14:55 ➔ 2026-10-05 19:15 | 4h 20m | **+32.17%** | **+55.96 USDT** | `exit_long_rebuy_d_6_1 ( 64 )` |
| #7 | **WLD/USDT:USDT** | 🟢 Long | `141 ` | 2026-10-25 08:55 ➔ 2026-10-25 15:40 | 6h 45m | **+19.30%** | **+55.29 USDT** | `exit_long_tc_d_3_2 ( 141 )` |
| #8 | **BAT/USDT:USDT** | 🟢 Long | `64 ` | 2026-10-03 06:15 ➔ 2026-10-04 07:40 | 25h 25m | **+33.11%** | **+52.24 USDT** | `exit_long_rebuy_d_6_1 ( 64 )` |
| #9 | **BTW/USDT:USDT** | 🟢 Long | `1 ` | 2026-10-22 20:45 ➔ 2026-10-22 21:40 | 55m | **+30.41%** | **+48.73 USDT** | `exit_long_normal_d_6_1 ( 1 )` |
| #10 | **QNT/USDT:USDT** | 🟢 Long | `2 ` | 2026-10-13 11:10 ➔ 2026-10-13 18:40 | 7h 30m | **+24.34%** | **+46.13 USDT** | `exit_long_normal_d_4_1 ( 2 )` |

### ⚠️ Top Lệnh Thua Lỗ / Sụt Giảm Lớn Nhất (Top Drawdown Trades)
| # | Cặp giao dịch | Vị thế | Enter Tag | Thời gian Mở ➔ Đóng | Thời lượng | Thua lỗ % | Thua lỗ USDT | Lý do thoát |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| #1 | **NXPC/USDT:USDT** | 🔴 Short | `703 721 724 731_AI_PASS` | 2026-10-26 07:05 ➔ 2026-10-26 14:20 | 7h 15m | **-19.66%** | **-56.32 USDT** | `exit_ai_early_structural_cut ( 703 721 724 731_AI_PASS)` |
| #2 | **MVLL/USDT:USDT** | 🔴 Short | `542 ` | 2026-08-20 17:15 ➔ 2026-08-20 20:05 | 2h 50m | **-23.02%** | **-15.42 USDT** | `exit_short_universal_structural_cut ( 542 )` |
| #3 | **OP/USDT:USDT** | 🔴 Short | `744_AI_PASS` | 2026-10-27 09:50 ➔ 2026-10-27 23:55 | 14h 5m | **-10.81%** | **-13.61 USDT** | `force_exit` |
| #4 | **ZEC/USDT:USDT** | 🔴 Short | `562 ` | 2026-07-29 03:35 ➔ 2026-07-30 05:50 | 26h 15m | **-22.91%** | **-12.01 USDT** | `exit_short_universal_structural_cut ( 562 )` |
| #5 | **RENDER/USDT:USDT** | 🟢 Long | `120 ` | 2026-06-04 01:20 ➔ 2026-06-22 00:00 | 430h 40m | **-10.04%** | **-10.77 USDT** | `exit_bad_trade_abandon_18d ( 120 )` |
| #6 | **CRCL/USDT:USDT** | 🔴 Short | `562 ` | 2026-06-17 11:10 ➔ 2026-06-17 15:50 | 4h 40m | **-23.74%** | **-8.49 USDT** | `exit_short_universal_structural_cut ( 562 )` |
| #7 | **ZEC/USDT:USDT** | 🔴 Short | `702 703 731_AI_PASS` | 2026-05-07 21:20 ➔ 2026-05-07 23:25 | 2h 5m | **-17.83%** | **-4.40 USDT** | `exit_ai_early_structural_cut ( 702 703 731_AI_PASS)` |
| #8 | **1000PEPE/USDT:USDT** | 🔴 Short | `702 703 731_AI_PASS` | 2026-05-07 22:05 ➔ 2026-05-08 16:00 | 17h 55m | **-20.34%** | **-4.02 USDT** | `exit_ai_early_structural_cut ( 702 703 731_AI_PASS)` |
| #9 | **QNT/USDT:USDT** | 🔴 Short | `562 ` | 2026-08-03 08:30 ➔ 2026-08-04 20:30 | 36h 0m | **-6.71%** | **-3.92 USDT** | `exit_ai_562_aged_breakeven ( 562 )` |
| #10 | **BAT/USDT:USDT** | 🔴 Short | `724 731_AI_PASS` | 2026-05-08 08:10 ➔ 2026-05-08 17:35 | 9h 25m | **-18.56%** | **-3.60 USDT** | `exit_ai_early_structural_cut ( 724 731_AI_PASS)` |

### ⏱️ Nhật Ký 15 Lệnh Giao Dịch Gần Nhất (Recent Trades Log)
| # | Cặp giao dịch | Vị thế | Enter Tag | Thời gian Đóng | Thời lượng | Lợi nhuận % | Lợi nhuận USDT | Lý do thoát |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| #1 | **OP/USDT:USDT** | 🔴 Short | `744_AI_PASS` | 2026-10-27 23:55 | 14h 5m | **-10.81%** | **-13.61 USDT** | `force_exit` |
| #2 | **ARB/USDT:USDT** | 🔴 Short | `703 721 724 731_AI_PASS` | 2026-10-27 09:40 | 15m | **+2.29%** | **+6.62 USDT** | `exit_ai_profit_lock ( 703 721 724 731_AI_PASS)` |
| #3 | **FET/USDT:USDT** | 🔴 Short | `702 703 731_AI_PASS` | 2026-10-27 03:10 | 7h 5m | **+6.13%** | **+17.27 USDT** | `exit_ai_reversal_harvest ( 702 703 731_AI_PASS)` |
| #4 | **BTW/USDT:USDT** | 🟢 Long | `103 ` | 2026-10-26 21:45 | 2h 30m | **+25.41%** | **+43.90 USDT** | `exit_long_rapid_d_5_1 ( 103 )` |
| #5 | **CHIP/USDT:USDT** | 🔴 Short | `542 ` | 2026-10-26 18:40 | 1h 0m | **+8.67%** | **+14.88 USDT** | `exit_short_adaptive_trailing_scalp ( 542 )` |
| #6 | **NXPC/USDT:USDT** | 🔴 Short | `703 721 724 731_AI_PASS` | 2026-10-26 14:20 | 7h 15m | **-19.66%** | **-56.32 USDT** | `exit_ai_early_structural_cut ( 703 721 724 731_AI_PASS)` |
| #7 | **WLD/USDT:USDT** | 🟢 Long | `141 ` | 2026-10-25 15:40 | 6h 45m | **+19.30%** | **+55.29 USDT** | `exit_long_tc_d_3_2 ( 141 )` |
| #8 | **BTW/USDT:USDT** | 🟢 Long | `2 ` | 2026-10-23 19:10 | 40m | **+38.38%** | **+64.07 USDT** | `exit_long_normal_d_7_1 ( 2 )` |
| #9 | **SAMSUNG/USDT:USDT** | 🔴 Short | `562 ` | 2026-10-23 00:15 | 11h 20m | **+10.74%** | **+22.81 USDT** | `exit_short_adaptive_trailing_scalp ( 562 )` |
| #10 | **SKHYNIX/USDT:USDT** | 🔴 Short | `562 ` | 2026-10-22 22:15 | 9h 20m | **+10.27%** | **+21.79 USDT** | `exit_short_adaptive_trailing_scalp ( 562 )` |
| #11 | **BTW/USDT:USDT** | 🟢 Long | `1 ` | 2026-10-22 21:40 | 55m | **+30.41%** | **+48.73 USDT** | `exit_long_normal_d_6_1 ( 1 )` |
| #12 | **BTW/USDT:USDT** | 🟢 Long | `1 ` | 2026-10-22 20:30 | 5m | **+6.42%** | **+10.23 USDT** | `exit_long_normal_u_1 ( 1 )` |
| #13 | **BTW/USDT:USDT** | 🟢 Long | `44 ` | 2026-10-20 09:30 | 1h 0m | **+22.21%** | **+34.80 USDT** | `exit_long_quick_q_9 ( 44 )` |
| #14 | **COIN/USDT:USDT** | 🔴 Short | `562 ` | 2026-10-20 03:10 | 53h 45m | **+10.44%** | **+16.52 USDT** | `exit_short_adaptive_trailing_scalp ( 562 )` |
| #15 | **TAO/USDT:USDT** | 🔴 Short | `744_AI_PASS` | 2026-10-20 01:15 | 7h 45m | **+6.10%** | **+7.77 USDT** | `exit_ai_reversal_harvest ( 744_AI_PASS)` |

---
*Báo cáo được khởi tạo tự động bởi `scripts/export_report.py` phục vụ chu trình Tối ưu hóa Tự động Agentic AI.*
