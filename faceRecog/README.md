# 🎭 سیستم تشخیص چهره با FastAPI

یک API کامل برای تشخیص و شناسایی چهره با استفاده از FastAPI، OpenCV و PostgreSQL.

## ✨ ویژگی‌ها

- 🔍 **تشخیص چهره**: استفاده از Haar Cascade برای تشخیص چهره در تصاویر
- 🧬 **استخراج ویژگی**: ترکیب LBP و HOG برای استخراج embedding چهره
- 👤 **مدیریت افراد**: ثبت و مدیریت اطلاعات افراد
- 📸 **ذخیره تصاویر**: آپلود و ذخیره تصاویر چهره
- 🔐 **پایگاه داده PostgreSQL**: ذخیره‌سازی امن و مقیاس‌پذیر
- ⚡ **API سریع**: ساخته شده با FastAPI
- 📊 **Type Safety**: استفاده کامل از Type Hints

## 🏗️ معماری
app/

├── main.py # نقطه ورود اصلی FastAPI

├── database.py # مدیریت اتصال PostgreSQL

├── crud.py # عملیات پایگاه داده (20+ تابع)

├── face_recognition.py # الگوریتم‌های تشخیص چهره

└── routers/

├── persons.py # API مدیریت افراد

├── faces.py # API مدیریت تصاویر

└── embeddings.py # API استخراج و تطبیق چهره

🚀 نصب و راه‌اندازی
پیش‌نیازها
Python 3.8+
PostgreSQL 12+
pip
مرحله ۱: کلون کردن پروژه
bash

git clone https://github.com/YOUR_USERNAME/face-recognition-api.git

cd face-recognition-api

مرحله ۲: ایجاد محیط مجازی
bash

python -m venv venv

در Windows:
venv\Scripts\activate

در Linux/Mac:
source venv/bin/activate

مرحله ۳: نصب وابستگی‌ها
bash

pip install -r requirements.txt

مرحله ۴: تنظیم پایگاه داده
bash

ایجاد دیتابیس در PostgreSQL
psql -U postgres

CREATE DATABASE face_recognition;

\q

اجرای اسکریپت ایجاد جداول
psql -U postgres -d face_recognition -f schema.sql

مرحله ۵: تنظیم متغیرهای محیطی
فایل .env بسازید:

env

DB_HOST=localhost

DB_PORT=5432

DB_NAME=face_recognition

DB_USER=postgres

DB_PASSWORD=your_password

مرحله ۶: اجرای سرور
bash

uvicorn app.main:app --reload

سرور روی http://localhost:8000 اجرا می‌شود.

📚 مستندات API
بعد از اجرا، مستندات تعاملی در دسترس است:

Swagger UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc
🔌 Endpoints اصلی
مدیریت افراد
http

POST /persons/ # ایجاد شخص جدید

GET /persons/{id} # دریافت اطلاعات شخص

GET /persons/ # لیست تمام افراد

DELETE /persons/{id} # حذف شخص

مدیریت تصاویر
http

POST /faces/upload # آپلود تصویر چهره

GET /faces/{id} # دریافت تصویر

GET /faces/person/{id} # تصاویر یک شخص

DELETE /faces/{id} # حذف تصویر

تشخیص و تطبیق
http

POST /embeddings/extract/{face_id} # استخراج embedding

POST /embeddings/recognize # تشخیص چهره در تصویر جدید

GET /embeddings/person/{person_id} # embeddings یک شخص

💡 مثال استفاده
۱. ثبت شخص جدید
bash

curl -X POST “http://localhost:8000/persons/” \

-H “Content-Type: application/json” \

-d ‘{“name”: “علی احمدی”, “metadata”: {“age”: 25}}’

۲. آپلود تصویر
bash

curl -X POST “http://localhost:8000/faces/upload?person_id=1” \

-F “file=@photo.jpg”

۳. استخراج embedding
bash

curl -X POST “http://localhost:8000/embeddings/extract/1”

۴. تشخیص چهره
bash

curl -X POST “http://localhost:8000/embeddings/recognize” \

-F “file=@unknown.jpg”

