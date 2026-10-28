# 📈 Báo Cáo Đánh Giá Hiệu Suất Backtest Toàn Diện (Comprehensive Quantitative Report)

| Thông Tin Phiên Chạy | Chi Tiết | Đánh Dấu / Định Danh |
| :--- | :--- | :--- |
| 🏷️ **Phiên bản Chiến lược (Version)** | **`v7.2-16-ga5dc0a83c`** | `v7.2` |
| 🔖 **Git Commit** | `a5dc0a8` | `fix(report): synchronize latest_trades.csv with latest backtest run and align position breakdown` |
| 🚀 **Đánh dấu lần chạy (Run Marker)** | **`v7.2-a5dc0a8`** | `Workflow #local` |
| 🤖 **Chiến lược (Strategy)** | `NostalgiaForInfinityX8_Combined_AI` | `Combined AI Engine` |
| 📅 **Thời gian đánh giá (Evaluation Date)** | `2026-10-28 11:31:47 UTC` | `UTC` |
| ⏱️ **Cửa sổ Backtest (Timerange)** | `20260501-20261028` | `179 ngày` |
| 📁 **Tệp kết quả (Source File)** | `backtest-result-2026-10-28_18-31-24.zip` | `Binance Futures 5m` |

---

## ⚖️ So Sánh Hiệu Suất Với Lần Backtest Trước (Benchmark Comparison)

| Chỉ số định lượng | Lần chạy này [v7.2-a5dc0a8 - a5dc0a8] | Lần trước [v7.2-a5dc0a8 - a5dc0a8] | Chênh lệch (Δ Delta) | Xu hướng |
| :--- | :--- | :--- | :--- | :--- |
| **Tỷ lệ thắng (Winrate)** | **96.96%** | **84.77%** | `+12.18%` | 🟢 Cải thiện |
| **Lợi nhuận ròng (Net Profit %)** | **+1164.67%** | **+918.72%** | `+245.95%` | 🟢 Cải thiện |
| **Lợi nhuận tuyệt đối (USDT)** | **+2,329.34 USDT** | **+1,837.45 USDT** | `+491.90 USDT` | 🟢 Cải thiện |
| **Hệ số Sharpe (Sharpe Ratio)** | **15.01** | **14.52** | `+0.50` | 🟢 Cải thiện |
| **Hệ số Sortino (Sortino Ratio)** | **13.92** | **19.39** | `-5.47` | 🔴 Suy giảm |
| **Sụt giảm tối đa (Max Drawdown %)** | **2.38%** | **6.58%** | `-4.20%` | 🟢 Cải thiện |
| **Hệ số lãi/lỗ (Profit Factor)** | **17.68** | **2.97** | `+14.71` | 🟢 Cải thiện |
| **Tổng số lệnh (Total Trades)** | **230** | **440** | `-210.00 lệnh` | 🔴 Suy giảm |
| **Chuỗi lệnh thua dài nhất** | **1 trades** | **4 trades** | `-3.00 lệnh` | 🟢 Cải thiện |
| **Kỳ vọng toán học (Expectancy)** | **10.1276** | **4.1760** | `+5.95` | 🟢 Cải thiện |
| **Hệ số Calmar (Calmar Ratio)** | **5230.10** | **1490.31** | `+3,739.79` | 🟢 Cải thiện |

---

## 🏛️ Ma Trận Lịch Sử Đối Soát Giữa Các Lần Chạy (Multi-Run Version History Matrix)

> *Bảng tổng hợp đối chiếu kết quả backtest qua từng phiên bản và lần chạy để tiện theo dõi tiến trình tối ưu hóa.*

| Đánh dấu lần chạy (Run Marker) | Phiên bản | Commit | Ngày chạy | Tỷ lệ thắng (Winrate) | Lợi nhuận ròng | Max DD % | Sharpe | Profit Factor | Tổng lệnh | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `v7.0-baseline` | **`v7.0`** | `1911385` | 20261027 | **95.59%** | +988.89 USDT (+494.4%) | 2.03% | 11.24 | 26.38 | `136` | ⚪ Đã lưu |
| `v7.1-relief-rejection` | **`v7.1`** | `56b0067` | 20261027 | **97.06%** | +1,037.73 USDT (+518.9%) | 2.03% | 11.55 | 39.79 | `136` | ⚪ Đã lưu |
| `20261027` | **`v7.0`** | `-` | 20261027 | **97.08%** | +1,044.41 USDT (+522.2%) | 2.03% | 11.59 | 39.95 | `137` | ⚪ Đã lưu |
| `v7.2-new-short-tags` | **`v7.2`** | `12c4e69` | 20261027 | **97.08%** | +1,044.41 USDT (+522.2%) | 2.03% | 11.59 | 39.95 | `137` | ⚪ Đã lưu |
| `v7.2-upstream163-101pairs` | **`v7.2`** | `b2b4429` | 20261027 | **85.02%** | +1,762.39 USDT (+881.2%) | 6.56% | 14.39 | 2.98 | `434` | ⚪ Đã lưu |
| `v7.2-latest-180d-101pairs` | **`v7.2`** | `d003c7e` | 20261028 | **84.77%** | +1,847.60 USDT (+923.8%) | 6.57% | 14.53 | 2.97 | `440` | ⚪ Đã lưu |
| `v7.2-a5dc0a8` | **`v7.2`** | `a5dc0a8` | 20261028 | **84.77%** | +1,837.45 USDT (+918.7%) | 6.58% | 14.52 | 2.97 | `440` | ⚪ Đã lưu |
| `v7.2-a5dc0a8` | **`v7.2`** | `a5dc0a8` | 20261028 | **96.96%** | +2,329.34 USDT (+1164.7%) | 2.38% | 15.01 | 17.68 | `230` | 🎯 **HIỆN TẠI** |

---

## 🎯 Chỉ Số Hiệu Suất Cốt Lõi (Executive Performance Metrics)

