from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.template import loader
from .models import  BeachTeam, BeachTournament, Event, Player, BeachRound, BeachMatch
from django.db.models import Q
from django.http import HttpResponse
from django.utils.timezone import make_aware
from datetime import datetime, timedelta
# Author: Simon Löschke
# models

# Create your views here.

def index(request):
    '''Diese Funktion gibt die Startseite zurück: Hier werden die Events angezeigt, die in den nächsten 5 Jahren stattfinden'''
    # Aktuelles Datum und Datum für 5 Jahre zurück und 7 Monate voraus berechnen
    today = make_aware(datetime.today())
    one_year_ago = today - timedelta(days=1 * 365)
    seven_months_later = today + timedelta(days=7 * 30)  # Ca. 7 Monate

    # Turniere filtern, die zwischen 5 Jahren zurück und 7 Monaten voraus starten
    events = Event.objects.filter(start_date__range=(one_year_ago, seven_months_later)).order_by('-start_date').distinct()

    context = {
        'events': events,
    }
    return render(request, 'index.html', context)

def tournament(request):
    '''Diese Funktion gibt die Turnierseite zurück: Hier werden alle Turniere angezeigt'''
    event_id = request.GET.get('event_id')
    selected_gender = request.GET.get('gender')
    
    tournaments = BeachTournament.objects.all()

    if event_id:
        tournaments = tournaments.filter(event__id=event_id)
    if selected_gender:
        tournaments = tournaments.filter(gender=selected_gender)

    events = Event.objects.all()
    genders = BeachTournament.objects.values_list('gender', flat=True).distinct()

    return render(request, 'tournament.html', {'tournaments': tournaments, 'events': events, 'genders': genders})

def player(request):
    '''Diese Funktion gibt die Spielerseite zurück: Hier werden alle Spieler angezeigt'''
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
    '''Diese Funktion gibt die Teamseite zurück: Hier werden alle Teams angezeigt'''
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



