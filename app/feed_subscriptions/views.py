"""site_base.views"""
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.urls import reverse

from feeds.models import Entry, Source
from site_base.views import new_model_form_view, edit_model_form_view, delete_model_form_view
from site_base.forms import SearchForm

from .models import SourceSubcription
from .forms import EditSourceForm


ITEMS_PER_PAGE = 10


@login_required
def all_posts(request: HttpResponse):
    """all posts from the users subscribed feeds"""
    posts = Entry.objects.filter(source__subscriptions__user = request.user).order_by('-created')

    context = paginator_args(request, posts)
    context['title'] = 'Open Feed Reader - Posts'

    return render(
        request,
        'posts/posts_list.html',
        context=context,
        )



@login_required
def one_post(request: HttpResponse, post_id: int):
    """view for a single post"""
    post = Entry.objects.get(id=post_id)
    return render(request,
        'posts/post.html',
        context={
            'post':post,
            'title':f'{post.title}'
            },
        )



@login_required
def all_sources(request: HttpResponse):
    """view for a list of posts"""

    if request.method == "POST":
        form = SearchForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # get the source object with the given feel url
            sources = Source.objects.filter(Q(feed_url__icontains = form.cleaned_data['search_text']) | Q(name__icontains = form.cleaned_data['search_text']))
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
            'title':'Open Feed Reader - Sources',
            },
        )



@permission_required('feeds.add_source')
def new_source(request: HttpResponse):
    """create a new source"""
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
    except SourceSubcription.DoesNotExist:
        return HttpResponseRedirect(reverse('all_sources'))

    return delete_model_form_view(request, source, 'all_sources')



@login_required
def one_source(request: HttpResponse, id: int):
    """view for a list of posts"""
    source = Source.objects.get(id=id)
    posts = Entry.objects.filter(source = source).order_by('-created')
    is_subed = SourceSubcription.objects.filter(user = request.user).filter(source = source).exists()

    context = paginator_args(request, posts)
    context['source'] = source
    context['title'] = source.display_name
    context['is_subed'] = is_subed

    return render(
        request,
        'sources/source.html',
        context=context,
        )



@login_required
def subscribe_source(request: HttpResponse, id: int):
    """subscribe to the source with the given id"""
    try:
        source = Source.objects.get(id = id)
    except Source.DoesNotExist:
        return redirect(request.META['HTTP_REFERER'])

    # check if you are already subscribed to that source
    try:
        sub = SourceSubcription.objects.get(source = source)
    except SourceSubcription.DoesNotExist:
        sub = None

    if sub is None:
        # add a subscription
        sub = SourceSubcription(user = request.user, source = source)
        sub.save()

    return redirect(request.META['HTTP_REFERER'])



@login_required
def unsubscribe_source(request: HttpResponse, id: int):
    """remove a subscription from a user"""
    try:
        sub = SourceSubcription.objects.filter(user = request.user).get(source = id)
    except SourceSubcription.DoesNotExist:
        return HttpResponseRedirect(reverse('subscriptions'))

    if request.method == "POST":
        sub.delete()
        return HttpResponseRedirect(reverse('subscriptions'))

    return render(request, "subscriptions/unsubscribe.html", {"sub": sub})



@login_required
def subscriptions(request: HttpResponse):
    """view a list of your subscriptions"""
    subs = SourceSubcription.objects.filter(user = request.user).order_by('source__name')

    if request.method == "POST":
        form = SearchForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # get the source object with the given feel url
            subs = subs.filter(Q(source__feed_url__icontains = form.cleaned_data['search_text']) | Q(source__name__icontains = form.cleaned_data['search_text']))
    else:
        form = SearchForm()

    return render(
        request,
        'subscriptions/subscriptions_list.html',
        context={
            'subscriptions':subs,
            'form':form,
            'title':'Open Feed Reader - Subscriptions',
            },
        )


def paginator_args(request, items) -> dict:
    """
    Calculate the paginator context for use with the paginator template
    """
    paginator = Paginator(items, ITEMS_PER_PAGE)

    page_number = max(min(int(request.GET.get("page", 1)), paginator.num_pages), 1)
    page_obj = paginator.get_page(page_number)

    page_range = range(max(1, page_number - 3), min(paginator.num_pages+1, page_number + 4))

    return {
        'page_obj':page_obj,
        'page_range':page_range,
        'page_number':page_number,
        'page_num_pages':paginator.num_pages,
    }
