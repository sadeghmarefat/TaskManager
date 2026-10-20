import os
from celery import Celery

# تنظیم ماژول تنظیمات پیش‌فرض جنگو برای سلری
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TaskManager.settings')

app = Celery('TaskManager')

# خواندن تنظیمات سلری از فایل settings.py جنگو با پیشوند CELERY
app.config_from_object('django.conf:settings', namespace='CELERY')

# پیدا کردن خودکار فایل‌های tasks.py در تمام اپلیکیشن‌های پروژه
app.autodiscover_tasks()