from logging import getLogger
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.http import Http404
from feeds.models import Source, Entry
from site_base.views import paginator_args
from django.contrib import messages

from .models import FeedsFolder

logger=getLogger('Feeds Folders')

@login_required
def folder_page(request: HttpResponse, folder_id: int):
    """view the posts in a folder"""
    folder = FeedsFolder.objects.get(id=folder_id)

    # can't view folders that are not yours
    if folder.user != request.user:
        raise Http404("Folder Not Found")

    if folder.feeds.count() == 0:
        return HttpResponseRedirect(reverse('edit_folder', kwargs={'folder_id':folder_id}))

    entries = Entry.objects.filter(source__folders = folder).order_by('-created')
    page = int(request.GET.get("page", 1))
    context = paginator_args(page, entries)
    context['folder'] = folder
    context["title"] = f"Open Feed Reader: {folder.name}"
    context["navbar_title"] = folder.name

    return render(
        request,
        'folders/folder_page.html',
        context=context,
        )


@login_required
def create_folder(request: HttpResponse):
    """return the html for a new folder form"""
    if request.method == "GET":
        return render(request, 'folders/menu/create_folder_form.html')

    if request.method == "POST":
        new_folder = FeedsFolder(name=request.POST.get('folder_name'), user=request.user)
        new_folder.save()
        return render(request, 'folders/menu/created_folder.html', context={'lifolder':new_folder})

    return None


@login_required
def edit_folder_page(request: HttpResponse, folder_id:int):
    """poge to edit the attributes of and content of a foldder"""
    folder = FeedsFolder.objects.get(id=folder_id)

    # can't edit folders that are not yours
    if folder.user != request.user:
        raise Http404("Folder Not Found")

    subed_feeds = Source.objects.filter(subscribers = request.user).order_by('name')
    ordered_feeds = sorted(subed_feeds, key=lambda f: (f not in folder.feeds.all()))

    return render(
        request,
        'folders/edit/edit_folder.html',
        context={
            "folder":folder,
            "all_feeds":ordered_feeds,
            "title":f"Open Feed Reader: {folder.name}",
            "navbar_title":f"Edit Folder: {folder.name}",
            },
        )


@login_required
def add_feed_to_folder(request: HttpResponse, folder_id:int, feed_id:int):
    """add a feed to a folder"""
    # reject non post requests
    if request.method != "POST":
        return None

    feed = Source.objects.get(id=feed_id)
    folder = FeedsFolder.objects.get(id=folder_id)

    # can't edit folders that are not yours
    if folder.user != request.user:
        raise Http404("Folder Not Found")

    folder.feeds.add(feed)
    folder.save()

    # return an unsubscribe button
    return render(request, 'folders/edit/remove_from_folder_btn.html', context={'folder':folder, 'feed':feed})



@login_required
def edit_folder_name(request: HttpResponse, folder_id:int):
    """add a feed to a folder"""
    # reject non post requests
    if request.method != "POST":
        return None

    folder = FeedsFolder.objects.get(id=folder_id)

    # can't edit folders that are not yours
    if folder.user != request.user:
        raise Http404("Folder Not Found")

    folder.name = request.POST.get('folder_name')
    folder.save()

    # return a no change
    return HttpResponse(status=204)


@login_required
def remove_feed_from_folder(request: HttpResponse, folder_id:int, feed_id:int):
    """remove a feed from a folder"""
    # reject non post requests
    if request.method != "POST":
        return None

    feed = Source.objects.get(id=feed_id)
    folder = FeedsFolder.objects.get(id=folder_id)

    # can't edit folders that are not yours
    if folder.user != request.user:
        raise Http404("Folder Not Found")

    folder.feeds.remove(feed)
    folder.save()

    # return an unsubscribe button
    return render(request, 'folders/edit/add_to_folder_btn.html', context={'folder':folder, 'feed':feed})


@login_required
def delete_folder(request: HttpResponse, folder_id:int):
    """delete a folder"""
    folder = FeedsFolder.objects.get(id=folder_id)

    # can't edit folders that are not yours
    if folder.user != request.user:
        raise Http404("Folder Not Found")

    folder.delete()
    messages.success(request, f"{folder} Deleted")

    # redirect for htmx
    response = HttpResponse(content='')
    response.headers['HX-Redirect'] = reverse('all_subed_feed')
    return response
