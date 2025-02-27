"""views for managing feed sources"""
from urllib.parse import urlencode
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from site_base.views import new_model_form_view, edit_model_form_view, delete_model_form_view
from feeds.models import Source
from feeds.fetch import init_feed
from .forms import EditSourceForm
from . import source_urls

# Create your views here.

@permission_required('feeds.add_source')
def generate_new_source(request: HttpResponse):
    """the form for initializing a source creation from a related link"""
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
            # redirect to the new source form
            return HttpResponseRedirect(reverse('new_source')+ '?' + urlencode({'feed_url':feed_url, 'site_url':site_url}))

    return render(request,
        'source_management/source_gen_form.html',
        context={
            'title':'Source Types'
            },
        )



@permission_required('feeds.add_source')
def new_source(request: HttpResponse):
    """create a new source"""
    if feed_url := request.GET.get('feed_url', ''):
        site_url = request.GET.get('site_url', '')
        source = Source(feed_url=feed_url, site_url=site_url)
        init_feed(source)

        if source.status_code > 400:
            messages.add_message(request, messages.ERROR, f"({source.status_code}) {source.last_result}")

        return new_model_form_view(request, EditSourceForm, 'one_source', initial_model=source)
    return new_model_form_view(request, EditSourceForm, 'one_source')



@permission_required('feeds.change_source')
def edit_source(request: HttpResponse, id: int):
    """Edit a source"""
    try:
        source = Source.objects.get(id = id)
    except Source.DoesNotExist:
        HttpResponseRedirect(reverse('all_sources'))

    return edit_model_form_view(request, source, EditSourceForm, 'one_source', delete_url='delete_source')



@permission_required('feeds.delete_source')
def delete_source(request: HttpResponse, id: int):
    """delete a source"""
    try:
        source = Source.objects.get(id = id)
    except Source.DoesNotExist:
        return HttpResponseRedirect(reverse('all_sources'))

    return delete_model_form_view(request, source, 'all_sources')
