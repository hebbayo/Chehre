```markdown
# 🎭 سیستم تشخیص چهره با FastAPI

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)]()

یک سیستم کامل تشخیص چهره با استفاده از FastAPI، face_recognition و PostgreSQL که امکان ثبت، آموزش و تشخیص چهره‌ها را با احراز هویت JWT فراهم می‌کند.

## 📋 فهرست مطالب

- [ویژگی‌ها](#ویژگیها)
- [معماری سیستم](#معماری-سیستم)
- [پیش‌نیازها](#پیشنیازها)
- [نصب و راه‌اندازی](#نصب-و-راهاندازی)
- [استفاده](#استفاده)
- [API Documentation](#api-documentation)
- [ساختار دیتابیس](#ساختار-دیتابیس)
- [امنیت](#امنیت)
- [تست](#تست)
- [عیب‌یابی](#عیبیابی)
- [بهبودهای آینده](#بهبودهای-آینده)
- [مشارکت](#مشارکت)
- [لایسنس](#لایسنس)

## ✨ ویژگی‌ها

- 🔐 **احراز هویت امن**: سیستم JWT-based authentication با bcrypt hashing
- 👤 **مدیریت کاربران**: ثبت‌نام، ورود و مدیریت پروفایل کاربران
- 📸 **آپلود چهره**: آپلود و ذخیره تصاویر چهره با اعتبارسنجی
- 🧠 **آموزش مدل**: آموزش مدل تشخیص چهره با الگوریتم face_recognition
- 🔍 **تشخیص چهره**: تشخیص و شناسایی چهره‌ها از تصاویر جدید
- 📊 **لاگ‌گذاری**: ثبت تمام فعالیت‌های تشخیص چهره
- 🗄️ **دیتابیس**: استفاده از PostgreSQL برای ذخیره‌سازی داده‌ها
- 📝 **مستندات خودکار**: Swagger UI و ReDoc برای API documentation
- 🎨 **رابط کاربری**: صفحات HTML برای تست و استفاده آسان

## 🏗️ معماری سیستم

```
┌─────────────────┐
│   Frontend      │
│  (HTML/JS)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   FastAPI       │
│   Backend       │
├─────────────────┤
│ • Auth Routes   │
│ • Face Routes   │
│ • User Routes   │
└────────┬────────┘
         │
         ├──────────────┬──────────────┐
         ▼              ▼              ▼
┌─────────────┐  ┌──────────┐  ┌──────────────┐
│ PostgreSQL  │  │  File    │  │ face_recog   │
│  Database   │  │  System  │  │   Library    │
└─────────────┘  └──────────┘  └──────────────┘

## 📦 پیش‌نیازها

- Python 3.8 یا بالاتر
- PostgreSQL 12 یا بالاتر
- pip (Python package manager)
- virtualenv (توصیه می‌شود)

### کتابخانه‌های سیستمی (برای face_recognition)

**Ubuntu/Debian:**
bash
sudo apt-get update
sudo apt-get install -y python3-dev build-essential cmake
sudo apt-get install -y libopenblas-dev liblapack-dev
sudo apt-get install -y libx11-dev libgtk-3-dev

**macOS:**
bash
brew install cmake

**Windows:**
- نصب [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/)
- نصب [CMake](https://cmake.org/download/)

## 🚀 نصب و راه‌اندازی

### 1. کلون کردن پروژه

bash
git clone https://github.com/hebbayo/Chehre.git
cd Chehre

### 2. ایجاد محیط مجازی

bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate

### 3. نصب وابستگی‌ها

bash
pip install --upgrade pip
pip install -r requirements.txt

### 4. تنظیم دیتابیس PostgreSQL

bash
# ورود به PostgreSQL
psql -U postgres

# ایجاد دیتابیس
CREATE DATABASE face_recognition_db;

# ایجاد کاربر (اختیاری)
CREATE USER face_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE face_recognition_db TO face_user;

# خروج
\q

### 5. تنظیم متغیرهای محیطی

فایل `.env` در root پروژه ایجاد کنید:

env
# Database
DATABASE_URL=postgresql://postgres:your_password@localhost/face_recognition_db

# JWT
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Upload
UPLOAD_DIR=uploaded_faces
MAX_FILE_SIZE=5242880  # 5MB

# Server
HOST=0.0.0.0
PORT=8000
DEBUG=True

**تولید SECRET_KEY امن:**
bash
python -c "import secrets; print(secrets.token_urlsafe(32))"

### 6. ایجاد جداول دیتابیس

bash
python -c "from database import engine, Base; Base.metadata.create_all(bind=engine)"

### 7. اجرای سرور

bash
# حالت توسعه
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# حالت تولید
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

سرور روی `http://localhost:8000` در دسترس خواهد بود.

## 💻 استفاده

### دسترسی به مستندات API

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### مثال استفاده با cURL

#### 1. ثبت‌نام کاربر جدید

bash
curl -X POST "http://localhost:8000/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "SecurePass123!",
    "full_name": "John Doe"
  }'

