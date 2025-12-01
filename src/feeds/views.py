"""Views for managing feed sources."""
import logging

from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_page

from feeds.models import Entry, Source
from site_base.views import paginator_args

logger = logging.getLogger("feed_management")


@login_required
def feed_page(request: HttpRequest, feed_id: int) -> HttpResponse:
    """Page for a single feed and it's entries."""
    context = {
        "feed_id": feed_id,
        "is_subed": request.user.subscriptions.filter(id=feed_id).exists(),
    }

    return render(
        request,
        "feeds/feed_page.html",
        context=context,
        )


@cache_page(60*15)
@login_required
def feed_page_content(request: HttpRequest, feed_id:int) -> HttpResponse:
    """Page of feed content. It is a seperate view in order to optimize caching."""
    try:
        feed = Source.objects.get(id=feed_id)
    except Entry.DoesNotExist:
        raise Http404("Feed Not Found")  # noqa: B904

    entries = Entry.objects.filter(source = feed).order_by("-created")
    page = int(request.GET.get("page", 1))
    context = paginator_args(page, entries)
    context["feed"] = feed

    return render(
        request,
        "feeds/feed_page_content.html",
        context=context,
        )


@login_required
def entry_page(request: HttpRequest, entry_id: int) -> HttpResponse:
    """View for a single entry."""
    try:
        entry = Entry.objects.get(id=entry_id)
    except Entry.DoesNotExist:
        raise Http404("Entry Not Found")  # noqa: B904

    return render(request,
        "entries/entry_page.html",
        context={
            "entry":entry,
            },
        )
