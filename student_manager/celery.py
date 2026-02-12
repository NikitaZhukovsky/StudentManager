import os
from celery import Celery
from celery.schedules import crontab
from .celery_tasks import update_daily_data

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "student_manager.settings")

app = Celery("student_manager")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "daily-update-data-at-6": {
        "task": "student_manager.celery_tasks.update_daily_data",
        "schedule": crontab(hour=6, minute=0),
        "args": (),
    },
}

app.conf.timezone = "UTC"

