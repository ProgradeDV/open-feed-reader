"""contains the urls for open feed reader"""
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('',                                   views.all_posts,           name='all_posts'),
    path('post/<int:post_id>/',                views.post,                name='post'),
    path('sources/',                           views.all_sources,         name='my_sources'),
    path('sources/new/',                       views.new_source,          name='new_source'),
    path('sources/<int:source_id>/',           views.source,              name='source'),
    path('sources/<int:source_id>/edit/',      views.edit_source,         name='edit_source'),
    path('sources/<int:source_id>/delete/',    views.delete_source,       name='delete_source'),
    path('subscriptions/',                     views.subscriptions,    name='new_subscription'),
    path('subscriptions/new/',                 views.new_subscription,    name='new_subscription'),
    path('subscriptions/<int:sub_id>/delete/', views.delete_subscription, name='delete_subscription'),
]
