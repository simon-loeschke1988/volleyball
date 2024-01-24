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


def beach_matches(request):
    current_year = datetime.now().year
    last_year = current_year - 1

    start_date_last_year = datetime(last_year, 1, 1)
    end_date_this_year = datetime(current_year, 12, 31)

    # Filtern der Matches für das letzte und dieses Jahr
    matches = BeachMatch.objects.filter(LocalDate__range=(start_date_last_year, end_date_this_year)).order_by('-LocalDate')

    # Filtern basierend auf den Anfrageparametern
    federation_code = request.GET.get('federation_code')
    nationality = request.GET.get('nationality')
    event_no = request.GET.get('event_no')
    tournament_no = request.GET.get('tournament_no')
    team_name = request.GET.get('team_name')

    if federation_code:
        matches = matches.filter(Q(NoTeamA__federation_code=federation_code) | Q(NoTeamB__federation_code=federation_code))
    if nationality:
        matches = matches.filter(Q(NoTeamA__nationality=nationality) | Q(NoTeamB__nationality=nationality))
    if event_no:
        matches = matches.filter(NoEvent__no=event_no)
    if tournament_no:
        matches = matches.filter(NoTournament__no=tournament_no)
    if team_name:
        matches = matches.filter(Q(NoTeamA__name=team_name) | Q(NoTeamB__name=team_name))

    # Ermitteln der Team-IDs aus den gefilterten Matches
    team_ids = set()
    for match in matches:
        if match.NoTeamA:
            team_ids.add(match.NoTeamA.no)
        if match.NoTeamB:
            team_ids.add(match.NoTeamB.no)

    # Filtern der Teams basierend auf den ermittelten IDs
    teams = BeachTeam.objects.filter(no__in=team_ids)

    # Paginierung
    page = request.GET.get('page', 1)
    paginator = Paginator(matches, 20)
    try:
        matches_page = paginator.page(page)
    except PageNotAnInteger:
        matches_page = paginator.page(1)
    except EmptyPage:
        matches_page = paginator.page(paginator.num_pages)

    # Abrufen der weiteren notwendigen Daten
    federations = Player.objects.values_list('federation_code', flat=True).distinct()
    countries = Player.objects.values_list('nationality', flat=True).distinct()
    events = Event.objects.all()
    tournaments = BeachTournament.objects.all()

    return render(request, 'matches.html', {
        'matches': matches_page,
        'federations': federations,
        'countries': countries,
        'events': events,
        'tournaments': tournaments,
        'teams': teams
    })