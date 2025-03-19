"""contains the urls for open feed reader"""
from django.urls import path
from . import views

urlpatterns = [
    path('',                            views.user_feed,          name='all_entries'),
    path('entry/<int:entry_id>/',       views.one_entry,          name='one_entry'),
    path('feeds/',                      views.all_feeds,          name='all_feeds'),
    path('feeds/search/',               views.all_feeds_search,   name='feeds_search'),
    path('feeds/<int:id>/',             views.one_feed,           name='one_feed'),
    path('feeds/<int:id>/subscribe/',   views.subscribe_feed,     name='subscribe_feed'),
    path('feeds/<int:id>/unsubscribe/', views.unsubscribe_feed,   name='unsubscribe_feed'),
    path('subscriptions/',              views.user_subscriptions, name='subscriptions'),
    path('folder/new/',                 views.create_folder,      name='create_folder'),
    path('folder/<int:id>/',            views.folder_page,        name='folder_page'),
    path('folder/<int:id>/edit',        views.edit_folder,        name='edit_folder'),
]
