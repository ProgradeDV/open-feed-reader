"""App config for the Feeds Folders."""
from django.apps import AppConfig


class FeedsFoldersConfig(AppConfig):
    """App config for the Feeds Folders."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "feeds_folders"

    def ready(self) -> None:  # noqa: D102
        pass
