from __future__ import absolute_import, unicode_literals
import os
from django.conf import settings
from celery import Celery

CELERY_ENABLE_UTC = False
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gitsearch.settings')


app = Celery(
    'main',
    backend='amqp',
    broker='amqp://guest@localhost//'
)

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.timezone = 'UTC'