| Chỉ số định lượng | Giá trị thực tế | Đánh giá Benchmark | Tiêu chuẩn chất lượng |
| :--- | :--- | :--- | :--- |
| **Tỷ lệ thắng (Winrate)** | **96.96%** | 🟢 Robust | Ngưỡng an toàn >= 70% |
| **Hệ số Sharpe (Sharpe Ratio)** | **15.01** | 🟢 Exceptional | Chuẩn Alpha quỹ >= 2.0 |
| **Hệ số Sortino (Sortino Ratio)** | **13.92** | 🟢 Excellent | Đo lường rủi ro sụt giảm âm |
| **Sụt giảm tài khoản tối đa (Max Drawdown %)** | **2.38%** | 🟢 Defended | Giới hạn rủi ro < 15% |
| **Sụt giảm tuyệt đối (Max Drawdown Abs)** | **+59.46 USDT** | 🟢 Đã kiểm soát | Độ sâu drawdown danh mục |
| **Hệ số lãi/lỗ (Profit Factor)** | **17.68** | 🟢 High | Chuẩn định lượng >= 1.5 |
| **Chuỗi thua dài nhất (Longest Loss Streak)** | **1 trades** | 🟢 Safe | Kiểm soát chuỗi sụt giảm |

---

## 📊 Chỉ Số Định Lượng Mở Rộng (Secondary Quantitative Indicators)

| Chỉ số định lượng | Kết quả | Mô tả & Ý nghĩa kỹ thuật |
| :--- | :--- | :--- |
| **Tổng số lệnh (Total Trades)** | `230` | Tổng số lệnh đã hoàn tất trong timerange |
| **Tổng lệnh thắng / hòa / thua** | `223` thắng / `0` hòa / `7` thua | Phân bổ kết quả các giao dịch |
| **Lợi nhuận ròng % (Net Profit %)** | `+1164.67%` | Tỷ lệ tăng trưởng toàn bộ tài khoản |
| **Lợi nhuận tuyệt đối (Net Profit Abs)** | `+2,329.34 USDT` | Lợi nhuận bằng tiền mặt (USDT) |
| **Lợi nhuận trung bình / lệnh** | `+10.13 USDT` | Hiệu quả trung bình mỗi lần vào lệnh |
| **Mật độ giao dịch (Trades Per Day)** | `1.28 lệnh / ngày` | Tần suất giao dịch bình quân |
| **Kỳ vọng toán học (Expectancy)** | `10.1276` | Lợi nhuận kỳ vọng trên mỗi 1 đơn vị rủi ro |
| **Hệ số Calmar (Calmar Ratio)** | `5230.10` | Tỷ lệ lợi nhuận trên sụt giảm vốn tối đa |
| **Tốc độ tăng trưởng kép (CAGR)** | `17562.39%` | Compound Annual Growth Rate quy năm |

---

## ⚔️ Thống Kê Phân Bổ Vị Thế (Long vs Short Performance)

| Vị thế (Position) | Số lệnh | Tỷ trọng | Tỷ lệ thắng (Winrate) | Lợi nhuận (USDT) | Lợi nhuận (%) | Đánh giá |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 🟢 **Lệnh Mua (Long)** | `168` | 73.0% | **98.81%** | **+2,102.47 USDT** | +2532.73% | 🟢 Vượt trội |
| 🔴 **Lệnh Bán (Short)** | `62` | 27.0% | **91.94%** | **+226.87 USDT** | +309.20% | 🟢 Vượt trội |
| 🌐 **Toàn bộ danh mục** | `230` | 100.0% | **96.96%** | **+2,329.34 USDT** | +1164.67% | 🎯 Hoàn tất |

## 🚪 Phân Tích Lý Do Thoát Lệnh (Exit Reason Breakdown)

