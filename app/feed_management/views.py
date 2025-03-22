"""views for managing feed sources"""
from urllib.parse import urlencode
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib import messages
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
from site_base.views import new_model_form_view, edit_model_form_view, delete_model_form_view, paginator_args
from site_base.forms import SearchForm
from feeds.models import Source, Entry
from feeds.fetch import init_feed
from feed_subscriptions.models import SourceSubcription
from .forms import EditFeedForm
from . import source_urls



@permission_required('feeds.add_source')
def generate_new_feed(request: HttpResponse):
    """the form for initializing a feed creation from a related link"""
    if request.method == "POST":

        feed_url = None
        site_url = None

        # convert the given url to an rss url
        if request.POST.get('feed_url', ''):
            feed_url = request.POST.get('feed_url', '')

        elif site_url := request.POST.get('youtube_link', ''):
            feed_url = source_urls.convert_youtube_channel(site_url)

        elif site_url := request.POST.get('blusky_link', ''):
            feed_url = source_urls.convert_bluesky_account(site_url)

        elif site_url := request.POST.get('subreddit_link', ''):
            feed_url = source_urls.convert_subreddit(site_url)

        if feed_url:
            # redirect to the new feed form
            return HttpResponseRedirect(reverse('new_feed') + '?' + urlencode({'feed_url':feed_url, 'site_url':site_url}))

    return render(request,
        'feeds/feed_gen_form.html',
        context={
            'title':'Feed Types'
            },
        )



@permission_required('feeds.add_source')
def new_feed(request: HttpResponse):
    """create a new feed"""
    if feed_url := request.GET.get('feed_url', ''):
        site_url = request.GET.get('site_url', '')
        feed = Source(feed_url=feed_url, site_url=site_url)
        init_feed(feed)

        if feed.status_code > 400:
            messages.add_message(request, messages.ERROR, f"({feed.status_code}) {feed.last_result}")

        return new_model_form_view(request, EditFeedForm, 'one_feed', initial_model=feed)
    return new_model_form_view(request, EditFeedForm, 'one_feed')



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
    """view for the responst to the htmx request for a filtered list of all feeds"""
    if request.method != "POST":
        return None

    form = SearchForm(request.POST)
    # check whether it's valid:
    if not form.is_valid():
        return None

    search_text = form.cleaned_data['search_text']
    page = int(request.GET.get("page", 1))

    if not search_text:
        feeds = Source.objects.all()

    else:
        feeds = Source.objects.filter(
            Q(feed_url__icontains = form.cleaned_data['search_text']) |
            Q(name__icontains = form.cleaned_data['search_text'])
            )

    subed_feeds = Source.objects.filter(subscriptions__user = request.user)
    context = paginator_args(page, feeds)
    context['subed_feeds'] = subed_feeds

    return render(
        request,
        'feeds/paginated_feeds_list.html',
        context=context
    )
