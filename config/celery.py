import os
from celery import Celery

# Set default Django settings module for Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# Load task modules from all registered Django app configs
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from installed Django apps
app.autodiscover_tasks()