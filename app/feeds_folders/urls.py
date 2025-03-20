"""contains the urls for open feed reader"""
from django.urls import path
from . import views

urlpatterns = [
    path('new/',                                 views.create_folder,           name='create_folder'),
    path('<int:folder_id>/',                     views.folder_page,             name='folder_page'),
    path('<int:folder_id>/edit/',                views.edit_folder_page,        name='edit_folder'),
    path('<int:folder_id>/edit_name/',           views.edit_folder_name,        name='edit_folder_name'),
    path('<int:folder_id>/add/<int:feed_id>',    views.remove_feed_from_folder, name='remove_feed_from_folder'),
    path('<int:folder_id>/remove/<int:feed_id>', views.add_feed_to_folder,      name='add_feed_to_folder'),
    path('<int:folder_id>/delete',               views.delete_folder,           name='delete_folder'),
]
