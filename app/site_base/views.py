"""site_base.views"""
from django.shortcuts import render, HttpResponse
from feeds.models import Post, Source
from django.contrib.auth.decorators import login_required


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
    return render(request, 'site_base/source_list.html', context={'sources':sources})


@login_required
def source(request: HttpResponse, source_id: int):
    """view for a list of posts"""
    source = Source.objects.get(id=source_id)
    return render(request, 'site_base/source.html', context={'source':source, 'posts':source.posts})
