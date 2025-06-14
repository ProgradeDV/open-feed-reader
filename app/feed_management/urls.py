"""contains the urls for open feed reader"""
from django.urls import path
from . import views

urlpatterns = [
    path('<int:id>',              views.feed_page,        name='one_feed'),
    path('<int:id>/edit/',        views.edit_feed,        name='edit_feed'),
    path('<int:id>/delete/',      views.delete_feed,      name='delete_feed'),
    path('new/',                  views.new_feed_submit,  name='new_feed'),
    path('entry/<int:entry_id>/', views.entry_page,       name='entry_page'),
]
