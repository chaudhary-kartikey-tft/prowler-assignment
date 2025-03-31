from __future__ import absolute_import, unicode_literals

import os
from django.conf import settings
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ProwlerAnalysis.settings')

app = Celery('ProwlerAnalysis')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Dynamically set `task_always_eager` based on `CELERY_ALWAYS_EAGER` from Django settings.
app.conf.task_always_eager = getattr(settings, 'CELERY_ALWAYS_EAGER', False)

# Automatically discover tasks from all installed apps
app.autodiscover_tasks()