#### 2. ورود و دریافت Token

bash
curl -X POST "http://localhost:8000/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john_doe&password=SecurePass123!"

پاسخ:
json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}

#### 3. آپلود تصویر چهره

bash
curl -X POST "http://localhost:8000/upload-face/" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -F "file=@path/to/image.jpg" \
  -F "label=john_doe"

#### 4. آموزش مدل

bash
curl -X POST "http://localhost:8000/train-model/" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

#### 5. تشخیص چهره

bash
curl -X POST "http://localhost:8000/recognize-face/" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -F "file=@path/to/test_image.jpg"

### مثال استفاده با Python

python
import requests

BASE_URL = "http://localhost:8000"

# ثبت‌نام
register_data = {
    "username": "jane_doe",
    "email": "jane@example.com",
    "password": "SecurePass456!",
    "full_name": "Jane Doe"
}
response = requests.post(f"{BASE_URL}/register", json=register_data)
print(response.json())

# ورود
login_data = {
    "username": "jane_doe",
    "password": "SecurePass456!"
}
response = requests.post(f"{BASE_URL}/token", data=login_data)
token = response.json()["access_token"]

# Headers با token
headers = {"Authorization": f"Bearer {token}"}

# آپلود چهره
with open("face_image.jpg", "rb") as f:
    files = {"file": f}
    data = {"label": "jane_doe"}
    response = requests.post(
        f"{BASE_URL}/upload-face/",
        headers=headers,
        files=files,
        data=data
    )
    print(response.json())

# آموزش مدل
response = requests.post(f"{BASE_URL}/train-model/", headers=headers)
print(response.json())

# تشخیص چهره
with open("test_image.jpg", "rb") as f:
    files = {"file": f}
    response = requests.post(
        f"{BASE_URL}/recognize-face/",
        headers=headers,
        files=files
    )
    print(response.json())

## 📚 API Documentation

### Authentication Endpoints

| Method | Endpoint | توضیحات | نیاز به Auth | Request Body | Response |
|:------:|:---------|:--------|:------------:|:-------------|:---------|
| `POST` | `/register` | ثبت‌نام کاربر جدید | ❌ | `UserCreate` | `User` |
| `POST` | `/token` | ورود و دریافت JWT token | ❌ | `OAuth2PasswordRequestForm` | `Token` |
| `GET` | `/users/me` | دریافت اطلاعات کاربر فعلی | ✅ | - | `User` |

**مثال Request Body برای `/register`:**
json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "SecurePass123!",
  "full_name": "John Doe"
}

**مثال Response برای `/token`:**
json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}

### Face Management Endpoints

| Method | Endpoint | توضیحات | نیاز به Auth | Parameters | Response |
|:------:|:---------|:--------|:------------:|:-----------|:---------|
| `POST` | `/upload-face/` | آپلود تصویر چهره | ✅ | `file`, `label` | `{"message": "..."}` |
| `POST` | `/train-model/` | آموزش مدل تشخیص | ✅ | - | `{"message": "..."}` |
| `POST` | `/recognize-face/` | تشخیص چهره از تصویر | ✅ | `file` | `{"recognized_faces": [...]}` |
| `GET` | `/recognition-logs/` | دریافت تاریخچه تشخیص‌ها | ✅ | `skip`, `limit` | `[RecognitionLog]` |

**مثال Response برای `/recognize-face/`:**
json
{
  "recognized_faces": [
    {
      "label": "john_doe",
      "confidence": 0.95,
      "location": {
        "top": 100,
        "right": 300,
        "bottom": 400,
        "left": 200
      }
    }
  ]
}

### Admin Endpoints

| Method | Endpoint | توضیحات | نیاز به Auth | Parameters | Response |
|:------:|:---------|:--------|:------------:|:-----------|:---------|
| `GET` | `/users/` | لیست تمام کاربران | ✅ Admin | `skip`, `limit` | `[User]` |
| `DELETE` | `/users/{user_id}` | حذف کاربر | ✅ Admin | `user_id` | `{"message": "..."}` |

### Static Pages

| Method | Endpoint | توضیحات |
|:------:|:---------|:--------|
| `GET` | `/` | صفحه اصلی |
| `GET` | `/upload` | صفحه آپلود چهره |
| `GET` | `/recognize` | صفحه تشخیص چهره |

## 🗄️ ساختار دیتابیس

### جدول `users`