🛠️ تکنولوژی‌های استفاده شده
FastAPI: فریمورک وب مدرن و سریع
OpenCV: پردازش تصویر و تشخیص چهره
NumPy: محاسبات عددی
scikit-image: استخراج ویژگی HOG
PostgreSQL: پایگاه داده رابطه‌ای
psycopg2: درایور PostgreSQL
Pydantic: اعتبارسنجی داده
python-multipart: آپلود فایل
📊 ساختار دیتابیس
جدول persons
id: شناسه یکتا
name: نام شخص
metadata: اطلاعات اضافی (JSONB)
created_at: تاریخ ایجاد
جدول face_images
id: شناسه یکتا
person_id: ارجاع به شخص
image_data: داده باینری تصویر
uploaded_at: تاریخ آپلود
جدول face_embeddings
id: شناسه یکتا
face_image_id: ارجاع به تصویر
embedding: بردار ویژگی (BYTEA)
created_at: تاریخ ایجاد
🔒 امنیت
✅ استفاده از متغیرهای محیطی برای اطلاعات حساس
✅ Prepared statements برای جلوگیری از SQL Injection
✅ اعتبارسنجی ورودی با Pydantic
⚠️ توجه: برای production، احراز هویت و authorization اضافه کنید
🧪 تست
bash

نصب pytest
pip install pytest pytest-asyncio httpx

اجرای تست‌ها
pytest tests/

📈 بهبودهای آینده
[ ] افزودن احراز هویت JWT
[ ] استفاده از مدل‌های deep learning (FaceNet, ArcFace)
[ ] پشتیبانی از تشخیص چند چهره همزمان
[ ] اضافه کردن Redis برای کش
[ ] Docker و Docker Compose
[ ] CI/CD با GitHub Actions
[ ] مستندات کامل‌تر
🤝 مشارکت
Fork کنید
برنچ feature بسازید (git checkout -b feature/AmazingFeature)
تغییرات را commit کنید (git commit -m 'Add some AmazingFeature')
Push کنید (git push origin feature/AmazingFeature)
Pull Request باز کنید
## 🚀 نصب و راه‌اندازی

### پیش‌نیازها

- Python 3.8+
- PostgreSQL 12+
- pip

### مرحله ۱: کلون کردن پروژه
```bash
git clone https://github.com/YOUR_USERNAME/face-recognition-api.git
cd face-recognition-api

### مرحله ۲: ایجاد محیط مجازی

bash
python -m venv venv

# در Windows:
venv\Scripts\activate

# در Linux/Mac:
source venv/bin/activate

### مرحله ۳: نصب وابستگی‌ها

**همه پکیج‌ها به صورت خودکار از `requirements.txt` نصب می‌شوند:**

bash
pip install -r requirements.txt

**یا اگر مشکل داشتید، به صورت دستی:**

bash
pip install fastapi uvicorn[standard] python-multipart psycopg2-binary opencv-python numpy scikit-image pydantic python-dotenv

> **نکته**: نصب OpenCV ممکن است چند دقیقه طول بکشد.

### مرحله ۴: تنظیم پایگاه داده

bash
# ایجاد دیتابیس در PostgreSQL
psql -U postgres
CREATE DATABASE face_recognition;
\q

### مرحله ۵: تنظیم متغیرهای محیطی

فایل `.env` در ریشه پروژه بسازید:

env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=face_recognition
DB_USER=postgres
DB_PASSWORD=your_password

> **هشدار امنیتی**: هرگز فایل `.env` را commit نکنید!

### مرحله ۶: اجرای سرور

bash
uvicorn app.main:app --reload

سرور روی `http://localhost:8000` اجرا می‌شود.

### مرحله ۷: بررسی نصب

مرورگر را باز کنید و به این آدرس بروید:
- http://localhost:8000/docs (مستندات Swagger)

اگر صفحه مستندات را دیدید، نصب موفق بوده است! ✅


### ۴. حالا مشکل push را حل می‌کنیم:

```bash
# اگر قبلاً venv را add کرده‌ای، باید از git حذفش کنی:
git rm -r --cached venv/
git rm -r --cached __pycache__/

# حالا تمام تغییرات را add کن:
git add .

# commit کن:
git commit -m "Remove venv and add proper .gitignore"

# push کن:
git push origin main

📝 لایسنس
این پروژه تحت لایسنس MIT منتشر شده است.

👨‍💻 توسعه‌دهنده
@hebbayo

لینک پروژه: https://github.com/hebbayo/Chehre

🙏 تشکر
FastAPI
OpenCV
PostgreSQL
