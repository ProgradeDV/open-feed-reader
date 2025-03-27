"""contains the urls for open feed reader"""
from django.urls import path
from . import views

urlpatterns = [
    path('',                            views.user_feed,          name='all_entries'),
    path('feeds/<int:id>/subscribe/',   views.subscribe_feed,     name='subscribe_feed'),
    path('feeds/<int:id>/unsubscribe/', views.unsubscribe_feed,   name='unsubscribe_feed'),
]
