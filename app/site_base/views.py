"""site_base.views"""
from django.db.models import Model
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.forms import ModelForm
from django.urls import reverse
from django.db.models.query import QuerySet
from django.core.paginator import Paginator

ITEMS_PER_PAGE = 20


def new_model_form_view(request: HttpResponse, form_class: ModelForm, success_url: str,
                        title: str = None, initial_model: Model = None) -> HttpResponse:
    """
    generic view to create a new model

    ### Parameters
    - request: the HttpResponse that requested this view
    - form: the model for that will be rendered
    - success_url: where to go on succsesfull creation
    - title: optional, title string, defaults to "New {model class}"

    ### Returns
    - HttpResponse, the rendered response
    """
    if request.method == "POST":
        form = form_class(request.POST)

        # check whether it's valid:
        if form.is_valid():
            new_model = form.save()
            return HttpResponseRedirect(reverse(success_url, kwargs={'id': new_model.id}))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = form_class(instance=initial_model)

    if title is None:
        title = f"Create New: {form_class.Meta.model}"

    return render(
        request,
        "site_base/edit_form.html",
        context={
            "form": form,
            "title":title,
            "post_url": request.path
            },
        )



def edit_model_form_view(request: HttpResponse, model: Model, form_class: ModelForm, success_url: str,
                         title: str = None, delete_url: str = None) -> HttpResponse:
    """
    generic page to edit a model
    
    ### Parameters
    - request: the HttpResponse that requested this view
    - model: the model to edit
    - form_cass: the form class that will be rendered
    - success_url: where to go on succsesfull creation
    - title: optional, title string, defaults to "Edit {model}"
    - delete_url: optional, the form will add a delete button if present

    ### Returns
    - HttpResponse, the rendered response
    """

    if request.method == "POST":
        form = form_class(request.POST, instance = model)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(success_url, kwargs={'id':model.id}))

    else:
        form = form_class(instance=model)

    if title is None:
        title = f'Edit: {model}'

    if delete_url is not None:
        delete_url = reverse(delete_url, kwargs={'id':model.id})

    return render(
        request,
        "site_base/edit_form.html",
        context={
            "form": form,
            "title":title,
            "success_url": success_url,
            "delete_url": delete_url,
            },
        )



def delete_model_form_view(request: HttpResponse, model: Model, success_url: str, title: str = None) -> HttpResponse:
    """
    generic view to delete a model
    
    ### Parameters
    - request: HttpResponse of the page to render
    - model: the model instance to delete
    - success_url: string url to redirecto to on successfull deletion
    - title: optional, string page title, defaults to "Delete {model}"

    ### Returns
    - HttpResponse, the rendered response
    """

    if title is None:
        title = f"Delete {model}"

    if request.method == "POST":
        model.delete()
        return HttpResponseRedirect(reverse(success_url))

    return render(
        request,
        "site_base/delete_form.html",
        context={
            "model": model,
            "title": title,
            "post_url": request.path
            },
        )


def paginator_args(page_index:int, items:QuerySet, items_per_page:int=ITEMS_PER_PAGE) -> dict:
    """
    Calculate the paginator context for use with the paginator template

    Parameters:
    - request: the http response object for the view
    - items: a django QuerySet for all of the items to be paged
    - items_per_page: integer number of items to put on each page
    """
    paginator = Paginator(items, items_per_page)

    page_number = max(min(page_index, paginator.num_pages), 1)
    page_obj = paginator.get_page(page_number)

    page_range = range(max(1, page_number - 3), min(paginator.num_pages+1, page_number + 4))

    return {
        'page_obj':page_obj,
        'page_range':page_range,
        'page_number':page_number,
        'page_num_pages':paginator.num_pages,
    }
