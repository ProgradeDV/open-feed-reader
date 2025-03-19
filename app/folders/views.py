from logging import getLogger
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, HttpResponse
from feeds.models import Source

from .models import SourcesFolder

logger=getLogger('folders')

@login_required
def folder_page(request: HttpResponse, id: int):
    """view the posts in a folder"""
    try:
        folder = SourcesFolder.objects.get(id=id)
    except SourcesFolder.DoesNotExist:
        return None


    return render(
        request,
        'folders/folder_page.html',
        context={
            "folder":folder
            },
        )

@permission_required('feeds.add_folder')
def create_folder(request: HttpResponse):
    """return the html for a new folder form"""
    if request.method == "GET":
        return render(request, 'folders/create_folder_form.html')

    if request.method == "POST":
        new_folder = SourcesFolder(name=request.POST.get('folder_name'), user=request.user)
        new_folder.save()
        return render(request, 'folders/created_folder.html', context={'lifolder':new_folder})

    return None


def edit_folder(request: HttpResponse, id:int):
    """edit the sources in a folder"""
    try:
        folder = SourcesFolder.objects.get(id=id)
    except SourcesFolder.DoesNotExist:
        return None

    # all_feeds = Source.objects.all()
    subed_sources = Source.objects.filter(subscriptions__user = request.user).order_by('name')
    ordered_feeds = sorted(subed_sources, key=lambda f: (f not in folder.sources.all()))

    return render(
        request,
        'folders/edit_folder.html',
        context={
            "folder":folder,
            "all_feeds":ordered_feeds,
            },
        )


@login_required
def add_feed_to_folder(request: HttpResponse, id:int, feed_id:int):
    """add a feed to a folder"""
    # reject non post requests
    if request.method != "POST":
        return None

    # reject subscriptions to sources that don't exist
    try:
        feed = Source.objects.get(id = feed_id)
    except Source.DoesNotExist:
        return None

    folder = SourcesFolder.objects.get(id=id)
    folder.sources.add(feed)
    folder.save()

    # return an unsubscribe button
    return render(request, 'folders/feed_list_item.html', context={'folder':folder, 'feed':feed})


def remove_feed_from_folder(request: HttpResponse, id:int, feed_id:int):
    """remove a feed from a folder"""
    # reject non post requests
    if request.method != "POST":
        return None

    # reject subscriptions to sources that don't exist
    try:
        feed = Source.objects.get(id = feed_id)
    except Source.DoesNotExist:
        return None

    folder = SourcesFolder.objects.get(id=id)
    folder.sources.remove(feed)
    folder.save()

    # return an unsubscribe button
    return render(request, 'folders/feed_list_item.html', context={'folder':folder, 'feed':feed})
