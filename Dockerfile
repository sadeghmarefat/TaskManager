# استفاده از ایمیج پایه پایتون
FROM python:3.11-slim

# تنظیم متغیرهای محیطی برای پایتون
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ساخت و تنظیم پوشه کاری داخل کانتینر
WORKDIR /app

# نصب پیش‌نیازهای سیستم‌عامل (برای اتصال به postgresql و...)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# کپی کردن فایل requirements و نصب پکیج‌ها
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# کپی کردن تمام کدهای پروژه به داخل کانتینر
COPY . /app/

# پورت اجرایی جنگو
EXPOSE 8000

# دستور اجرای پروژه
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]