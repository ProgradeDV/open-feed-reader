"""site_base.views"""
from logging import getLogger
from urllib.parse import  urlparse, ParseResult
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse
from django.http import Http404
from django.db.models import Q
from site_base.forms import SearchForm
from site_base.views import paginator_args
from feeds.models import Entry, Source
from feeds.url_converters import get_rss_url
from feeds.fetch import fetch_feed
from .models import SourceSubcription

logger = getLogger('feed_subscriptions/views.py')


ITEMS_PER_PAGE = 20


@login_required
def edit_subscriptions_page(request: HttpResponse):
    """view for the page of all known feeds"""

    return render(
        request,
        'subscriptions/edit_subs_page.html',
        context={
            'navbar_title':'All Feeds',
            },
        )



@login_required
def all_subed_feed(request: HttpResponse):
    """all entries from the users subscribed feeds"""
    entries = Entry.objects.filter(source__subscriptions__user = request.user).order_by('-created')

    page = int(request.GET.get("page", 1))
    context = paginator_args(page, entries)
    context['navbar_title'] = 'My Feeds'

    return render(
        request,
        'folders/folder_page.html',
        context=context,
        )



@login_required
def subscribe_feed(request: HttpResponse, id: int):
    """subscribe to the feed with the given id"""
    # reject non post requests
    if request.method != "POST":
        return HttpResponse(status=405) # Method Not Allowed

    # reject subscriptions to feeds that don't exist
    try:
        feed = Source.objects.get(id = id)
    except Source.DoesNotExist:
        return Http404("Feed not Found")

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
    return render(request, 'subscriptions/actions/unsubscribe_btn.html', context={'id':id})



@login_required
def unsubscribe_feed(request: HttpResponse, id: int):
    """Unsubscribe the user from the feed with the given id"""
    if request.method != "POST":
        return HttpResponse(status=405) # Method Not Allowed

    try:
        # find the subscription
        sub = SourceSubcription.objects.filter(user = request.user).get(source = id)

    except SourceSubcription.DoesNotExist:
        logger.debug('%s is not subscribed to %s', request.user, id)
        return Http404("Subscription not Found")

    logger.debug('%s unsubscribing from %s', request.user, sub.source.name)
    feed = sub.source

    # remove the feed from all of the users folders
    for folder in request.user.source_folders.all():
        folder.feeds.remove(feed)

    sub.delete()

    # return a subscribe button
    return render(request, 'subscriptions/actions/resubscribe_btn.html', context={'id':id})



@login_required
def all_subs_search(request: HttpResponse):
    """view for the responst to the htmx request for searching for a feed"""
    if request.method != "POST":
        return HttpResponse(status=405) # Method Not Allowed

    # check whether it's valid:
    form = SearchForm(request.POST)
    if not form.is_valid():
        return HttpResponse(content='Invalid Form')

    # get the search results
    search_text = form.cleaned_data['search_text']
    parsed_url = urlparse(search_text)
    if parsed_url.scheme:
        rss_url = get_rss_url(parsed_url)
        matched_feeds = feeds_search_url(request, rss_url)

        if not matched_feeds.count():
            return new_feed_search(request, rss_url)
    else:
        matched_feeds = feeds_search_text(request, search_text)

    if matched_feeds.count():
        page = int(request.GET.get("page", 1))
        context = paginator_args(page, matched_feeds)

        return render(
            request,
            'subscriptions/search/paginated_feeds_list.html',
            context=context
        )

    return HttpResponse('')


def feeds_search_text(request: HttpResponse, search_text:str):
    """search the database for feeds matching the given text
    
    Returns a set of matches
    """
    # if empty search text, return all feeds
    if not search_text:
        return Source.objects\
            .filter(subscriptions__user = request.user)\
            .order_by('title')

    # matches if search_text is in the name or title
    return Source.objects\
        .filter(subscriptions__user = request.user)\
        .filter(Q(title__icontains = search_text) | Q(name__icontains = search_text))\
        .order_by('title')


def feeds_search_url(request: HttpResponse, search_text:str):
    """search the database for feeds matching the given text
    
    Returns a set of matches
    """
    # if empty search text, return all feeds
    if not search_text:
        return Source.objects\
            .filter(subscriptions__user = request.user)\
            .order_by('title')

    # valid links matching the feed or site url
    return Source.objects\
        .filter(subscriptions__user = request.user)\
        .filter(Q(feed_url = search_text) | Q(site_url = search_text))\
        .order_by('title')


def new_feed_search(request: HttpResponse, rss_url:str):
    """create a new feed, return a search result"""
    new_source = Source(feed_url=rss_url)
    fetch_feed(new_source, no_cache=True)

    return render(
        request,
        'subscriptions/search/search_item_not_subed.html',
        context={'feed':new_source},
    )
