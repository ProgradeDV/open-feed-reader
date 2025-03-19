"""contains the urls for open feed reader"""
from django.urls import path
from . import views

urlpatterns = [
    path('new/',                          views.create_folder,           name='create_folder'),
    path('<int:id>/',                     views.folder_page,             name='folder_page'),
    path('<int:id>/edit/',                views.edit_folder,             name='edit_folder'),
    path('<int:id>/add/<int:feed_id>',    views.remove_feed_from_folder, name='remove_feed_from_folder'),
    path('<int:id>/remove/<int:feed_id>', views.add_feed_to_folder,      name='add_feed_to_folder'),
]
