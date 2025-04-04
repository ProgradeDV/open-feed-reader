"""views for managing feed sources"""
import logging
from urllib.parse import  urlparse, ParseResult
from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
from django.contrib import messages
from site_base.views import edit_model_form_view, delete_model_form_view, paginator_args
from site_base.forms import SearchForm
from feeds.models import Source, Entry
from feeds.fetch import init_feed, fetch_feed
from feed_subscriptions.models import SourceSubcription
from .forms import EditFeedForm
from . import source_urls

logger = logging.getLogger("feed_management")


@permission_required('feeds.change_source')
def edit_feed(request: HttpResponse, id: int):
    """Edit a feed"""
    try:
        feed = Source.objects.get(id = id)
    except Source.DoesNotExist:
        HttpResponseRedirect(reverse('all_feeds'))

    return edit_model_form_view(request, feed, EditFeedForm, 'one_feed', delete_url='delete_feed')



@permission_required('feeds.delete_source')
def delete_feed(request: HttpResponse, id: int):
    """delete a feed"""
    try:
        feed = Source.objects.get(id = id)
    except Source.DoesNotExist:
        return HttpResponseRedirect(reverse('all_feeds'))

    return delete_model_form_view(request, feed, 'all_feeds')



@login_required
def feed_page(request: HttpResponse, id: int):
    """the view for a single feed and it's entries"""
    feed = Source.objects.get(id=id)
    entries = Entry.objects.filter(source = feed).order_by('-created')
    is_subed = SourceSubcription.objects.filter(user = request.user).filter(source = feed).exists()

    page = int(request.GET.get("page", 1))
    context = paginator_args(page, entries)
    context['feed'] = feed
    context['is_subed'] = is_subed

    return render(
        request,
        'feeds/feed.html',
        context=context,
        )



@login_required
def all_feeds(request: HttpResponse):
    """view for the page of all known feeds"""

    return render(
        request,
        'feeds/all_feeds_page.html',
        context={
            'navbar_title':'All Feeds',
            },
        )



@login_required
def all_feeds_search(request: HttpResponse):
    """view for the responst to the htmx request for searching for a feed"""
    if request.method != "POST":
        return HttpResponse(status=405) # Method Not Allowed

    form = SearchForm(request.POST)
    # check whether it's valid:
    if not form.is_valid():
        return HttpResponse(content='')

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
        feeds = Source.objects.all()

    else:
        # matches if search_text is in the name or title
        feeds = Source.objects.filter(Q(feed_url__icontains = search_text) | Q(name__icontains = search_text))

    page = int(request.GET.get("page", 1))
    subed_feeds = Source.objects.filter(subscriptions__user = request.user)

    context = paginator_args(page, feeds)
    context['subed_feeds'] = subed_feeds

    return render(
        request,
        'feeds/paginated_feeds_list.html',
        context=context
    )


def new_feed_form(request: HttpResponse, parsed_url:ParseResult):
    """generate a form for a new feed"""
    # convert the given url to to the correct feed url
    actual_url = source_urls.get_rss_url(parsed_url)
    # create a new feed
    feed = Source(feed_url=actual_url, site_url=parsed_url.geturl())
    # update the feed atributes
    init_feed(feed)

    return render(
        request,
        'feeds/new_feed_form.html',
        context={
            'form': EditFeedForm(instance=feed),
        }
    )


@login_required
def new_feed_submit(request: HttpResponse):
    """this is the view for when a user hits submit on a new feed form"""
    if request.method != "POST":
        return HttpResponse(status=405) # Method Not Allowed

    form = EditFeedForm(request.POST)

    # if the form is valid, save the new feed and redirect the user to the feed page
    if form.is_valid():
        new_feed = form.save()
        fetch_feed(new_feed)

        response = HttpResponse(content='')
        response.headers['HX-Redirect'] = reverse('one_feed', kwargs={'id': new_feed.id})
        messages.success(request, f"{new_feed} Created")
        return response

    # return a rendered form html
    return render(
        request,
        'feeds/new_feed_form.html',
        context={
            'form': form,
        }
    )


@login_required
def entry_page(request: HttpResponse, entry_id: int):
    """view for a single entry"""
    entry = Entry.objects.get(id=entry_id)
    return render(request,
        'entries/entry.html',
        context={
            'entry':entry,
            },
        )