| ستون | نوع | توضیحات | Constraints |
|:-----|:----|:--------|:------------|
| `id` | `Integer` | شناسه یکتا | Primary Key, Auto Increment |
| `username` | `String(50)` | نام کاربری | Unique, Not Null, Index |
| `email` | `String(100)` | ایمیل | Unique, Not Null, Index |
| `hashed_password` | `String(255)` | رمز عبور هش شده | Not Null |
| `full_name` | `String(100)` | نام کامل | Nullable |
| `is_active` | `Boolean` | وضعیت فعال بودن | Default: True |
| `is_admin` | `Boolean` | دسترسی ادمین | Default: False |
| `created_at` | `DateTime` | تاریخ ایجاد | Default: Now |

### جدول `faces`

| ستون | نوع | توضیحات | Constraints |
|:-----|:----|:--------|:------------|
| `id` | `Integer` | شناسه یکتا | Primary Key, Auto Increment |
| `user_id` | `Integer` | شناسه کاربر | Foreign Key → users.id |
| `label` | `String(100)` | برچسب چهره | Not Null, Index |
| `image_path` | `String(255)` | مسیر فایل تصویر | Not Null |
| `encoding` | `LargeBinary` | encoding چهره | Nullable |
| `uploaded_at` | `DateTime` | تاریخ آپلود | Default: Now |

### جدول `recognition_logs`

| ستون | نوع | توضیحات | Constraints |
|:-----|:----|:--------|:------------|
| `id` | `Integer` | شناسه یکتا | Primary Key, Auto Increment |
| `user_id` | `Integer` | شناسه کاربر | Foreign Key → users.id |
| `recognized_label` | `String(100)` | برچسب تشخیص داده شده | Nullable |
| `confidence` | `Float` | درصد اطمینان | Nullable |
| `image_path` | `String(255)` | مسیر تصویر تست | Nullable |
| `timestamp` | `DateTime` | زمان تشخیص | Default: Now |

### روابط جداول


users (1) ──────< (N) faces
users (1) ──────< (N) recognition_logs

## 🔒 امنیت

### اقدامات امنیتی پیاده‌سازی شده

- ✅ **Password Hashing**: استفاده از bcrypt با salt برای هش کردن رمز عبور
- ✅ **JWT Authentication**: توکن‌های JWT با expiration time
- ✅ **CORS Protection**: تنظیمات CORS برای محدود کردن دسترسی
- ✅ **Input Validation**: اعتبارسنجی ورودی‌ها با Pydantic
- ✅ **File Type Validation**: بررسی نوع فایل‌های آپلود شده
- ✅ **File Size Limit**: محدودیت حجم فایل‌های آپلودی
- ✅ **SQL Injection Prevention**: استفاده از ORM (SQLAlchemy)
- ✅ **Rate Limiting**: محدودیت تعداد درخواست‌ها (توصیه می‌شود)

### Checklist امنیتی برای Production

- [ ] تغییر `SECRET_KEY` به یک مقدار تصادفی و امن
- [ ] فعال کردن HTTPS
- [ ] تنظیم CORS origins به دامنه‌های مشخص
- [ ] فعال کردن rate limiting
- [ ] استفاده از environment variables برای اطلاعات حساس
- [ ] فعال کردن logging و monitoring
- [ ] بک‌آپ منظم دیتابیس
- [ ] استفاده از reverse proxy (nginx/apache)
- [ ] فعال کردن firewall
- [ ] بررسی و به‌روزرسانی منظم وابستگی‌ها

### مثال تنظیمات CORS برای Production

python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # دامنه‌های مجاز
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

## 🧪 تست

### تست دستی با Swagger UI

1. به `http://localhost:8000/docs` بروید
2. از بخش "Authorize" وارد شوید
3. API endpoints را تست کنید

### تست با pytest (در صورت وجود تست‌ها)

bash
# نصب pytest
pip install pytest pytest-asyncio httpx

# اجرای تست‌ها
pytest tests/ -v

# اجرای تست‌ها با coverage
pytest tests/ --cov=. --cov-report=html

### مثال تست ساده

python
# tests/test_auth.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_register_user():
    response = client.post(
        "/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "TestPass123!",
            "full_name": "Test User"
        }
    )
    assert response.status_code == 200
    assert "id" in response.json()

