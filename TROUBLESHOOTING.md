# ⚠️ API Deployment Issues - Root Causes and Solutions

## 🐛 Vấn đề bạn gặp phải

**Triệu chứng:** API hoạt động tốt ở local nhưng bị lỗi "Failed to fetch" sau khi deploy lên Render

## 🔍 Các nguyên nhân chính (đã được sửa)

### 1. ❌ CORS Configuration Issues (Đã sửa ✅)

**Vấn đề:**

- Code ban đầu chỉ có `CORS(app)` - cấu hình mặc định không đủ cho production
- Render và frontend ở domain khác nhau cần CORS được config rõ ràng

**Giải pháp đã áp dụng:**

```python
CORS(app, resources={
    r"/api/*": {
        "origins": "*",  # Allow all origins
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "expose_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True,
        "max_age": 3600
    }
})
```

📍 File: `src/__init__.py` (line 24-35)

---

### 2. ❌ Production Server Issues (Đã sửa ✅)

**Vấn đề:**

- `app.run()` chỉ phù hợp cho development
- Render yêu cầu production WSGI server như Gunicorn
- Port phải được bind từ environment variable `PORT`

**Giải pháp đã áp dụng:**

- ✅ Tạo file `wsgi.py` để Gunicorn sử dụng
- ✅ Config start command: `gunicorn wsgi:app`
- ✅ wsgi.py tự động lấy PORT từ environment

📍 Files tạo mới:

- `wsgi.py` - Production entry point
- `render.yaml` - Render deployment config

---

### 3. ❌ Missing Environment Variables (Cần check)

**Vấn đề:**
Code của bạn yêu cầu 3 biến bắt buộc:

```python
SECRET_KEY = os.environ.get("SECRET_KEY")
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
FLASK_DB_URI = os.environ.get("FLASK_DB_URI")
```

Nếu thiếu, app sẽ raise ValueError ngay khi khởi động.

**Giải pháp:**
Bạn cần set đầy đủ các biến này trên Render Dashboard:

```env
SECRET_KEY=lxi0MIK_rJhKtyTMqLt95CXfHHWf7cFep7vKUR5LWSA
JWT_SECRET_KEY=z47ZYdcZoJ1ppSd8LqiIpuRDqwXPl_sIbumb5DIK3G8
FLASK_DB_URI=postgresql://your_db_connection_string
FLASK_ENV=production
```

📍 Hướng dẫn chi tiết: `RENDER_DEPLOYMENT.md` (Section "Step 3")

---

### 4. ❌ Database Connection Issues (Cần check)

**Vấn đề:**

- Local bạn dùng Docker PostgreSQL: `db:5432`
- Render production phải dùng external database (Supabase hoặc Render PostgreSQL)
- Connection string sai hoặc database không accessible

**Giải pháp:**

1. **Nếu dùng Supabase:**

   ```
   FLASK_DB_URI=postgresql://postgres:[PASSWORD]@[SUPABASE_HOST]:5432/postgres
   ```

2. **Nếu dùng Render PostgreSQL:**
   - Tạo PostgreSQL database trên Render
   - Copy "Internal Database URL"
   - Set vào environment variable `FLASK_DB_URI`

**Test kết nối:**
Endpoint `/health` đã được thêm vào để test database:

```bash
curl https://your-app.onrender.com/health
```

Nếu database OK, sẽ trả về:

```json
{
  "status": "healthy",
  "database": "connected",
  "message": "Portfolio API is running"
}
```

📍 Code: `src/__init__.py` (function `health_check()`)

---

### 5. ❌ Missing Health Check (Đã sửa ✅)

**Vấn đề:**
Render cần health check endpoint để verify service đang chạy

**Giải pháp đã áp dụng:**

- ✅ Tạo endpoint `/health`
- ✅ Config `healthCheckPath: /health` trong `render.yaml`

---

## 📋 Checklist để deploy thành công

### Bước 1: Code đã được sửa ✅

