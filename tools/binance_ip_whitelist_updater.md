# Binance API Key IP Whitelist Auto-Updater

Tool: [`tools/binance_ip_whitelist_updater.py`](./binance_ip_whitelist_updater.py)  
Chạy trực tiếp trên máy/VPS của bot live, không cần cài thêm thư viện ngoài (thuần Python 3 standard library).

## Cơ chế hoạt động (2 chế độ)

1. **Chế độ Sub-Account (`subaccount` — tự động cập nhật lên Binance):**
   - Kích hoạt tự động khi cấu hình đủ bộ biến `BINANCE_MASTER_API_KEY`, `BINANCE_MASTER_API_SECRET`, `BINANCE_SUBACCOUNT_EMAIL`, và `BINANCE_SUBACCOUNT_API_KEY` (nếu bỏ trống sẽ tự lấy `FREQTRADE__EXCHANGE__KEY` từ `.env`).
   - Khi public IP thay đổi:
     1. Đọc danh sách IP hiện tại qua `GET /sapi/v1/sub-account/subAccountApi/ipRestriction`.
     2. **Thêm IP mới trước** (`POST /sapi/v2/sub-account/subAccountApi/ipRestriction`, `status=2`) để đảm bảo bot không bị gián đoạn.
     3. Sau khi xác nhận IP mới đã nằm trong `ipList`, tự động xoá IP cũ (`DELETE /sapi/v1/sub-account/subAccountApi/ipRestriction/ipList`), **luôn giữ lại** IP hiện tại và các IP cố định trong `BINANCE_KEEP_IPS`.
     4. Gửi thông báo kết quả (hoặc lỗi nếu có) về Telegram.

2. **Chế độ Master Account (`alert` — theo dõi & cảnh báo Telegram ngay lập tức):**
   - Binance không mở API cho phép sửa IP whitelist của chính Master Account API Key (bắt buộc 2FA/Passkey trên Web/App).
   - Khi chưa cấu hình Sub-Account (hoặc chạy `--mode alert`), tool sẽ:
     1. Phát hiện public IP thay đổi.
     2. Kiểm tra nhanh trạng thái API key hiện tại qua `GET /sapi/v1/account/apiRestrictions` (phát hiện lỗi `-2015` bị chặn IP).
     3. Gửi thông báo Telegram kèm **IP cũ → IP mới** và link trực tiếp tới Binance API Management để bạn dán IP mới trong vài giây.

---

## Cấu hình `.env`

Tool tự đọc file `.env` ở thư mục hiện tại (hoặc chỉ định bằng `--env-file`) và kế thừa sẵn `FREQTRADE__BOT_NAME`, `FREQTRADE__EXCHANGE__KEY`, `FREQTRADE__EXCHANGE__SECRET`, `FREQTRADE__TELEGRAM__TOKEN`, `FREQTRADE__TELEGRAM__CHAT_ID`.

### Nếu dùng Sub-Account (tự động update lên Binance)

Thêm các biến sau vào `.env`:

```env
# Master Account API Key (cần quyền quản lý Sub-Account trên Binance)
BINANCE_MASTER_API_KEY=your_master_api_key
BINANCE_MASTER_API_SECRET=your_master_api_secret

# Thông tin Sub-Account mà bot live đang chạy
BINANCE_SUBACCOUNT_EMAIL=your_subaccount@example.com
# Tùy chọn: mặc định sẽ tự lấy FREQTRADE__EXCHANGE__KEY nếu bỏ trống
BINANCE_SUBACCOUNT_API_KEY=your_subaccount_api_key

# Tùy chọn: danh sách IP tĩnh luôn giữ lại trong whitelist (phân tách bằng dấu phẩy)
BINANCE_KEEP_IPS=

# Tùy chọn: tự động xoá IP động cũ sau khi thêm IP mới (mặc định: true)
BINANCE_REMOVE_OLD_IP=true
```