def test_login():
    response = client.post(
        "/token",
        data={
            "username": "testuser",
            "password": "TestPass123!"
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

## 🔧 عیب‌یابی

### مشکلات رایج و راه‌حل‌ها

#### 1. خطای نصب face_recognition

**مشکل:**

ERROR: Could not build wheels for dlib

**راه‌حل:**
bash
# Ubuntu/Debian
sudo apt-get install build-essential cmake

# macOS
brew install cmake

# Windows
# نصب Visual Studio Build Tools

#### 2. خطای اتصال به دیتابیس

**مشکل:**

sqlalchemy.exc.OperationalError: could not connect to server

**راه‌حل:**
- بررسی کنید PostgreSQL در حال اجرا است
- `DATABASE_URL` در `.env` را بررسی کنید
- دسترسی‌های کاربر دیتابیس را چک کنید

bash
# بررسی وضعیت PostgreSQL
sudo systemctl status postgresql

# راه‌اندازی PostgreSQL
sudo systemctl start postgresql

#### 3. خطای JWT Token

**مشکل:**

Could not validate credentials

**راه‌حل:**
- مطمئن شوید token منقضی نشده است
- `SECRET_KEY` را بررسی کنید
- فرمت header را چک کنید: `Authorization: Bearer <token>`

#### 4. خطای آپلود فایل

**مشکل:**

File size exceeds maximum allowed size

**راه‌حل:**
- حجم فایل را کاهش دهید (حداکثر 5MB)
- فرمت فایل را بررسی کنید (فقط JPG, PNG)

#### 5. خطای تشخیص چهره

**مشکل:**

No faces found in the image

**راه‌حل:**
- کیفیت تصویر را بهبود دهید
- نور کافی در تصویر داشته باشید
- چهره باید واضح و رو به دوربین باشد
- از تصاویر با رزولوشن بالاتر استفاده کنید

### لاگ‌ها

برای مشاهده لاگ‌های دقیق‌تر:

bash
# اجرا با لاگ debug
uvicorn main:app --reload --log-level debug

# ذخیره لاگ‌ها در فایل
uvicorn main:app --reload --log-config logging.conf

## 🚀 بهبودهای آینده

### ویژگی‌های پیشنهادی

- [ ] **Real-time Recognition**: تشخیص چهره از وب‌کم به صورت زنده
- [ ] **Multi-face Detection**: تشخیص چند چهره همزمان
- [ ] **Face Clustering**: گروه‌بندی خودکار چهره‌های مشابه
- [ ] **Age & Gender Detection**: تشخیص سن و جنسیت
- [ ] **Emotion Recognition**: تشخیص احساسات از چهره
- [ ] **Face Mask Detection**: تشخیص ماسک روی چهره
- [ ] **Liveness Detection**: تشخیص چهره واقعی از عکس
- [ ] **Dashboard**: داشبورد مدیریتی با آمار و نمودار
- [ ] **Mobile App**: اپلیکیشن موبایل (React Native/Flutter)
- [ ] **Docker Support**: Containerization با Docker
- [ ] **CI/CD Pipeline**: اتوماسیون deployment
- [ ] **Microservices**: تبدیل به معماری microservices
- [ ] **Redis Caching**: کش کردن نتایج با Redis
- [ ] **Message Queue**: استفاده از Celery/RabbitMQ برای پردازش async
- [ ] **Cloud Storage**: ذخیره تصاویر در S3/MinIO

### بهبودهای فنی

- [ ] استفاده از مدل‌های پیشرفته‌تر (FaceNet, ArcFace)
- [ ] بهینه‌سازی سرعت پردازش
- [ ] پشتیبانی از GPU
- [ ] افزودن unit tests و integration tests
- [ ] مستندسازی کامل با Sphinx
- [ ] پیاده‌سازی WebSocket برای real-time updates
- [ ] افزودن Prometheus metrics
- [ ] پیاده‌سازی GraphQL API

## 🤝 مشارکت

مشارکت شما در بهبود این پروژه خوشایند است!

### مراحل مشارکت

1. **Fork** کردن پروژه
2. ایجاد **Branch** جدید:
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit** کردن تغییرات:
   ```bash
   git commit -m "Add some amazing feature"
   ```
4. **Push** کردن به Branch:
   ```bash
   git push origin feature/amazing-feature
   ```
5. ایجاد **Pull Request**

### راهنمای کدنویسی

- از PEP 8 style guide پیروی کنید
- کد را با docstring مستند کنید
- تست برای کد جدید بنویسید
- commit message‌ها را واضح و توصیفی بنویسید

### گزارش باگ

برای گزارش باگ، یک Issue با اطلاعات زیر ایجاد کنید:

- توضیح مشکل
- مراحل بازتولید باگ
- رفتار مورد انتظار
- رفتار واقعی
- اسکرین‌شات (در صورت نیاز)
- محیط (OS, Python version, etc.)

## 📄 لایسنس

این پروژه تحت لایسنس MIT منتشر شده است. برای جزئیات بیشتر فایل [LICENSE](LICENSE) را مطالعه کنید.

## 📞 تماس و پشتیبانی

- **GitHub**: [@hebbayo](https://github.com/hebbayo)
- **Repository**: [Chehre](https://github.com/hebbayo/Chehre)
- **Issues**: [GitHub Issues](https://github.com/hebbayo/Chehre/issues)

---

<div align="center">

**ساخته شده با ❤️ توسط [hebbayo](https://github.com/hebbayo)**

اگر این پروژه برای شما مفید بود، یک ⭐ بدهید!

</div>
