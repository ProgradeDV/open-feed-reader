"""site_base.views"""
from logging import getLogger
from urllib.parse import  urlparse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse
from django.http import Http404
from django.db.models import Q
from site_base.forms import SearchForm
from site_base.views import paginator_args
from feeds.models import Entry, Source
from feed_management.views import new_feed_form
from .models import SourceSubcription

logger = getLogger('feed_subscriptions/views.py')


ITEMS_PER_PAGE = 20


@login_required
def all_subs(request: HttpResponse):
    """view for the page of all known feeds"""

    return render(
        request,
        'subscriptions/all_subs_page.html',
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
        'feeds_folders/folder_page.html',
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
    return render(request, 'subscriptions/unsubscribe.html', context={'id':id})



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
    return render(request, 'subscriptions/subscribe.html', context={'id':id})



@login_required
def all_subs_search(request: HttpResponse):
    """view for the responst to the htmx request for searching for a feed"""
    if request.method != "POST":
        return HttpResponse(status=405) # Method Not Allowed

    form = SearchForm(request.POST)
    # check whether it's valid:
    if not form.is_valid():
        return HttpResponse(content='Invalid Form')

    search_text = form.cleaned_data['search_text']

    # if the url is valid
    if (parsed_url := urlparse(search_text)).scheme:
        # if a feed of that url exists, return just that feed
        try:
            feed = Source.objects.get(feed_url=search_text)

        except Source.DoesNotExist:
            # mif it does not exist, return the new feed form
            return new_feed_form(request, parsed_url)

        subed_feeds = Source.objects.filter(subscriptions__user = request.user)
        return render(
            request,
            'feeds/feeds_list_item.html',
            context={
                'feed': feed,
                'is_subed': (feed in subed_feeds),
            }
        )
    # search for feeds for ones matching the given text
    return feeds_search_result(request, search_text)


def feeds_search_result(request: HttpResponse, search_text:str):
    """search the database for feeds matching the given text and return the http response"""
    # if no search, return all feeds
    if not search_text:
        feeds = Source.objects.filter(subscriptions__user = request.user).order_by('title')

    else:
        # matches if search_text is in the name or title
        feeds = Source.objects.filter(subscriptions__user = request.user).filter(Q(feed_url__icontains = search_text) | Q(name__icontains = search_text)).order_by('title')

    page = int(request.GET.get("page", 1))
    subed_feeds = Source.objects.filter(subscriptions__user = request.user)

    context = paginator_args(page, feeds)
    context['subed_feeds'] = subed_feeds

    return render(
        request,
        'feeds/paginated_feeds_list.html',
        context=context
    )