| Lý do đóng lệnh (Exit Reason) | Số lệnh | Tỷ trọng | Tỷ lệ thắng (Winrate) | Lợi nhuận (USDT) |
| :--- | :--- | :--- | :--- | :--- |
| `TOTAL` | `230` | 100.0% | **97.0%** | +2,329.34 USDT |
| `exit_ai_reversal_harvest ( 702 703 731_AI_PASS)` | `18` | 7.8% | **100.0%** | +62.55 USDT |
| `exit_profit_long_rebuy_t_0_1_m ( 64 )` | `14` | 6.1% | **100.0%** | +49.66 USDT |
| `exit_short_adaptive_trailing_scalp ( 562 )` | `9` | 3.9% | **100.0%** | +100.89 USDT |
| `exit_profit_long_tc_t_0_1_m ( 142 )` | `7` | 3.0% | **100.0%** | +7.61 USDT |
| `exit_long_rebuy_d_6_1 ( 64 )` | `5` | 2.2% | **100.0%** | +216.65 USDT |
| `exit_ai_reversal_harvest ( 702 703 731 743_AI_PASS)` | `5` | 2.2% | **100.0%** | +15.00 USDT |
| `exit_long_rebuy_e_r ( 65 )` | `4` | 1.7% | **100.0%** | +36.39 USDT |
| `exit_profit_long_tc_t_0_1_m ( 143 )` | `4` | 1.7% | **100.0%** | +7.91 USDT |
| `exit_profit_long_tc_t_0_1_m ( 144 )` | `4` | 1.7% | **100.0%** | +6.70 USDT |
| `exit_long_quick_q_9 ( 44 )` | `3` | 1.3% | **100.0%** | +58.72 USDT |
| `exit_short_adaptive_trailing_scalp ( 542 )` | `3` | 1.3% | **100.0%** | +27.48 USDT |
| `exit_profit_long_tc_t_1_1_m ( 145 )` | `3` | 1.3% | **100.0%** | +16.94 USDT |
| `exit_long_normal_u_1 ( 2 )` | `3` | 1.3% | **100.0%** | +14.06 USDT |
| `exit_profit_long_tc_t_0_1_m ( 145 )` | `3` | 1.3% | **100.0%** | +9.21 USDT |
| `exit_profit_long_rebuy_t_0_1_m ( 62 )` | `3` | 1.3% | **100.0%** | +3.71 USDT |
| `exit_profit_short_rebuy_t_0_1_m ( 562 )` | `3` | 1.3% | **100.0%** | +3.32 USDT |
| `exit_long_rebuy_d_7_1 ( 64 )` | `2` | 0.9% | **100.0%** | +144.04 USDT |
| `exit_long_normal_d_4_1 ( 2 )` | `2` | 0.9% | **100.0%** | +91.63 USDT |
| `exit_long_normal_d_7_1 ( 2 )` | `2` | 0.9% | **100.0%** | +74.66 USDT |
| `exit_long_rebuy_d_4_1 ( 65 )` | `2` | 0.9% | **100.0%** | +52.06 USDT |
| `exit_short_rebuy_1_1_1 ( 562 )` | `2` | 0.9% | **100.0%** | +32.07 USDT |
| `exit_long_rebuy_d_4_1 ( 64 )` | `2` | 0.9% | **100.0%** | +31.85 USDT |
| `exit_long_normal_d_6_1 ( 2 )` | `2` | 0.9% | **100.0%** | +24.09 USDT |
| `exit_long_rapid_rpd_2 ( 102 )` | `2` | 0.9% | **100.0%** | +17.21 USDT |
| `exit_long_tc_u_1 ( 141 )` | `2` | 0.9% | **100.0%** | +17.08 USDT |
| `exit_long_tc_d_5_1 ( 141 142 )` | `2` | 0.9% | **100.0%** | +10.76 USDT |
| `exit_long_tc_d_5_1 ( 142 )` | `2` | 0.9% | **100.0%** | +10.12 USDT |
| `exit_profit_long_scalp_t_1_1_m ( 163 )` | `2` | 0.9% | **100.0%** | +8.38 USDT |
| `exit_short_rebuy_u_1 ( 562 )` | `2` | 0.9% | **100.0%** | +6.08 USDT |
| `exit_ai_reversal_harvest ( 703 721 731_AI_PASS)` | `2` | 0.9% | **100.0%** | +4.14 USDT |
| `exit_profit_long_tc_t_0_1_m ( 141 )` | `2` | 0.9% | **100.0%** | +4.14 USDT |
| `exit_ai_profit_lock ( 702 703 731_AI_PASS)` | `2` | 0.9% | **100.0%** | +3.66 USDT |
| `exit_profit_long_rebuy_t_0_1_m ( 61 )` | `2` | 0.9% | **100.0%** | +3.63 USDT |
| `exit_profit_long_scalp_t_0_1_m ( 163 )` | `2` | 0.9% | **100.0%** | +1.53 USDT |
| `exit_short_universal_structural_cut ( 562 )` | `2` | 0.9% | **0.0%** | -19.63 USDT |
| `exit_long_rebuy_d_6_1 ( 62 )` | `1` | 0.4% | **100.0%** | +77.02 USDT |
| `exit_long_quick_d_11_1 ( 43 )` | `1` | 0.4% | **100.0%** | +74.30 USDT |
| `exit_long_rebuy_2_1_1 ( 64 )` | `1` | 0.4% | **100.0%** | +71.46 USDT |
| `exit_long_tc_d_3_2 ( 141 )` | `1` | 0.4% | **100.0%** | +58.38 USDT |
| `exit_long_normal_d_6_1 ( 1 )` | `1` | 0.4% | **100.0%** | +51.44 USDT |
| `exit_long_quick_q_6 ( 42 )` | `1` | 0.4% | **100.0%** | +47.19 USDT |
| `exit_long_rapid_d_5_1 ( 103 )` | `1` | 0.4% | **100.0%** | +46.35 USDT |
| `exit_long_rebuy_w_6_1 ( 64 )` | `1` | 0.4% | **100.0%** | +38.04 USDT |
| `exit_long_normal_d_4_1 ( 6 )` | `1` | 0.4% | **100.0%** | +36.62 USDT |
| `exit_long_normal_d_7_1 ( 6 )` | `1` | 0.4% | **100.0%** | +35.65 USDT |
| `exit_long_rebuy_d_8_1 ( 64 )` | `1` | 0.4% | **100.0%** | +35.05 USDT |
| `exit_long_tc_d_8_1 ( 142 )` | `1` | 0.4% | **100.0%** | +33.91 USDT |
| `exit_long_tc_d_3_1 ( 141 )` | `1` | 0.4% | **100.0%** | +33.36 USDT |
| `exit_long_tc_d_5_1 ( 141 )` | `1` | 0.4% | **100.0%** | +32.05 USDT |
| `exit_long_normal_u_3 ( 6 141 )` | `1` | 0.4% | **100.0%** | +26.88 USDT |
| `exit_long_tc_3_1_1 ( 141 142 )` | `1` | 0.4% | **100.0%** | +26.14 USDT |
| `exit_long_scalp_d_5_1 ( 163 )` | `1` | 0.4% | **100.0%** | +24.60 USDT |
| `exit_short_adaptive_trailing_mega ( 562 )` | `1` | 0.4% | **100.0%** | +23.75 USDT |
| `exit_long_rebuy_d_9_1 ( 65 )` | `1` | 0.4% | **100.0%** | +18.67 USDT |
| `exit_long_tc_d_6_1 ( 144 )` | `1` | 0.4% | **100.0%** | +16.87 USDT |
| `exit_profit_long_rebuy_t_7_1_m ( 63 )` | `1` | 0.4% | **100.0%** | +16.03 USDT |
| `exit_profit_long_normal_t_2_1_m ( 3 )` | `1` | 0.4% | **100.0%** | +13.57 USDT |
| `exit_long_rebuy_d_8_1 ( 61 )` | `1` | 0.4% | **100.0%** | +13.29 USDT |
| `exit_ai_reversal_harvest ( 702 703 705 731_AI_PASS)` | `1` | 0.4% | **100.0%** | +13.23 USDT |
| `exit_long_scalp_d_6_1 ( 61 162 )` | `1` | 0.4% | **100.0%** | +12.90 USDT |
| `exit_long_quick_q_6 ( 47 )` | `1` | 0.4% | **100.0%** | +12.89 USDT |
| `exit_long_rebuy_d_6_1 ( 63 )` | `1` | 0.4% | **100.0%** | +12.57 USDT |
| `exit_long_tc_u_1 ( 141 142 )` | `1` | 0.4% | **100.0%** | +12.38 USDT |
| `exit_profit_long_tc_t_2_1_m ( 145 )` | `1` | 0.4% | **100.0%** | +12.23 USDT |
| `exit_long_tc_d_5_1 ( 145 )` | `1` | 0.4% | **100.0%** | +12.22 USDT |
| `exit_long_tc_u_1 ( 142 )` | `1` | 0.4% | **100.0%** | +11.99 USDT |
| `exit_long_rebuy_d_6_1 ( 61 )` | `1` | 0.4% | **100.0%** | +11.98 USDT |
| `exit_profit_short_rebuy_t_1_1_m ( 562 )` | `1` | 0.4% | **100.0%** | +11.92 USDT |
| `exit_profit_long_tc_t_2_1_m ( 142 )` | `1` | 0.4% | **100.0%** | +11.74 USDT |
| `exit_long_scalp_d_6_1 ( 162 )` | `1` | 0.4% | **100.0%** | +11.26 USDT |
| `exit_profit_long_quick_t_2_1_m ( 46 )` | `1` | 0.4% | **100.0%** | +11.03 USDT |
| `exit_long_quick_d_7_1 ( 42 )` | `1` | 0.4% | **100.0%** | +10.80 USDT |
| `exit_long_normal_u_1 ( 1 )` | `1` | 0.4% | **100.0%** | +10.80 USDT |
| `exit_long_normal_d_3_2 ( 5 )` | `1` | 0.4% | **100.0%** | +10.00 USDT |
| `exit_long_tc_d_6_1 ( 141 )` | `1` | 0.4% | **100.0%** | +9.18 USDT |
| `exit_long_normal_d_5_1 ( 1 )` | `1` | 0.4% | **100.0%** | +9.16 USDT |
| `exit_long_rebuy_d_5_1 ( 63 )` | `1` | 0.4% | **100.0%** | +9.05 USDT |
| `exit_profit_long_normal_t_1_1_m ( 3 )` | `1` | 0.4% | **100.0%** | +8.59 USDT |
| `exit_profit_long_tc_t_1_1_m ( 141 142 )` | `1` | 0.4% | **100.0%** | +8.23 USDT |
| `exit_long_tc_d_6_1 ( 141 143 163 )` | `1` | 0.4% | **100.0%** | +8.19 USDT |
| `exit_profit_long_tc_t_1_1_m ( 141 )` | `1` | 0.4% | **100.0%** | +8.08 USDT |
| `exit_long_tc_d_4_2 ( 145 )` | `1` | 0.4% | **100.0%** | +7.37 USDT |
| `exit_long_normal_d_8_1 ( 4 )` | `1` | 0.4% | **100.0%** | +7.32 USDT |
| `exit_long_tc_d_5_1 ( 62 144 )` | `1` | 0.4% | **100.0%** | +7.32 USDT |
| `exit_long_tc_d_6_1 ( 142 )` | `1` | 0.4% | **100.0%** | +7.07 USDT |
| `exit_long_normal_d_7_1 ( 2 101 141 )` | `1` | 0.4% | **100.0%** | +7.00 USDT |
| `exit_ai_profit_lock ( 703 721 724 731_AI_PASS)` | `1` | 0.4% | **100.0%** | +6.98 USDT |
| `exit_long_normal_d_5_1 ( 2 )` | `1` | 0.4% | **100.0%** | +6.61 USDT |
| `exit_long_normal_u_4 ( 1 61 )` | `1` | 0.4% | **100.0%** | +6.60 USDT |
| `exit_profit_long_rebuy_t_3_1_m ( 61 )` | `1` | 0.4% | **100.0%** | +6.53 USDT |
| `exit_long_normal_d_6_1 ( 3 142 )` | `1` | 0.4% | **100.0%** | +6.49 USDT |
| `exit_long_normal_d_3_2 ( 3 )` | `1` | 0.4% | **100.0%** | +6.17 USDT |
| `exit_profit_long_rebuy_t_2_1_m ( 65 )` | `1` | 0.4% | **100.0%** | +6.16 USDT |
| `exit_profit_long_normal_t_0_1_m ( 2 )` | `1` | 0.4% | **100.0%** | +6.00 USDT |
| `exit_long_normal_d_5_1 ( 6 102 141 )` | `1` | 0.4% | **100.0%** | +5.91 USDT |
| `exit_long_tc_d_3_2 ( 102 142 )` | `1` | 0.4% | **100.0%** | +5.55 USDT |
| `exit_long_tc_d_5_1 ( 144 )` | `1` | 0.4% | **100.0%** | +5.47 USDT |
| `exit_profit_long_rapid_t_1_1_m ( 102 )` | `1` | 0.4% | **100.0%** | +5.33 USDT |
| `exit_long_normal_d_5_1 ( 5 )` | `1` | 0.4% | **100.0%** | +5.33 USDT |
| `exit_profit_long_tc_t_0_1_m ( 141 142 )` | `1` | 0.4% | **100.0%** | +5.05 USDT |
| `exit_long_normal_d_6_1 ( 2 141 )` | `1` | 0.4% | **100.0%** | +4.97 USDT |
| `exit_long_quick_q_2 ( 42 )` | `1` | 0.4% | **100.0%** | +4.55 USDT |
| `exit_long_rapid_rpd_6 ( 102 )` | `1` | 0.4% | **100.0%** | +4.36 USDT |
| `exit_long_quick_q_2 ( 41 )` | `1` | 0.4% | **100.0%** | +4.03 USDT |
| `exit_profit_long_tc_t_3_1_m ( 143 )` | `1` | 0.4% | **100.0%** | +3.71 USDT |
| `exit_long_normal_u_2 ( 4 41 61 )` | `1` | 0.4% | **100.0%** | +3.70 USDT |
| `exit_long_normal_w_1_1 ( 1 )` | `1` | 0.4% | **100.0%** | +3.38 USDT |
| `exit_profit_long_rebuy_t_2_1_m ( 62 )` | `1` | 0.4% | **100.0%** | +3.33 USDT |
| `exit_profit_long_rebuy_t_1_1_m ( 62 )` | `1` | 0.4% | **100.0%** | +3.19 USDT |
| `exit_ai_reversal_harvest ( 721 724 741_AI_PASS)` | `1` | 0.4% | **100.0%** | +3.01 USDT |
| `exit_profit_long_normal_t_0_1_m ( 6 102 )` | `1` | 0.4% | **100.0%** | +2.95 USDT |
| `exit_ai_reversal_harvest ( 721 724 731_AI_PASS)` | `1` | 0.4% | **100.0%** | +2.61 USDT |
| `exit_long_normal_u_2 ( 2 )` | `1` | 0.4% | **100.0%** | +2.49 USDT |
| `exit_ai_reversal_harvest ( 702 731 743_AI_PASS)` | `1` | 0.4% | **100.0%** | +2.34 USDT |
| `exit_long_quick_u_1 ( 42 )` | `1` | 0.4% | **100.0%** | +2.22 USDT |
| `exit_ai_reversal_harvest ( 702 703 724 731_AI_PASS)` | `1` | 0.4% | **100.0%** | +2.20 USDT |
| `exit_profit_long_scalp_t_2_1_m ( 163 )` | `1` | 0.4% | **100.0%** | +1.97 USDT |
| `exit_profit_long_normal_t_0_1_m ( 6 )` | `1` | 0.4% | **100.0%** | +1.94 USDT |
| `exit_short_adaptive_trailing_scalp ( 702 703 731_AI_PASS)` | `1` | 0.4% | **100.0%** | +1.91 USDT |
| `exit_profit_long_rebuy_t_2_1_m ( 64 )` | `1` | 0.4% | **100.0%** | +1.89 USDT |
| `exit_profit_long_normal_t_2_1_m ( 2 63 101 )` | `1` | 0.4% | **100.0%** | +1.78 USDT |
| `exit_long_quick_u_1 ( 43 )` | `1` | 0.4% | **100.0%** | +1.68 USDT |
| `exit_profit_long_scalp_t_0_1_m ( 161 )` | `1` | 0.4% | **100.0%** | +1.67 USDT |
| `exit_long_tc_u_1 ( 144 )` | `1` | 0.4% | **100.0%** | +1.61 USDT |
| `exit_ai_reversal_harvest ( 731 743_AI_PASS)` | `1` | 0.4% | **100.0%** | +1.60 USDT |
| `exit_profit_long_quick_t_1_1_m ( 42 )` | `1` | 0.4% | **100.0%** | +1.29 USDT |
| `exit_profit_long_rapid_t_0_1_m ( 102 )` | `1` | 0.4% | **100.0%** | +1.03 USDT |
| `exit_profit_long_scalp_t_0_1_m ( 162 )` | `1` | 0.4% | **100.0%** | +0.94 USDT |
| `exit_profit_long_quick_t_0_1_m ( 43 )` | `1` | 0.4% | **100.0%** | +0.73 USDT |
| `exit_ai_profit_lock ( 703 705 706 731_AI_PASS)` | `1` | 0.4% | **100.0%** | +0.38 USDT |
| `exit_profit_long_normal_t_0_1_m ( 5 )` | `1` | 0.4% | **100.0%** | +0.31 USDT |
| `exit_ai_562_aged_breakeven ( 562 )` | `1` | 0.4% | **0.0%** | -3.76 USDT |
| `exit_bad_trade_abandon_18d ( 120 )` | `1` | 0.4% | **0.0%** | -11.24 USDT |
| `exit_short_universal_structural_cut ( 542 )` | `1` | 0.4% | **0.0%** | -15.42 USDT |
| `stop_loss` | `1` | 0.4% | **0.0%** | -30.17 USDT |
| `exit_ai_early_structural_cut ( 703 721 724 731_AI_PASS)` | `1` | 0.4% | **0.0%** | -59.46 USDT |