> **Lưu ý quan trọng:** Nếu chính `BINANCE_MASTER_API_KEY` cũng đang bị giới hạn IP whitelist và máy gọi bị đổi IP, Binance sẽ từ chối request với lỗi `-2015`. Trong trường hợp đó tool sẽ tự gửi cảnh báo Telegram kèm lỗi và link cập nhật tay.

### Nếu dùng Master Account thường (chế độ cảnh báo Telegram)

Không cần thêm biến mới nếu `.env` của Freqtrade đã có sẵn `FREQTRADE__TELEGRAM__TOKEN` và `FREQTRADE__TELEGRAM__CHAT_ID`.

---

## Cách chạy

### 1. Kiểm tra trạng thái hiện tại
```bash
python3 tools/binance_ip_whitelist_updater.py --status
```

### 2. Chạy thử không ghi thay đổi (`--dry-run --force`)
```bash
python3 tools/binance_ip_whitelist_updater.py --dry-run --force --verbose
```

### 3. Chạy 1 lần (phù hợp với `cron`)
```bash
python3 tools/binance_ip_whitelist_updater.py
```

### 4. Chế độ định kỳ kiểm tra IP (4 cách triển khai)

#### Cách A: Chạy nền liên tục bằng `--watch` (có tự đối soát Binance & retry backoff)
```bash
python3 tools/binance_ip_whitelist_updater.py \
  --watch \
  --interval 300 \
  --reconcile-every 3600 \
  --log-file user_data/logs/binance_ip_updater.log
```
- `--interval 300`: kiểm tra public IP mỗi 300 giây (5 phút), cũng có thể cấu hình qua `BINANCE_IP_CHECK_INTERVAL` trong `.env`.
- `--reconcile-every 3600`: mỗi 1 giờ tự đối soát lại với Binance ngay cả khi IP không đổi (tự thêm lại nếu IP bị xoá nhầm trên Binance ở chế độ Sub-Account, hoặc cảnh báo Telegram nếu gặp `-2015` ở chế độ Master Account). Đặt `0` để tắt.
- `--retry-delay 30`: khi lỗi mạng tạm thời sẽ retry sớm theo exponential backoff (30s → 60s → 120s...) và gửi cảnh báo Telegram nếu lỗi liên tiếp >= `BINANCE_IP_MAX_CONSECUTIVE_ERRORS` (mặc định `3`), kèm thông báo khi phục hồi.
- `--log-file`: tự xoay vòng log tối đa 5 MB × 3 file backup.

#### Cách B: Cài Cron tự động bằng 1 lệnh (`--install-cron`)
```bash
# Cài cron kiểm tra mỗi 5 phút (300 giây)
python3 tools/binance_ip_whitelist_updater.py --install-cron --interval 300

# Gỡ cron khi không dùng nữa
python3 tools/binance_ip_whitelist_updater.py --uninstall-cron
```

#### Cách C: Tạo `systemd` service trên VPS Linux (`--print-systemd`)
```bash
python3 tools/binance_ip_whitelist_updater.py --print-systemd --interval 300 \
  | sudo tee /etc/systemd/system/binance-ip-updater.service
sudo systemctl daemon-reload
sudo systemctl enable --now binance-ip-updater.service
sudo systemctl status binance-ip-updater.service
```

#### Cách D: Chạy sidecar container cùng Docker Compose
Sử dụng file overlay [`docker/docker-compose.ip-updater.yml`](../docker/docker-compose.ip-updater.yml):
```bash
docker compose -f docker-compose.yml -f docker/docker-compose.ip-updater.yml up -d binance-ip-updater
```

### Biến môi trường bổ sung cho chế độ định kỳ (`.env`)
```env
BINANCE_IP_CHECK_INTERVAL=300
BINANCE_IP_RECONCILE_EVERY=3600
BINANCE_IP_RETRY_DELAY=30
BINANCE_IP_MAX_CONSECUTIVE_ERRORS=3
BINANCE_IP_LOG_FILE=user_data/logs/binance_ip_updater.log
```
