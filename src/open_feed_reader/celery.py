"""Celery service."""
import os
from logging import getLogger

from celery import Celery
from django.conf import settings

logger = getLogger("Celery")

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "open_feed_reader.settings")

celery_app = Celery("open_feed_reader")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
celery_app.config_from_object(settings, namespace="CELERY")

# Load task modules from all registered Django apps.
celery_app.autodiscover_tasks()