## 🔍 Bảng Phân Tích Đầy Đủ Tất Cả Các Entry Tags (Full Enter Tag Breakdown)

> *Bảng tổng hợp chi tiết 100% tất cả các tag tín hiệu vào lệnh (Entry Tags) đã hoạt động trong phiên backtest.*

| Enter Tag | Vị thế | Số lệnh | Tỷ lệ thắng (Winrate) | Thắng/Hòa/Thua | Tổng LN % | Tổng LN (USDT) | LN TB/Lệnh | Thời lượng TB | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `TOTAL` | 🟢 Long Core | `230` | **97.0%** | 223/0/7 | +1164.67% | **+2,329.34 USDT** | +12.36% | 12:40:00 | 🟢 Tối ưu |
| `64` | 🟢 Long Core | `27` | **100.0%** | 27/0/0 | +294.33% | **+588.66 USDT** | +18.36% | 10:41:00 | 🟢 Tối ưu |
| `2` | 🟢 Long Core | `12` | **100.0%** | 12/0/0 | +109.77% | **+219.53 USDT** | +20.29% | 2:08:00 | 🟢 Tối ưu |
| `141` | 🟢 Long Core | `9` | **100.0%** | 9/0/0 | +81.13% | **+162.26 USDT** | +13.21% | 9:31:00 | 🟢 Tối ưu |
| `562` | 🟢 Long Core | `21` | **85.7%** | 18/0/3 | +77.32% | **+154.63 USDT** | +5.75% | 1 day, 6:33:00 | 🟢 Tối ưu |
| `65` | 🟢 Long Core | `8` | **100.0%** | 8/0/0 | +56.63% | **+113.27 USDT** | +19.27% | 2:26:00 | 🟢 Tối ưu |
| `62` | 🟢 Long Core | `6` | **100.0%** | 6/0/0 | +43.62% | **+87.25 USDT** | +8.45% | 14:27:00 | 🟢 Tối ưu |
| `142` | 🟢 Long Core | `13` | **100.0%** | 13/0/0 | +41.22% | **+82.45 USDT** | +11.81% | 8:32:00 | 🟢 Tối ưu |
| `43` | 🟢 Long Core | `3` | **100.0%** | 3/0/0 | +38.35% | **+76.70 USDT** | +26.00% | 0:35:00 | 🟢 Tối ưu |
| `1` | 🟢 Long Core | `4` | **100.0%** | 4/0/0 | +37.39% | **+74.78 USDT** | +12.44% | 1 day, 20:39:00 | 🟢 Tối ưu |
| `6` | 🟢 Long Core | `3` | **100.0%** | 3/0/0 | +37.11% | **+74.22 USDT** | +18.75% | 17:13:00 | 🟢 Tối ưu |
| `702 703 731_AI_PASS` | 🤖 Short AI Gatekeeper | `21` | **100.0%** | 21/0/0 | +34.06% | **+68.12 USDT** | +5.76% | 4:17:00 | 🟢 Tối ưu |
| `42` | 🟢 Long Core | `5` | **100.0%** | 5/0/0 | +33.03% | **+66.05 USDT** | +15.47% | 2 days, 4:25:00 | 🟢 Tối ưu |
| `141 142` | 🟢 Long Core | `6` | **100.0%** | 6/0/0 | +31.28% | **+62.57 USDT** | +13.96% | 9:57:00 | 🟢 Tối ưu |
| `44` | 🟢 Long Core | `3` | **100.0%** | 3/0/0 | +29.36% | **+58.72 USDT** | +22.49% | 2:32:00 | 🟢 Tối ưu |
| `145` | 🟢 Long Core | `9` | **100.0%** | 9/0/0 | +28.98% | **+57.97 USDT** | +10.60% | 8:46:00 | 🟢 Tối ưu |
| `103` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +23.17% | **+46.35 USDT** | +25.41% | 2:30:00 | 🟢 Tối ưu |
| `63` | 🟢 Long Core | `3` | **100.0%** | 3/0/0 | +18.82% | **+37.65 USDT** | +33.10% | 3:02:00 | 🟢 Tối ưu |
| `163` | 🟢 Long Core | `6` | **100.0%** | 6/0/0 | +18.24% | **+36.48 USDT** | +9.34% | 2:25:00 | 🟢 Tối ưu |
| `61` | 🟢 Long Core | `5` | **100.0%** | 5/0/0 | +17.71% | **+35.43 USDT** | +20.53% | 2:10:00 | 🟢 Tối ưu |
| `144` | 🟢 Long Core | `7` | **100.0%** | 7/0/0 | +15.33% | **+30.66 USDT** | +11.47% | 12:38:00 | 🟢 Tối ưu |
| `102` | 🟢 Long Core | `5` | **100.0%** | 5/0/0 | +13.97% | **+27.94 USDT** | +5.32% | 2:58:00 | 🟢 Tối ưu |
| `6 141` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +13.44% | **+26.88 USDT** | +16.21% | 19:20:00 | 🟢 Tối ưu |
| `5` | 🟢 Long Core | `3` | **100.0%** | 3/0/0 | +7.82% | **+15.64 USDT** | +14.52% | 3:03:00 | 🟢 Tối ưu |
| `702 703 731 743_AI_PASS` | 🤖 Short AI Gatekeeper | `5` | **100.0%** | 5/0/0 | +7.50% | **+15.00 USDT** | +5.92% | 2:27:00 | 🟢 Tối ưu |
| `702 703 705 731_AI_PASS` | 🤖 Short AI Gatekeeper | `1` | **100.0%** | 1/0/0 | +6.62% | **+13.23 USDT** | +6.15% | 7:45:00 | 🟢 Tối ưu |
| `61 162` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +6.45% | **+12.90 USDT** | +32.22% | 4:05:00 | 🟢 Tối ưu |
| `47` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +6.45% | **+12.89 USDT** | +13.38% | 1 day, 2:00:00 | 🟢 Tối ưu |
| `162` | 🟢 Long Core | `2` | **100.0%** | 2/0/0 | +6.10% | **+12.20 USDT** | +17.33% | 0:52:00 | 🟢 Tối ưu |
| `542` | 🟢 Long Core | `4` | **75.0%** | 3/0/1 | +6.03% | **+12.06 USDT** | +1.59% | 1:24:00 | 🟡 Hiệu quả |
| `143` | 🟢 Long Core | `5` | **100.0%** | 5/0/0 | +5.81% | **+11.63 USDT** | +5.30% | 18:36:00 | 🟢 Tối ưu |
| `46` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +5.51% | **+11.03 USDT** | +11.97% | 0:45:00 | 🟢 Tối ưu |
| `141 143 163` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +4.10% | **+8.19 USDT** | +33.41% | 1:30:00 | 🟢 Tối ưu |
| `4` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +3.66% | **+7.32 USDT** | +44.22% | 1:10:00 | 🟢 Tối ưu |
| `62 144` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +3.66% | **+7.32 USDT** | +25.85% | 1:25:00 | 🟢 Tối ưu |
| `2 101 141` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +3.50% | **+7.00 USDT** | +36.21% | 1:00:00 | 🟢 Tối ưu |
| `1 61` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +3.30% | **+6.60 USDT** | +21.38% | 0:15:00 | 🟢 Tối ưu |
| `3 142` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +3.24% | **+6.49 USDT** | +21.61% | 1 day, 19:40:00 | 🟢 Tối ưu |
| `6 102 141` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +2.96% | **+5.91 USDT** | +26.17% | 1:00:00 | 🟢 Tối ưu |
| `102 142` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +2.78% | **+5.55 USDT** | +19.97% | 1:40:00 | 🟢 Tối ưu |
| `2 141` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +2.48% | **+4.97 USDT** | +30.19% | 2:15:00 | 🟢 Tối ưu |
| `703 721 731_AI_PASS` | 🤖 Short AI Gatekeeper | `2` | **100.0%** | 2/0/0 | +2.07% | **+4.14 USDT** | +5.50% | 14:42:00 | 🟢 Tối ưu |
| `41` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +2.02% | **+4.03 USDT** | +11.69% | 5:00:00 | 🟢 Tối ưu |
| `4 41 61` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +1.85% | **+3.70 USDT** | +11.78% | 0:10:00 | 🟢 Tối ưu |
| `721 724 741_AI_PASS` | 🤖 Short AI Gatekeeper | `1` | **100.0%** | 1/0/0 | +1.51% | **+3.01 USDT** | +5.01% | 7:05:00 | 🟢 Tối ưu |
| `6 102` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +1.47% | **+2.95 USDT** | +1.43% | 2:05:00 | 🟢 Tối ưu |
| `721 724 731_AI_PASS` | 🤖 Short AI Gatekeeper | `1` | **100.0%** | 1/0/0 | +1.30% | **+2.61 USDT** | +6.65% | 17:10:00 | 🟢 Tối ưu |
| `702 731 743_AI_PASS` | 🤖 Short AI Gatekeeper | `1` | **100.0%** | 1/0/0 | +1.17% | **+2.34 USDT** | +6.75% | 9:05:00 | 🟢 Tối ưu |
| `702 703 724 731_AI_PASS` | 🤖 Short AI Gatekeeper | `1` | **100.0%** | 1/0/0 | +1.10% | **+2.20 USDT** | +6.01% | 0:25:00 | 🟢 Tối ưu |
| `2 63 101` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +0.89% | **+1.78 USDT** | +10.72% | 2:55:00 | 🟢 Tối ưu |
| `161` | 🟢 Long Core | `1` | **100.0%** | 1/0/0 | +0.84% | **+1.67 USDT** | +3.34% | 12:05:00 | 🟢 Tối ưu |
| `731 743_AI_PASS` | 🤖 Short AI Gatekeeper | `1` | **100.0%** | 1/0/0 | +0.80% | **+1.60 USDT** | +5.56% | 2:40:00 | 🟢 Tối ưu |
| `703 705 706 731_AI_PASS` | 🤖 Short AI Gatekeeper | `1` | **100.0%** | 1/0/0 | +0.19% | **+0.38 USDT** | +1.92% | 6:05:00 | 🟢 Tối ưu |
| `3` | 🟢 Long Core | `4` | **75.0%** | 3/0/1 | -0.92% | **-1.84 USDT** | -12.21% | 4:46:00 | 🔴 Cần tinh chỉnh |
| `120` | 🟢 Long Core | `1` | **0.0%** | 0/0/1 | -5.62% | **-11.24 USDT** | -9.79% | 17 days, 22:40:00 | 🔴 Cần tinh chỉnh |
| `703 721 724 731_AI_PASS` | 🤖 Short AI Gatekeeper | `2` | **50.0%** | 1/0/1 | -26.24% | **-52.47 USDT** | -8.68% | 3:45:00 | 🔴 Cần tinh chỉnh |

