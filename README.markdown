# Homie Chat

**Homie Chat** là một ứng dụng nhắn tin thời gian thực được xây dựng với:

- **Backend**:
  - **User Service**: PHP Laravel, quản lý người dùng và bạn bè, sử dụng PostgreSQL.
  - **Chat Service**: FastAPI, xử lý tin nhắn với WebSocket, sử dụng MongoDB.
  - **API Gateway**: FastAPI, định tuyến yêu cầu giữa các service.
- **Frontend**: React, cung cấp giao diện người dùng để nhắn tin và quản lý bạn bè.
- **Database**: PostgreSQL (người dùng, bạn bè) và MongoDB (hộp thoại, tin nhắn).

Ứng dụng được container hóa hoàn toàn bằng Docker, sử dụng một file `.env` duy nhất để cấu hình.

## Yêu cầu hệ thống
- **Docker**: Docker Desktop (Windows/Mac)
- **Docker Compose**: Phiên bản 2.0 hoặc cao hơn.

Kiểm tra cài đặt Docker:
```bash
docker --version
docker-compose --version
```

## Hướng dẫn cài đặt với Docker

Dưới đây là các bước chi tiết để cài đặt và chạy ứng dụng **Homie Chat** sử dụng Docker.

### Bước 1: Clone repository
1. Mở terminal và clone repository từ GitHub:
   ```bash
   git clone https://github.com/quocviet2001/homie-chat.git
   cd homie-chat
   ```

### Bước 2: Tạo file môi trường (.env)
1. Sao chép file `.env.example` để tạo file `.env`:
   ```bash
   cp .env.example .env
   ```

2. Mở file `homie-chat/.env` và điền các giá trị sau:
   ```text
   POSTGRES_USER=<your_database_username>
   POSTGRES_PASSWORD=<your_database_password>
   POSTGRES_DB=<your_database_name>
   MONGO_DB=<your_database_name>
   JWT_SECRET=<your_jwt_secret>
   APP_KEY=base64:<your_laravel_app_key>
   ```

   - **JWT_SECRET**: Tạo chuỗi ngẫu nhiên (32 byte) sử dụng GitBash:
     ```bash
     openssl rand -hex 32
     ```
     Ví dụ: `f4a1b2c3d4e5f67890abcdef1234567890abcdef1234567890abcdef12345678`.

   - **APP_KEY**: Tạo key cho Laravel:
     ```bash
     cd user-service
     docker run --rm -v ${PWD}:/app php:8.1-fpm php artisan key:generate --show
     ```
     Sao chép key (dạng `base64:...`) và dán vào `APP_KEY`.

3. Lưu file `.env`

### Bước 3: Build và chạy Docker
1. Build các container:
   ```bash
   cd homie-chat
   docker-compose build
   ```

2. Khởi động các container:
   ```bash
   docker-compose up -d
   ```

3. Kiểm tra các container đang chạy:
   ```bash
   docker ps
   ```
   - Bạn sẽ thấy 6 container: `homie-chat-user-service-1`, `homie-chat-chat-service-1`, `homie-chat-api-gateway-1`, `homie-chat-frontend-1`, `homie-chat-postgres-1`, `homie-chat-mongodb-1`.

### Bước 4: Chạy migration cho User Service
1. Chạy migration để tạo bảng trong PostgreSQL:
   ```bash
   docker exec -it homie-chat-user-service-1 php artisan migrate
   ```

### Bước 5: Kiểm tra ứng dụng
1. Mở trình duyệt và truy cập: `http://localhost:3000`

2. Tiến hành Đăng ký/Đăng nhập tài khoản và test các chức năng của ứng dụng.

### Bước 6: Dừng ứng dụng
Khi không sử dụng, dừng các container:
```bash
docker-compose down
```

Để xóa dữ liệu database (nếu cần reset):
```bash
docker-compose down -v
```
