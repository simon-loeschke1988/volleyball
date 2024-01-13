import os
from celery import Celery
from django.conf import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'applikation.settings')

app = Celery('applikation', broker='amqp://guest:guest@rabbitmq:5672//')

app.config_from_object(settings, namespace='CELERY')
app.autodiscover_tasks()
