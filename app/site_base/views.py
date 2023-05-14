"""site_base.views"""
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from feeds.models import Post, Source
from feeds_extensions.models import SourceSubcription
from .forms import EditSourceForm, SourceSearchForm


@login_required
def all_posts(request: HttpResponse):
    """all feeds"""
    posts = Post.objects.filter(source__subscriptions__user = request.user).order_by('-created')
    return render(request, 'posts/posts_list.html', context={'posts':posts[0:10]})


@login_required
def post(request: HttpResponse, post_id: int):
    """view for a single post"""
    post = Post.objects.get(id=post_id)
    return render(request, 'posts/post.html', context={'post':post})


@login_required
def all_sources(request: HttpResponse):
    """view for a list of posts"""

    if request.method == "POST":
        form = SourceSearchForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # get the source object with the given feel url
            sources = Source.objects.filter(Q(feed_url__icontains = form.cleaned_data['search_text']) | Q(name__icontains = form.cleaned_data['search_text']))
        else:
            sources = []
    else:
        form = SourceSearchForm()
        sources = Source.objects.all()

    subed_sources = Source.objects.filter(subscriptions__user = request.user)
    return render(request, 'sources/sources_list.html', 
                  context={'form':form, 'sources':sources, 'subed_sources':subed_sources})


@permission_required('feeds.add_source')
def new_source(request: HttpResponse):
    """create a new source"""
    if request.method == "POST":
        form = EditSourceForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # make sure the feed isn't duplicated
            if Source.objects.get(feed_url = form.cleaned_data["feed_url"]).exists():
                form.add_error('feed_url', 'URL already exists in sources list')
                return render(request, "sources/new_source.html", {"form": form})

            source = Source(**form.cleaned_data)
            source.save()
            return HttpResponseRedirect(reverse('sources'))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = EditSourceForm()

    return render(request, "sources/new_source.html", {"form": form})


@permission_required('feeds.change_source')
def edit_source(request: HttpResponse, source_id: int):
    """edit a source"""
    try:
        source = Source.objects.get(id = source_id)
    except Source.DoesNotExist:
        HttpResponseRedirect(reverse('all_sources'))

    if request.method == "POST":
        form = EditSourceForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            source.name        = form.cleaned_data['name']
            source.site_url    = form.cleaned_data['site_url']
            source.feed_url    = form.cleaned_data['feed_url ']
            source.image_url   = form.cleaned_data['image_url']
            source.description = form.cleaned_data['description']
            source.interval    = form.cleaned_data['interval']

            source.save()
            return HttpResponseRedirect(reverse('all_sources'))

    else:
        form = EditSourceForm(initial={
            'name':source.name,
            'site_url':source.site_url,
            'feed_url':source.feed_url,
            'image_url':source.image_url,
            'description':source.description,
            'interval':source.interval,
            }
        )

    return render(request, "sources/edit_source.html", {"form": form})


@permission_required('feeds.delete_source')
def delete_source(request: HttpResponse, source_id: int):
    """delete a source"""
    try:
        source = Source.objects.get(id = source_id)
    except SourceSubcription.DoesNotExist:
        return HttpResponseRedirect(reverse('all_sources'))

    if request.method == "POST":
        source.delete()
        return HttpResponseRedirect(reverse('all_sources'))

    return render(request, "sources/delete_source.html", {"source": source})


@login_required
def source(request: HttpResponse, source_id: int):
    """view for a list of posts"""
    source = Source.objects.get(id=source_id)
    posts = Post.objects.filter(source = source).order_by('-created')
    is_subed = SourceSubcription.objects.filter(user = request.user).filter(source = source).exists()
    return render(request, 'sources/source.html', context={'source':source, 'posts':posts, 'is_subed':is_subed})


@login_required
def subscribe_source(request: HttpResponse, source_id: int):
    """subscribe to the source with the given id"""
    try:
        source = Source.objects.get(id = source_id)
    except Source.DoesNotExist:
        return HttpResponseRedirect(reverse('subscriptions'))

    # check if you are already subscribed to that source
    try:
        sub = SourceSubcription.objects.get(source = source)
    except SourceSubcription.DoesNotExist:
        sub = None

    if sub is None:
        # add a subscription
        sub = SourceSubcription(user = request.user, source = source)
        sub.save()

    return HttpResponseRedirect(reverse('subscriptions'))


@login_required
def unsubscribe_source(request: HttpResponse, source_id: int):
    """remove a subscription from a user"""
    try:
        sub = SourceSubcription.objects.filter(user = request.user).get(source = source_id)
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
    return render(request, 'subscriptions/subscriptions_list.html', context={'subscriptions':subs})
