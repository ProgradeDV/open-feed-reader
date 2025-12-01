"""Admin panel config for feed folders."""
from typing import ClassVar

from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from feeds.models import Source

from .models import FeedsFolder


class FeedsFolderAdmin(admin.ModelAdmin):
    """Adds link to a sources entries to the admin panel."""

    list_display:ClassVar[list] = ["name", "user", "feeds_count"]
    list_filter:ClassVar[list] = ["name", "user"]

    def feeds_count(self, folder:FeedsFolder) -> str:
        """HTML link string to the feeds list."""
        if folder.id is None:
            return ""
        qs = folder.feeds.count()

        link = reverse(f"admin:{Source._meta.app_label}_{Source._meta.model_name}_changelist")

        return mark_safe(f'<a href="{link}?folders__id={folder.id:d}" target="_blank">{qs:d} Feeds</a>')  # noqa: S308

    feeds_count.short_description = "feeds"


# Register your models here.
admin.site.register(FeedsFolder, FeedsFolderAdmin)
