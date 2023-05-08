"""site_base.views"""
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
from feeds.models import Post, Source
from feeds_extensions.models import SourceSubcription
from .forms import NewSubscriptionForm


@login_required
def all_posts(request: HttpResponse):
    """all feeds"""
    posts = Post.objects.filter(source__subscriptions__user = request.user)
    return render(request, 'site_base/posts_list.html', context={'posts':posts})


@login_required
def post(request: HttpResponse, post_id: int):
    """view for a single post"""
    post = Post.objects.get(id=post_id)
    return render(request, 'posts/post.html', context={'post':post})


@login_required
def all_sources(request: HttpResponse):
    """view for a list of posts"""
    sources = Source.objects.all()
    return render(request, 'sources/sources_list.html', context={'sources':sources})


@permission_required('feeds.add_source')
def new_source(request: HttpResponse):
    """create a new source"""
    return HttpResponseRedirect(reverse('all_posts'))


@permission_required('feeds.change_source')
def edit_source(request: HttpResponse, source_id: int):
    """edit a source"""
    return HttpResponseRedirect(reverse('all_posts'))


@permission_required('feeds.delete_source')
def delete_source(request: HttpResponse, source_id: int):
    """delete a source"""
    return HttpResponseRedirect(reverse('all_posts'))


@login_required
def source(request: HttpResponse, source_id: int):
    """view for a list of posts"""
    source = Source.objects.get(id=source_id)
    return render(request, 'sources/source.html', context={'source':source, 'posts':source.posts})


@login_required
def subscriptions(request: HttpResponse):
    """view a list of your subscriptions"""
    sources = Source.objects.filter(subscriptions__user = request.user)
    return render(request, 'sources/sources_list.html', context={'sources':sources})


@login_required
def new_subscription(request: HttpResponse):
    """view for subscribing to a source"""

    if request.method == "POST":
        form = NewSubscriptionForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # get the source object with the given feel url
            try:
                source = Source.objects.get(feed_url = form.cleaned_data["feed_url"])
            except Source.DoesNotExist:
                source = None

            # if a source with the given feed does not exist, return an error
            if source is None:
                form.add_error('feed_url', 'Unknown URL')
                return render(request, "sources/new_sub_form.html", {"form": form})

            # check if you are already subscribed to that url
            try:
                sub = SourceSubcription.objects.get(source = source)
            except SourceSubcription.DoesNotExist:
                sub = None

            if sub is None:
                # add a subscription
                sub = SourceSubcription(user = request.user, source = source)
                sub.save()
                return HttpResponseRedirect(reverse('my_sources'))

            form.add_error('feed_url', f'You are already subscribed to {form.cleaned_data["feed_url"]}')
            return render(request, "sources/new_sub_form.html", {"form": form})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NewSubscriptionForm()

    return render(request, "sources/new_sub_form.html", {"form": form})


@permission_required('feeds_extensions.delete_sourcesubscriptions')
def delete_subscription(request: HttpResponse, sub_id: int):
    """remove a subscription from a user"""
    return HttpResponseRedirect(reverse('all_posts'))
