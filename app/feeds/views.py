"""views for managing feed sources"""
import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse
from django.http import Http404
from site_base.views import paginator_args
from feeds.models import Source, Entry

logger = logging.getLogger("feed_management")


@login_required
def feed_page(request: HttpResponse, id: int):
    """the view for a single feed and it's entries"""
    try:
        feed = Source.objects.get(id=id)
    except Entry.DoesNotExist:
        raise Http404("Feed Not Found")

    entries = Entry.objects.filter(source = feed).order_by('-created')
    is_subed = feed.subscribers.filter(id=request.user.id).exists()

    page = int(request.GET.get("page", 1))
    context = paginator_args(page, entries)
    context['feed'] = feed
    context['is_subed'] = is_subed

    return render(
        request,
        'feeds/feed_page.html',
        context=context,
        )


@login_required
def entry_page(request: HttpResponse, entry_id: int):
    """view for a single entry"""
    try:
        entry = Entry.objects.get(id=entry_id)
    except Entry.DoesNotExist:
        raise Http404("Entry Not Found")

    return render(request,
        'entries/entry_page.html',
        context={
            'entry':entry,
            },
        )
