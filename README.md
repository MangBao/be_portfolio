# Portfolio Backend API

Dự án Backend cho Portfolio cá nhân, được xây dựng bằng **Flask** và **PostgreSQL**, hỗ trợ deploy dễ dàng với **Docker**.

## 📝 Giới thiệu

Đây là RESTful API cung cấp dữ liệu cho ứng dụng Portfolio Frontend. Hệ thống quản lý các thông tin:

- Thông tin cá nhân (Profile)
- Dự án (Projects)
- Kỹ năng (Skills)
- Kinh nghiệm làm việc (Experiences)
- Authentication (JWT)

## 🛠 Yêu cầu hệ thống

- **Docker** & **Docker Compose** (bắt buộc để chạy database và app)
- **Python 3.x** (để chạy script setup tự động)

---

## 🚀 Hướng dẫn Cài đặt & Chạy (Auto Setup)

Dự án đi kèm với script `setup.py` giúp tự động hóa toàn bộ quy trình cấu hình và khởi chạy.

**Bước 1:** Mở terminal tại thư mục gốc dự án.

**Bước 2:** Chạy lệnh setup:

```bash
python setup.py
```

**Bước 3:** Tại menu chính, chọn **Option 1** (`🚀 Quick Start`).

- Script sẽ tự động kiểm tra Docker.
- Tạo file `.env` với các secret key an toàn.
- Build Docker images và khởi động containers.

Sau khi hoàn tất, API sẽ sẵn sàng tại `http://localhost:5000`.

---

## ⚙️ Hướng dẫn Cài đặt Thủ công (Manual Setup)

Nếu bạn muốn thiết lập từng bước mà không dùng script tự động:

1. **Tạo file cấu hình môi trường (.env)**:
   Copy file mẫu `.env.example` thành `.env`:

   ```bash
   # Windows
   copy .env.example .env
   # Linux/macOS
   cp .env.example .env
   ```

   _Lưu ý: Cập nhật `SECRET_KEY` và `JWT_SECRET_KEY` trong file `.env` nếu cần bảo mật cao hơn._

2. **Build Docker Images**:

   ```bash
   docker-compose build
   ```

3. **Khởi chạy Containers**:
   Chạy ứng dụng ở chế độ background:

   ```bash
   docker-compose up -d
   ```

4. **Kiểm tra trạng thái**:
   ```bash
   docker-compose ps
   ```

## 📡 Thông tin Truy cập

- **API Endpoint**: `http://localhost:5000`
- **Database Host**: `localhost:5432`
- **Tài khoản DB mặc định**:
  - User: `portfolio_user`
  - Pass: `portfolio_password`
  - DB: `portfolio_db`

## 📂 Cấu trúc Dự án

```
be_portfolio/
├── src/                 # Source code Flask App
├── docker-compose.yml   # Cấu hình Docker services
├── Dockerfile           # Cấu hình build image
├── setup.py             # Script tự động hóa
├── requirements.txt     # Các thư viện Python
└── database_schema...   # SQL khởi tạo database
```

## 🔧 Các lệnh thường dùng

- **Xem logs**: `docker-compose logs -f`
- **Dừng dự án**: `docker-compose down`
- **Dừng và xóa volume dữ liệu**: `docker-compose down -v`
