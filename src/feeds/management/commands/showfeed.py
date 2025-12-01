"""Django Command to shwo the data for a feed."""
import logging
from argparse import ArgumentParser

from django.core.management.base import BaseCommand, CommandError

from feeds.models import Source

LOGGER = logging.getLogger("ShowFeed")

DISPLAY_KEYS = [
    "name",
    "title",
    "subtitle",
    "last_polled",
    "due_poll",
    "site_url",
    "feed_url",
    "image_url",
    "icon_url",
    "author",
    "description",
]


class Command(BaseCommand):
    """Command to query and show the data for a feed."""

    help = "Print most fields for a given feed"

    def add_arguments(self, parser:ArgumentParser) -> None:
        """Add arguments to the command parser."""
        parser.add_argument("--url", type=str)
        parser.add_argument("--name", type=str)


    def handle(self, *args:any, **options:any) -> None:  # noqa: ARG002
        """Query and show the data for a feed."""
        if options["url"]:
            source = Source.objects.get(feed_url=options["url"])

        elif options["name"]:
            source = Source.objects.get(name=options["name"])

        else:
            raise CommandError("must supply either --name or --url")

        for key in DISPLAY_KEYS:
            value = getattr(source, key, None)
            self.stdout.write(f"{key:<11} = {value}")

        self.stdout.write(self.style.SUCCESS("Finished"))
