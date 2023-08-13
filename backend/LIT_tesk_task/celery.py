import os
from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LIT_tesk_task.settings")
app = Celery("LIT_tesk_task")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
