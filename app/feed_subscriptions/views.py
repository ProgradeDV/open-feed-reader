"""site_base.views"""
from logging import getLogger
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.query import QuerySet
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.urls import reverse

from feeds.models import Entry, Source
from site_base.forms import SearchForm

from .models import SourceSubcription

logger = getLogger('feed_subscriptions/views.py')


ITEMS_PER_PAGE = 20


@login_required
def user_feed(request: HttpResponse):
    """all entries from the users subscribed feeds"""
    entries = Entry.objects.filter(source__subscriptions__user = request.user).order_by('-created')

    context = paginator_args(request, entries)
    context['navbar_title'] = 'My Feed'

    return render(
        request,
        'entries/entries_list.html',
        context=context,
        )



@login_required
def one_entry(request: HttpResponse, entry_id: int):
    """view for a single entry"""
    entry = Entry.objects.get(id=entry_id)
    return render(request,
        'entries/entry.html',
        context={
            'entry':entry,
            },
        )



@login_required
def all_sources(request: HttpResponse):
    """view for a list of entries"""

    if request.method == "POST":
        form = SearchForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # get the source object with the given feel url
            sources = Source.objects.filter(
                Q(feed_url__icontains = form.cleaned_data['search_text']) |
                Q(name__icontains = form.cleaned_data['search_text'])
                )
        else:
            sources = []
    else:
        form = SearchForm()
        sources = Source.objects.all()

    subed_sources = Source.objects.filter(subscriptions__user = request.user)
    return render(
        request,
        'sources/sources_list.html',
        context={
            'form':form,
            'sources':sources,
            'subed_sources':subed_sources,
            'navbar_title':'Feed Sources',
            },
        )



@login_required
def one_source(request: HttpResponse, id: int):
    """view for a list of entries"""
    source = Source.objects.get(id=id)
    entries = Entry.objects.filter(source = source).order_by('-created')
    is_subed = SourceSubcription.objects.filter(user = request.user).filter(source = source).exists()

    context = paginator_args(request, entries)
    context['source'] = source
    context['is_subed'] = is_subed

    return render(
        request,
        'sources/source.html',
        context=context,
        )



@login_required
def subscribe_source(request: HttpResponse, id: int):
    """subscribe to the source with the given id"""
    # reject non post requests
    if request.method != "POST":
        return None

    # reject subscriptions to sources that don't exist
    try:
        source = Source.objects.get(id = id)
    except Source.DoesNotExist:
        return None

    # check if you are already subscribed to that source
    try:
        sub = SourceSubcription.objects.filter(user = request.user).get(source = source)

    except SourceSubcription.DoesNotExist:
        # if the subscription doesn't exist, subscribe
        logger.debug('%s subscribing to %s', request.user, source.name)
        sub = SourceSubcription(user = request.user, source = source)
        sub.save()

    else:
        # if you're already subscribed
        logger.debug('%s is already subscribed to %s', request.user, source.name)

    # return an unsubscribe button
    return render(request, 'subscriptions/unsubscribe.html', context={'id':id})



@login_required
def unsubscribe_source(request: HttpResponse, id: int):
    """remove a subscription from a user"""
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



@login_required
def user_subscriptions(request: HttpResponse):
    """view a list of your subscriptions"""
    subs = SourceSubcription.objects.filter(user = request.user).order_by('source__name')

    if request.method == "POST":
        form = SearchForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # get the source object with the given feel url
            subs = subs.filter(
                Q(source__feed_url__icontains = form.cleaned_data['search_text']) |
                Q(source__name__icontains = form.cleaned_data['search_text'])
            )
    else:
        form = SearchForm()

    return render(
        request,
        'subscriptions/subscriptions_list.html',
        context={
            'subscriptions':subs,
            'form':form,
            'navbar_title':'Subscriptions',
            },
        )


def paginator_args(request:HttpResponse, items:QuerySet, items_per_page:int=ITEMS_PER_PAGE) -> dict:
    """
    Calculate the paginator context for use with the paginator template

    Parameters:
    - request: the http response object for the view
    - items: a django QuerySet for all of the items to be paged
    - items_per_page: integer number of items to put on each page
    """
    paginator = Paginator(items, items_per_page)

    page_number = max(min(int(request.GET.get("page", 1)), paginator.num_pages), 1)
    page_obj = paginator.get_page(page_number)

    page_range = range(max(1, page_number - 3), min(paginator.num_pages+1, page_number + 4))

    return {
        'page_obj':page_obj,
        'page_range':page_range,
        'page_number':page_number,
        'page_num_pages':paginator.num_pages,
    }
