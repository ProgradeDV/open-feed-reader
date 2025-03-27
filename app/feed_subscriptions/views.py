"""site_base.views"""
from logging import getLogger
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, HttpResponse
from site_base.forms import SearchForm
from site_base.views import paginator_args
from feeds.models import Entry, Source
from .models import SourceSubcription

logger = getLogger('feed_subscriptions/views.py')


ITEMS_PER_PAGE = 20


@login_required
def user_feed(request: HttpResponse):
    """all entries from the users subscribed feeds"""
    entries = Entry.objects.filter(source__subscriptions__user = request.user).order_by('-created')

    page = int(request.GET.get("page", 1))
    context = paginator_args(page, entries)
    context['navbar_title'] = 'My Feed'

    return render(
        request,
        'entries/entries_list.html',
        context=context,
        )



@login_required
def subscribe_feed(request: HttpResponse, id: int):
    """subscribe to the feed with the given id"""
    # reject non post requests
    if request.method != "POST":
        return None

    # reject subscriptions to feeds that don't exist
    try:
        feed = Source.objects.get(id = id)
    except Source.DoesNotExist:
        return None

    # check if you are already subscribed to that feed
    try:
        sub = SourceSubcription.objects.filter(user = request.user).get(source = feed)

    except SourceSubcription.DoesNotExist:
        # if the subscription doesn't exist, subscribe
        logger.debug('%s subscribing to %s', request.user, feed.name)
        sub = SourceSubcription(user = request.user, source = feed)
        sub.save()

    else:
        # if you're already subscribed
        logger.debug('%s is already subscribed to %s', request.user, feed.name)

    # return an unsubscribe button
    return render(request, 'subscriptions/unsubscribe.html', context={'id':id})



@login_required
def unsubscribe_feed(request: HttpResponse, id: int):
    """Unsubscribe the user from the feed with the given id"""
    if request.method != "POST":
        return None

    try:
        # find the subscription
        sub = SourceSubcription.objects.filter(user = request.user).get(source = id)

    except SourceSubcription.DoesNotExist:
        logger.debug('%s is not subscribed to %s', request.user, id)

    else:
        logger.debug('%s unsubscribing from %s', request.user, sub.source.name)
        sub.delete()

    # return a subscribe button
    return render(request, 'subscriptions/subscribe.html', context={'id':id})
