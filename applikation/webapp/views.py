from django.core.paginator import Paginator
from django.shortcuts import render
from django.template import loader
from .models import Player
from django.db.models import Q


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
    query_name = request.GET.get('name','')
    query_fedcode = request.GET.get('fedcode','')
    
    fed = Player.objects.values_list('federation_code', flat=True).distinct()
    spieler_liste = Player.objects.all()
    if query_name:
     spieler_liste = spieler_liste.filter(
                Q(first_name__icontains=query_name) | 
                Q(last_name__icontains=query_name))
    elif query_fedcode:
        spieler_liste = Player.objects.filter(federation_code__icontains=query_fedcode)
   # else:
    
   
    paginator = Paginator(spieler_liste, 100)  # 10 Spieler pro Seite

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context= {
        'page_obj': page_obj,
        'fed': fed,
        'query_name': query_name,
        'query_fedcode': query_fedcode,
        }

    return render(request, 'player.html', context)