---

## 📑 Chi Tiết Các Lệnh Giao Dịch (Trade Execution Journal)

### 🥇 Top 10 Lệnh Lãi Cao Nhất (Top Winning Trades)
| # | Cặp giao dịch | Vị thế | Enter Tag | Thời gian Mở ➔ Đóng | Thời lượng | Lợi nhuận % | Lợi nhuận USDT | Lý do thoát |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| #1 | **BAT/USDT:USDT** | 🟢 Long | `64 ` | 2026-10-08 08:20 ➔ 2026-10-09 06:05 | 21h 45m | **+43.38%** | **+85.86 USDT** | `exit_long_rebuy_d_7_1 ( 64 )` |
| #2 | **GRASS/USDT:USDT** | 🟢 Long | `62 ` | 2026-10-14 17:45 ➔ 2026-10-15 15:05 | 21h 20m | **+33.86%** | **+77.02 USDT** | `exit_long_rebuy_d_6_1 ( 62 )` |
| #3 | **BTW/USDT:USDT** | 🟢 Long | `43 ` | 2026-10-05 06:45 ➔ 2026-10-05 08:05 | 1h 20m | **+71.12%** | **+74.30 USDT** | `exit_long_quick_d_11_1 ( 43 )` |
| #4 | **ARB/USDT:USDT** | 🟢 Long | `64 ` | 2026-09-17 21:45 ➔ 2026-09-18 01:50 | 4h 5m | **+59.20%** | **+71.46 USDT** | `exit_long_rebuy_2_1_1 ( 64 )` |
| #5 | **BTW/USDT:USDT** | 🟢 Long | `2 ` | 2026-10-23 18:30 ➔ 2026-10-23 19:10 | 40m | **+38.38%** | **+67.66 USDT** | `exit_long_normal_d_7_1 ( 2 )` |
| #6 | **GRASS/USDT:USDT** | 🟢 Long | `64 ` | 2026-10-05 14:55 ➔ 2026-10-05 19:15 | 4h 20m | **+32.17%** | **+58.99 USDT** | `exit_long_rebuy_d_6_1 ( 64 )` |
| #7 | **WLD/USDT:USDT** | 🟢 Long | `141 ` | 2026-10-25 08:55 ➔ 2026-10-25 15:40 | 6h 45m | **+19.30%** | **+58.38 USDT** | `exit_long_tc_d_3_2 ( 141 )` |
| #8 | **WLD/USDT:USDT** | 🟢 Long | `64 ` | 2026-09-26 22:25 ➔ 2026-09-27 10:10 | 11h 45m | **+40.20%** | **+58.18 USDT** | `exit_long_rebuy_d_7_1 ( 64 )` |
| #9 | **BAT/USDT:USDT** | 🟢 Long | `64 ` | 2026-10-03 06:15 ➔ 2026-10-04 07:40 | 25h 25m | **+33.11%** | **+55.06 USDT** | `exit_long_rebuy_d_6_1 ( 64 )` |
| #10 | **BTW/USDT:USDT** | 🟢 Long | `1 ` | 2026-10-22 20:45 ➔ 2026-10-22 21:40 | 55m | **+30.41%** | **+51.44 USDT** | `exit_long_normal_d_6_1 ( 1 )` |

