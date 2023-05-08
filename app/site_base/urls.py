"""contains the urls for open feed reader"""
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.all_posts, name='all_posts'),
    path('post/<int:post_id>/', views.post, name='post'),
    path('sources/', views.all_sources, name='my_sources'),
    path('sources/<int:source_id>', views.source, name='source'),
]
