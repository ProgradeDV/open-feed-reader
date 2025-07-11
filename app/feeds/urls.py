"""contains the urls for open feed reader"""
from django.urls import path
from . import views

urlpatterns = [
    path('<int:feed_id>',           views.feed_page,         name='one_feed'),
    path('<int:feed_id>/content/',  views.feed_page_content, name='feed_page_content'),
    path('entry/<int:entry_id>/',   views.entry_page,        name='entry_page'),
]
