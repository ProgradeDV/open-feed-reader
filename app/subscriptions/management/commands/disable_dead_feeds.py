"""
Django command to disable feeds with no subscribers
"""
import logging
from django.core.management.base import BaseCommand, CommandError
from feeds.models import Source

logger = logging.getLogger('DisableFeeds')


class Command(BaseCommand):
    """
    Command to disable all feeds that have no subscribers
    """
    help = 'Disable all feeds that have no Subscribers'

    def handle(self, *args, **options):
        # query for feeds with no subscribers
        logger.info('Disabling feeds with no subscribers')
        sources = Source.objects.filter(live=True, subscriptions__isnull = True)

        for source in sources:
            logger.info("Disabling Feed: %s", source)
            source.live = False
            source.save(update_fields=['live'])

        self.stdout.write(self.style.SUCCESS('Finished'))
