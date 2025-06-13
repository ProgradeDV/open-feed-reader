"""contains the urls for open feed reader"""
from django.urls import path
from . import views

urlpatterns = [
    path('',                            views.all_subed_feed,          name='all_subed_feed'),
    path('feeds/<int:id>/subscribe/',   views.subscribe_feed,          name='subscribe_feed'),
    path('feeds/<int:id>/unsubscribe/', views.unsubscribe_feed,        name='unsubscribe_feed'),
    path('subscriptions/',              views.edit_subscriptions_page, name='subscriptions'),
    path('search/',                     views.all_subs_search,         name='feeds_search'),
]
