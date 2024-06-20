# смотри __init__.py

import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eleng.settings')

app = Celery('eleng')
app.config_from_object('django.conf:settings', namespace='CELERY')

# автоматически подцеплять таски
app.autodiscover_tasks()