- [x] `wsgi.py` - Production entry point
- [x] `render.yaml` - Deployment config
- [x] CORS configuration đã được update
- [x] Health check endpoint đã được thêm
- [x] Gunicorn đã có trong requirements.txt

### Bước 2: Cần làm trên Render Dashboard

- [ ] Push code lên GitHub
- [ ] Tạo Web Service trên Render
- [ ] Set environment variables:
  - [ ] SECRET_KEY
  - [ ] JWT_SECRET_KEY
  - [ ] FLASK_DB_URI (database connection)
  - [ ] FLASK_ENV=production
- [ ] Deploy và chờ build hoàn thành

### Bước 3: Verify deployment

- [ ] Check logs trên Render
- [ ] Test health endpoint: `https://your-app.onrender.com/health`
- [ ] Test API endpoint: `https://your-app.onrender.com/api/v1/about`
- [ ] Check CORS: Gọi API từ frontend

---

## 🧪 Test trước khi deploy

Để đảm bảo code chạy tốt trước khi deploy lên Render, test với Gunicorn local:

**Windows:**

```bash
.\test_gunicorn.bat
```

**Linux/Mac:**

```bash
./test_gunicorn.sh
```

Server sẽ chạy tại `http://localhost:8000`

---

## 🔧 Debug khi vẫn gặp lỗi

### Lỗi: "Application failed to respond"

✅ **Kiểm tra:**

1. Logs trên Render Dashboard
2. Environment variables đã set đầy đủ chưa?
3. Database connection string đúng chưa?

```bash
# Test database connection trên Render Shell
python -c "from sqlalchemy import create_engine; engine = create_engine('YOUR_DB_URI'); engine.connect()"
```

### Lỗi: "Failed to fetch" hoặc CORS error

✅ **Đã sửa** - CORS config đã được update

- Nếu vẫn gặp, check Network tab trong DevTools
- Verify request headers có `Origin` header
- Response phải có header `Access-Control-Allow-Origin`

### Lỗi: Database connection timeout

✅ **Kiểm tra:**

1. Supabase có allow IP từ Render không? (hoặc set `0.0.0.0/0` để allow all)
2. Connection string format đúng chưa?
3. Database có tồn tại không?

---

## 📖 Tài liệu tham khảo

- **Full deployment guide:** `RENDER_DEPLOYMENT.md`
- **Render config:** `render.yaml`
- **Production entry point:** `wsgi.py`
- **Main app config:** `src/__init__.py`

---

## 💡 Lưu ý quan trọng

1. **Free Tier Render:**
   - App sẽ sleep sau 15 phút không có traffic
   - Request đầu tiên sau khi sleep sẽ mất 30-60s
   - → Bình thường, không phải lỗi!

2. **Security:**
   - KHÔNG commit file `.env` lên GitHub
   - Regenerate SECRET_KEY cho production (đừng dùng local key)

3. **Database:**
   - Supabase free tier tốt hơn Render PostgreSQL free
   - Nên dùng connection pooling cho production

---

## 🆘 Vẫn không được?

Nếu sau khi làm theo tất cả các bước mà vẫn gặp lỗi:

1. **Check Render Logs:**
   - Render Dashboard → Your Service → Logs
   - Copy error message

2. **Test locally với Gunicorn:**

   ```bash
   .\test_gunicorn.bat
   ```

   Nếu local cũng lỗi → vấn đề ở code
   Nếu local OK → vấn đề ở Render config

3. **Verify environment variables:**
   - Render Dashboard → Environment
   - Check all variables có giá trị đúng

4. **Test database connection:**
   ```python
   from sqlalchemy import create_engine
   engine = create_engine(FLASK_DB_URI)
   conn = engine.connect()
   ```

---

**Tóm lại:** Hầu hết các vấn đề đã được sửa trong code. Bây giờ bạn chỉ cần:

1. Push code lên GitHub
2. Set environment variables trên Render
3. Deploy!

Good luck! 🚀