### ⚠️ Top Lệnh Thua Lỗ / Sụt Giảm Lớn Nhất (Top Drawdown Trades)
| # | Cặp giao dịch | Vị thế | Enter Tag | Thời gian Mở ➔ Đóng | Thời lượng | Thua lỗ % | Thua lỗ USDT | Lý do thoát |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| #1 | **NXPC/USDT:USDT** | 🔴 Short | `703 721 724 731_AI_PASS` | 2026-10-26 07:05 ➔ 2026-10-26 14:20 | 7h 15m | **-19.66%** | **-59.46 USDT** | `exit_ai_early_structural_cut ( 703 721 724 731_AI_PASS)` |
| #2 | **SOXL/USDT:USDT** | 🟢 Long | `3 ` | 2026-06-05 15:40 ➔ 2026-06-06 02:50 | 11h 10m | **-78.58%** | **-30.17 USDT** | `stop_loss` |
| #3 | **MVLL/USDT:USDT** | 🔴 Short | `542 ` | 2026-08-20 17:15 ➔ 2026-08-20 20:05 | 2h 50m | **-23.02%** | **-15.42 USDT** | `exit_short_universal_structural_cut ( 542 )` |
| #4 | **ZEC/USDT:USDT** | 🔴 Short | `562 ` | 2026-07-29 03:35 ➔ 2026-07-30 05:50 | 26h 15m | **-22.91%** | **-11.30 USDT** | `exit_short_universal_structural_cut ( 562 )` |
| #5 | **RENDER/USDT:USDT** | 🟢 Long | `120 ` | 2026-06-04 01:20 ➔ 2026-06-22 00:00 | 430h 40m | **-9.79%** | **-11.24 USDT** | `exit_bad_trade_abandon_18d ( 120 )` |
| #6 | **CRCL/USDT:USDT** | 🔴 Short | `562 ` | 2026-06-17 11:10 ➔ 2026-06-17 15:50 | 4h 40m | **-23.74%** | **-8.33 USDT** | `exit_short_universal_structural_cut ( 562 )` |
| #7 | **QNT/USDT:USDT** | 🔴 Short | `562 ` | 2026-08-03 08:30 ➔ 2026-08-04 20:30 | 36h 0m | **-6.71%** | **-3.76 USDT** | `exit_ai_562_aged_breakeven ( 562 )` |

