"""views for managing feed sources"""
from urllib.parse import urlencode
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from site_base.views import new_model_form_view, edit_model_form_view, delete_model_form_view
from feeds.models import Source
from feeds.fetch import init_feed
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
        'feed_management/feed_gen_form.html',
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
