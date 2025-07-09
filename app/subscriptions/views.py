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
from feeds.fetch import new_feed


logger = getLogger('subscriptions/views.py')


ITEMS_PER_PAGE = 20


@login_required
def edit_subscriptions_page(request: HttpResponse):
    """view for the page of all known feeds"""

    return render(
        request,
        'subscriptions/edit_subs_page.html',
        context={
            'navbar_title':'Subscribe to Feeds',
            },
        )



@login_required
def all_subed_feed(request: HttpResponse):
    """all entries from the users subscribed feeds"""
    entries = Entry.objects.filter(source__subscribers = request.user).order_by('-created')

    page = int(request.GET.get("page", 1))
    context = paginator_args(page, entries)
    context['navbar_title'] = 'All Feeds'

    return render(
        request,
        'entries/entries_list_page.html',
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
    if feed.subscribers.filter(id=request.user.id).exists():
        logger.debug('%s is already subscribed to %s',  request.user, feed)

    else:
        logger.debug('%s subscribing to %s', request.user, feed)
        feed.subscribers.add(request.user)

    # return an unsubscribe button
    return render(request, 'subscriptions/actions/unsubscribe_btn.html', context={'id':id})



@login_required
def unsubscribe_feed(request: HttpResponse, id: int):
    """Unsubscribe the user from the feed with the given id"""
    if request.method != "POST":
        return HttpResponse(status=405) # Method Not Allowed

    try:
        feed = Source.objects.get(id = id)
    except Source.DoesNotExist:
        return Http404("Feed not Found")

    if not feed.subscribers.filter(id=request.user.id).exists():
        logger.debug('%s is not subscribed to %s', request.user, id)
        return Http404("Subscription not Found")

    logger.debug('%s unsubscribing from %s', request.user, feed.name)

    # remove the feed from all of the users folders
    for folder in request.user.source_folders.all():
        folder.feeds.remove(feed)

    feed.subscribers.remove(request.user)

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

    # get the text to search for search
    search_text = form.cleaned_data['search_text']

    # if the search text is empty, return all subbed feeds
    if not search_text:
        return feeds_search_blank(request)

    # if the search text is a valiid url
    parsed_url = urlparse(search_text)
    if parsed_url.scheme:
        # match the given url
        return feeds_search_url(request, parsed_url)

    # else search for title/name matches
    return feeds_search_text(request, search_text)


def feeds_search_blank(request: HttpResponse):
    """this is the searcch result for empty search box"""
    sources = Source.objects\
        .filter(subscribers = request.user)\
        .order_by('title')

    if not sources.count():
        return feeds_search_no_match(request)

    page = int(request.GET.get("page", 1))
    context = paginator_args(page, sources)

    return render(
        request,
        'subscriptions/search/paginated_feeds_list.html',
        context=context
    )


def feeds_search_no_match(request):
    """this is the search result for an empty list of matches"""
    return HttpResponse(render(request, 'subscriptions/search/search_no_match.html'))


def feeds_search_text(request: HttpResponse, search_text:str):
    """search the database for feeds matching the given text
    
    Returns a set of matches
    """
    # matches if search_text is in the name or title
    matched_sources = Source.objects\
        .filter(subscribers = request.user)\
        .filter(Q(title__icontains = search_text) | Q(name__icontains = search_text))\
        .order_by('title')

    if matched_sources.count():
        page = int(request.GET.get("page", 1))
        context = paginator_args(page, matched_sources)

        return render(
            request,
            'subscriptions/search/paginated_feeds_list.html',
            context=context
        )

    return feeds_search_no_match(request)


def feeds_search_url(request: HttpResponse, search_url:ParseResult):
    """search the database for feeds matching the given text
    
    Returns a set of matches
    """
    # valid links matching the feed or site url
    rss_url = get_rss_url(search_url)
    try:
        feed = Source.objects.get(feed_url = rss_url)
    except Source.DoesNotExist:
        return new_feed_search(request, rss_url)

    logger.debug('feed found: %s', feed)

    # check if the user is subscribed
    if not feed.subscribers.filter(id=request.user.id).exists():
        return render(
            request,
            'subscriptions/search/search_item_not_subed.html',
            context={'feed':feed}
        )

    return render(
            request,
            'subscriptions/search/search_item_subed.html',
            context={'feed':feed}
        )



def new_feed_search(request: HttpResponse, rss_url:str):
    """create a new feed, return a search result"""
    new_source = Source(feed_url=rss_url)
    new_feed(new_source)

    if new_source.status_code >= 400: # the source will not have been created if there was an error
        return render(
            request,
            'subscriptions/search/search_item_error.html',
            context={'feed':new_source},
        )

    return render(
        request,
        'subscriptions/search/search_item_not_subed.html',
        context={'feed':new_source},
    )
