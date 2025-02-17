"""contains the urls for open feed reader"""
from django.urls import path
from . import views

urlpatterns = [
    path('gen', views.source_types, name='source_types'),
]
