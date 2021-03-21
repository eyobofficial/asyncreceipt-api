from __future__ import absolute_import, unicode_literals

import os
from celery import Celery
from decouple import config

from django.conf import settings

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    config('DJANGO_SETTINGS_MODULE')
)

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.broker_url = config('CELERY_BROKER_URL')
app.conf.beat_scheduler = 'django_celery_beat.schedulers.DatabaseScheduler'
