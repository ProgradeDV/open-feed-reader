"""contains the urls for open feed reader"""
from django.urls import path
from . import views

urlpatterns = [
    path('',                                views.all_posts,           name='all_posts'),
    path('post/<int:post_id>/',             views.one_post,            name='one_post'),
    path('feeds/',                        views.all_sources,         name='all_sources'),
    path('feeds/<int:id>/',               views.one_source,          name='one_source'),
    path('feeds/<int:id>/subscribe/',     views.subscribe_source,    name='subscribe_source'),
    path('feeds/<int:id>/unsubscribe/',   views.unsubscribe_source,  name='unsubscribe_source'),
    path('subscriptions/',                  views.subscriptions,       name='subscriptions'),
]
