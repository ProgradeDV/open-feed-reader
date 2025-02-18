from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from site_base.views import new_model_form_view, edit_model_form_view, delete_model_form_view
from django.urls import reverse
from feeds.models import Source
from .forms import EditSourceForm

# Create your views here.

@permission_required('feeds.add_source')
def source_types(request: HttpResponse):
    """view for a single post"""
    return render(request,
        'source_management/source_types.html',
        context={
            'title':'Source Types'
            },
        )



@permission_required('feeds.add_source')
def new_source(request: HttpResponse, initial_source:Source=None):
    """create a new source"""
    return new_model_form_view(request, EditSourceForm, 'one_source', initial_model=initial_source)



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
