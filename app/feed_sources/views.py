from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from feeds.models import Source

# Create your views here.

@login_required
def source_types(request: HttpResponse):
    """view for a single post"""
    return render(request,
        'feed_sources/source_types.html',
        context={
            'title':'Source Types'
            },
        )
