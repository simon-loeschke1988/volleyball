from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('player/', views.player, name='player'),
    path('beach_teams/', views.beach_teams_list, name='beach_teams_list'),
]
