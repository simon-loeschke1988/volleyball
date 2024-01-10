from django.shortcuts import render
from django.template import loader

from django.http import HttpResponse
# Author: Simon Löschke
# models
from .models import Player
# Create your views here.

def index(request):
    # index.html is located in applikation/webapp/templates/index.html, but we don't need to specify the full path // Simon Löschke
    template = loader.get_template('index.html')
    return HttpResponse(template.render({}, request))

def player(request):
    player = Player.objects.all().values()
    template = loader.get_template('player.html')
    context = {
        'players': player,
    }
    return HttpResponse(template.render(context, request))

# zu testen 


