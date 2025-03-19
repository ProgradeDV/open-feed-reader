"""contains the urls for open feed reader"""
from django.urls import path
from . import views

urlpatterns = [
    path('new/',           views.create_folder, name='create_folder'),
    path('<int:id>/',      views.folder_page,   name='folder_page'),
    path('<int:id>/edit/', views.edit_folder,   name='edit_folder'),
]
