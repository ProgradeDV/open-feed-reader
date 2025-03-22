"""contains the urls for open feed reader"""
from django.urls import path
from . import views

urlpatterns = [
    path('gen/',             views.generate_new_feed,  name='gen_feed'),
    path('new/',             views.new_feed,           name='new_feed'),
    path('<int:id>',         views.feed_page,           name='one_feed'),
    path('<int:id>/edit/',   views.edit_feed,          name='edit_feed'),
    path('<int:id>/delete/', views.delete_feed,        name='delete_feed'),
    path('all/',             views.all_feeds,          name='all_feeds'),
    path('feeds/search/',    views.all_feeds_search,   name='feeds_search'),
]
