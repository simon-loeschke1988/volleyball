from django.core.management.base import BaseCommand
from xml.etree import ElementTree
import requests
from datetime import datetime

from webapp.models import Event, BeachMatch, Player, BeachRound, BeachTeam, BeachTournament

class Command(BaseCommand):
    help = "Import data from XML API responses"

    def handle(self, *args, **kwargs):
        self.import_events()
        self.import_beach_matches()
        self.import_players()
        self.import_beach_rounds()
        self.import_beach_teams()
        self.import_beach_tournaments()

    def import_events(self):
        url = "https://www.fivb.org/vis2009/XmlRequest.asmx"
        payload = {"Request": "<Request Type='GetEventList' Fields='Code Name StartDate EndDate No'></Request>"}
        response = requests.get(url, params=payload)
        if response.status_code == 200:
            xml_response = ElementTree.fromstring(response.content)
            for event_xml in xml_response.findall('Event'):
                event_data = {key: event_xml.attrib.get(key) for key in ['Code', 'Name', 'StartDate', 'EndDate', 'No']}
                Event.objects.update_or_create(no=event_data['No'], defaults=event_data)

    def import_beach_matches(self):
        url = "https://www.fivb.org/vis2009/XmlRequest.asmx"
        payload = {"Request": "<Request Type='GetBeachMatchList' Fields='...'></Request>"}
        response = requests.get(url, params=payload)
        if response.status_code == 200:
            xml_response = ElementTree.fromstring(response.content)
            for match in xml_response.findall('BeachMatch'):
                match_data = {key: match.attrib.get(key) for key in match.attrib}
                BeachMatch.objects.create(**match_data)

    def import_players(self):
        Player.objects.all().delete()
        url = "https://www.fivb.org/vis2009/XmlRequest.asmx"
        payload = {"Request": "<Request Type='GetPlayerList' Fields='FederationCode FirstName LastName Gender ...'></Request>"}
        response = requests.get(url, params=payload)
        if response.status_code == 200:
            xml_response = ElementTree.fromstring(response.content)
            for player in xml_response.findall('Player'):
                player_data = {key: player.attrib.get(key) for key in player.attrib}
                Player.objects.create(**player_data)

    def import_beach_rounds(self):
        url = "https://www.fivb.org/vis2009/XmlRequest.asmx"
        payload = {"Request": "<Requests> <Request Type='GetBeachRoundList' Fields='Code Name Bracket ...'></Request></Requests>"}
        response = requests.get(url, params=payload)
        if response.status_code == 200:
            xml_response = ElementTree.fromstring(response.content)
            for round in xml_response.findall('.//BeachRound'):
                round_data = {key: round.attrib.get(key) for key in round.attrib}
                BeachRound.objects.get_or_create(**round_data)

    def import_beach_teams(self):
        url = "https://www.fivb.org/vis2009/XmlRequest.asmx"
        payload = {"Request": "<Request Type='GetBeachTeamList' Fields='NoPlayer1 NoPlayer2 Name ...'></Request>"}
        response = requests.get(url, params=payload)
        if response.status_code == 200:
            xml_response = ElementTree.fromstring(response.content)
            for team in xml_response.findall('BeachTeam'):
                team_data = {key: team.attrib.get(key) for key in team.attrib}
                BeachTeam.objects.update_or_create(**team_data)

    def import_beach_tournaments(self):
        url = "https://www.fivb.org/vis2009/XmlRequest.asmx"
        payload = {"Request": "<Request Type='GetBeachTournamentList' Fields='Code Name StartDateMainDraw EndDate ...'></Request>"}
        response = requests.get(url, params=payload)
        if response.status_code == 200:
            xml_response = ElementTree.fromstring(response.content)
            for tournament in xml_response.findall('BeachTournament'):
                tournament_data = {key: tournament.attrib.get(key) for key in tournament.attrib}
                BeachTournament.objects.update_or_create(**tournament_data)
