"""The main open-feed-reader django app."""
from .celery import celery_app

__all__ = ("celery_app",)
