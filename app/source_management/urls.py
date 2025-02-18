"""contains the urls for open feed reader"""
from django.urls import path
from . import views

urlpatterns = [
    path('gen/',             views.source_types,  name='gen_source'),
    path('new/',             views.new_source,    name='new_source'),
    path('<int:id>/edit/',   views.edit_source,   name='edit_source'),
    path('<int:id>/delete/', views.delete_source, name='delete_source'),
]
