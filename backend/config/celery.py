import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Ось цей 'app' шукає воркер, коли ми пишемо "celery -A config"
app = Celery('config')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()