### ⏱️ Nhật Ký 15 Lệnh Giao Dịch Gần Nhất (Recent Trades Log)
| # | Cặp giao dịch | Vị thế | Enter Tag | Thời gian Đóng | Thời lượng | Lợi nhuận % | Lợi nhuận USDT | Lý do thoát |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| #1 | **ARB/USDT:USDT** | 🔴 Short | `703 721 724 731_AI_PASS` | 2026-10-27 09:40 | 15m | **+2.29%** | **+6.98 USDT** | `exit_ai_profit_lock ( 703 721 724 731_AI_PASS)` |
| #2 | **FET/USDT:USDT** | 🔴 Short | `702 703 731_AI_PASS` | 2026-10-27 03:10 | 7h 5m | **+6.13%** | **+18.23 USDT** | `exit_ai_reversal_harvest ( 702 703 731_AI_PASS)` |
| #3 | **BTW/USDT:USDT** | 🟢 Long | `103 ` | 2026-10-26 21:45 | 2h 30m | **+25.41%** | **+46.35 USDT** | `exit_long_rapid_d_5_1 ( 103 )` |
| #4 | **CHIP/USDT:USDT** | 🔴 Short | `542 ` | 2026-10-26 18:40 | 1h 0m | **+8.67%** | **+15.71 USDT** | `exit_short_adaptive_trailing_scalp ( 542 )` |
| #5 | **NXPC/USDT:USDT** | 🔴 Short | `703 721 724 731_AI_PASS` | 2026-10-26 14:20 | 7h 15m | **-19.66%** | **-59.46 USDT** | `exit_ai_early_structural_cut ( 703 721 724 731_AI_PASS)` |
| #6 | **WLD/USDT:USDT** | 🟢 Long | `141 ` | 2026-10-25 15:40 | 6h 45m | **+19.30%** | **+58.38 USDT** | `exit_long_tc_d_3_2 ( 141 )` |
| #7 | **BTW/USDT:USDT** | 🟢 Long | `2 ` | 2026-10-23 19:10 | 40m | **+38.38%** | **+67.66 USDT** | `exit_long_normal_d_7_1 ( 2 )` |
| #8 | **SAMSUNG/USDT:USDT** | 🔴 Short | `562 ` | 2026-10-23 00:15 | 11h 20m | **+10.74%** | **+24.05 USDT** | `exit_short_adaptive_trailing_scalp ( 562 )` |
| #9 | **SKHYNIX/USDT:USDT** | 🔴 Short | `562 ` | 2026-10-22 22:15 | 9h 20m | **+10.27%** | **+22.93 USDT** | `exit_short_adaptive_trailing_scalp ( 562 )` |
| #10 | **BTW/USDT:USDT** | 🟢 Long | `1 ` | 2026-10-22 21:40 | 55m | **+30.41%** | **+51.44 USDT** | `exit_long_normal_d_6_1 ( 1 )` |
| #11 | **BTW/USDT:USDT** | 🟢 Long | `1 ` | 2026-10-22 20:30 | 5m | **+6.42%** | **+10.80 USDT** | `exit_long_normal_u_1 ( 1 )` |
| #12 | **BTW/USDT:USDT** | 🟢 Long | `44 ` | 2026-10-20 09:30 | 1h 0m | **+22.21%** | **+36.78 USDT** | `exit_long_quick_q_9 ( 44 )` |
| #13 | **COIN/USDT:USDT** | 🔴 Short | `562 ` | 2026-10-20 03:10 | 53h 45m | **+10.44%** | **+17.42 USDT** | `exit_short_adaptive_trailing_scalp ( 562 )` |
| #14 | **QNT/USDT:USDT** | 🔴 Short | `702 703 731_AI_PASS` | 2026-10-20 01:10 | 1h 0m | **+6.39%** | **+10.90 USDT** | `exit_ai_reversal_harvest ( 702 703 731_AI_PASS)` |
| #15 | **SAND/USDT:USDT** | 🔴 Short | `702 703 705 731_AI_PASS` | 2026-10-20 00:55 | 7h 45m | **+6.15%** | **+13.23 USDT** | `exit_ai_reversal_harvest ( 702 703 705 731_AI_PASS)` |

---
*Báo cáo được khởi tạo tự động bởi `scripts/export_report.py` phục vụ chu trình Tối ưu hóa Tự động Agentic AI.*
