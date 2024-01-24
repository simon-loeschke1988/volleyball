from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('player/', views.player, name='player'),
    path('teams/', views.teams, name='teams'),
    path('tournaments', views.tournament, name='tournament'),
    path('beach_matches/', views.beach_matches, name='beach_matches'),
]
