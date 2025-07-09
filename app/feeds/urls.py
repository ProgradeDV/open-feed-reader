"""contains the urls for open feed reader"""
from django.urls import path
from . import views

urlpatterns = [
    path('<int:id>',              views.feed_page,        name='one_feed'),
    path('entry/<int:entry_id>/', views.entry_page,       name='entry_page'),
]
