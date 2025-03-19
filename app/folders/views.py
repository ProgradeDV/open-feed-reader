from logging import getLogger
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, HttpResponse

from .models import SourcesFolder


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

    return render(
        request,
        'folders/edit_folder.html',
        context={
            "folder":folder
            },
        )
