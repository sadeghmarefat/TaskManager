from celery import shared_task
import time

@shared_task
def send_task_notification(user_email, task_title):
    # شبیه‌سازی یک کار زمان‌بر (مثل ارسال ایمیل)
    time.sleep(3)
    print(f">>> [Celery Task] Notification email sent to {user_email} for task: '{task_title}'")
    return "Email sent successfully"