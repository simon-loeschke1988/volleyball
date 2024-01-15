from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.template import loader
from .models import Player, BeachTeam, BeachMatch, BeachTournament
from django.db.models import Q
from django.http import HttpResponse
# Author: Simon Löschke
# models

# Create your views here.



def index(request):
    # Filter-Parameter aus dem Request holen
    selected_tournament = request.GET.get('tournament')
    selected_team = request.GET.get('team')
    selected_court = request.GET.get('court')

    # Grunddaten holen
    tournaments = BeachTournament.objects.all()
    teams = BeachTeam.objects.all()
    matches = BeachMatch.objects.all()
    
    if selected_tournament:
        matches = matches.filter(no_tournament=selected_tournament)

    if selected_team:
        matches = matches.filter(team_a__name=selected_team) | matches.filter(team_b__name=selected_team)

    if selected_court:
        matches = matches.filter(court=selected_court)

    context = {
        'tournaments': tournaments,
        'teams': teams,
        'matches': matches,
        'selected_tournament': selected_tournament,
        'selected_team': selected_team,
        'selected_court': selected_court,
    }
    return render(request, 'index.html', context)

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


def teams(request):
    teams = BeachTeam.objects.all()

    # Suche implementieren
    query = request.GET.get('q')
    if query:
        teams = teams.filter(
            Q(name__icontains=query) | Q(player1__federation_code__icontains=query) | Q(player2__federation_code__icontains=query)
        )

    # Paginierung
    paginator = Paginator(teams, 10)  # 10 Teams pro Seite
    page = request.GET.get('page')

    try:
        teams = paginator.page(page)
    except PageNotAnInteger:
        teams = paginator.page(1)
    except EmptyPage:
        teams = paginator.page(paginator.num_pages)

    return render(request, 'teams.html', {'teams': teams, 'query': query})



