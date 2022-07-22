import os
from celery import Celery
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drones.settings')
app = Celery('drones')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print("Doing async task")
    time.sleep(2)
    print("Task is done")
