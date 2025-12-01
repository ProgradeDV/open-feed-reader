"""App config for the site base."""
from django.apps import AppConfig


class SiteBaseConfig(AppConfig):
    """App config for the site base."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "site_base"
