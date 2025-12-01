"""Register models for admin panel management."""
from typing import ClassVar

from django.contrib import admin, messages
from django.db.models import QuerySet
from django.http import HttpRequest
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import ngettext

from feeds import models
from feeds.fetch import fetch_feed


class SourceAdmin(admin.ModelAdmin):
    """Adds link to a sources entries to the admin panel."""

    list_display:ClassVar[list] = ["display_name", "entries_link", "status_code", "last_result", "due_fetch"]
    readonly_fields:ClassVar[list] = ("entries_link",)
    actions:ClassVar[list] = ["fetch_feeds"]


    @admin.action(description="Fetch selected feeds")
    def fetch_feeds(self, request:HttpRequest, queryset:QuerySet) -> None:
        """Admin Action to update the selected sources."""
        sucsesses = 0
        failed = 0

        for source in queryset:
            fetch_feed(source, no_cache=True)
            if source.status_code < 400:  # noqa: PLR2004
                sucsesses += 1
            else:
                failed += 1

        message = ngettext(
                f"{sucsesses} feed was updated.",  # noqa: INT001
                f"{sucsesses} feeds were updated.",
                sucsesses,
            ) + f" {failed} failed"

        self.message_user(
            request,
            message,
            messages.SUCCESS if failed == 0 else messages.ERROR,
        )

    def entries_link(self, source: models.Source) -> str:
        """HTML link string to the given sources entries."""
        if source.id is None:
            return ""
        count = source.entries.all().count()
        url = reverse("admin:feeds_entry_changelist")

        return mark_safe(f'<a href="{url}?source__id={source.id:d}" target="_blank">{count:d} Posts</a>')  # noqa: S308
    entries_link.short_description = "entries"



class EntryAdmin(admin.ModelAdmin):
    """Adds a link to a entry's enclosures to the admin panel."""

    raw_id_fields = ("source",)
    list_display = ("title", "enclosures_link", "source", "created", "guid", "author")
    search_fields = ("title",)
    ordering = ("-created",)

    readonly_fields = (
        "enclosures_link",
    )

    def enclosures_link(self, entry: models.Entry) -> str:
        """HTML link to the given entry's enclosures."""
        if entry.id is None:
            return ""
        count = entry.enclosures.all().count()
        url = reverse("admin:feeds_enclosure_changelist")


        return mark_safe(f'<a href="{url}?entry__id={entry,id:d}" target="_blank">{count:d} Enclosures</a>')  # noqa: S308
    enclosures_link.short_description = "enclosures"



class EnclosureAdmin(admin.ModelAdmin):
    """Admin panel for enclosures."""

    raw_id_fields = ("entry",)
    list_display = ("href", "type")


admin.site.register(models.Source, SourceAdmin)
admin.site.register(models.Entry, EntryAdmin)
admin.site.register(models.Enclosure, EnclosureAdmin)
