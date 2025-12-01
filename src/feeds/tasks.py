"""Celery Tasks for warframe_django_interface."""
from logging import getLogger

from celery import shared_task

from feeds.fetch import fetch_feed
from feeds.fetch.predict import due_sources

logger = getLogger("Tasks")

@shared_task
def update_feeds() -> None:
    """Vertsion of update_all_content wrapped by celery registry."""
    sources = due_sources()
    for source in sources:
        fetch_feed(source)

