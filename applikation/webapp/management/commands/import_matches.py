from django.core.management.base import BaseCommand
from xml.etree import ElementTree
import requests
import logging

from webapp.models import BeachMatch, BeachRound, BeachTeam, Player

# Konfigurieren Sie das Logging-Modul
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Handler für die Ausgabe der Log-Nachrichten in eine Datei
file_handler = logging.FileHandler('logs/matches_log.log')
file_handler.setLevel(logging.DEBUG)

# Format für die Log-Nachrichten
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Fügen Sie den Handler zum Logger hinzu
logger.addHandler(file_handler)

class Command(BaseCommand):
    help = "Import BeachMatches from XML API response"

    def handle(self, *args, **kwargs):
        url = "https://www.fivb.org/vis2009/XmlRequest.asmx"
        payload = {
            "Request": "<Request Type='GetBeachMatchList' Fields='NoInTournament LocalDate LocalTime NoTeamA NoTeamB Court MatchPointsA MatchPointsB PointsTeamASet1 PointsTeamBSet1 PointsTeamASet2 PointsTeamBSet2 PointsTeamASet3 PointsTeamBSet3 DurationSet1 DurationSet2 DurationSet3 NoRound NoTournament NoPlayerA1 NoPlayerA2 NoPlayerB1 NoPlayerB2'> </Request>"
        }

        response = requests.get(url, params=payload)
        if response.status_code != 200:
            logger.error(f"Failed to retrieve data with status code: {response.status_code}")
            return

        xml_response = ElementTree.fromstring(response.content)

        for match in xml_response.findall('BeachMatch'):
            # Die Attribute des Matches extrahieren
            attributes = {attr: match.attrib.get(attr) for attr in match.attrib}

            try:
                # Rest des Codes bleibt unverändert
                beach_round = BeachRound.objects.get(code=attributes['NoRound'])
                team_a = BeachTeam.objects.get(no=attributes['NoTeamA'])
                team_b = BeachTeam.objects.get(no=attributes['NoTeamB'])
                player_a1 = Player.objects.get(no=attributes['NoPlayerA1'])
                player_a2 = Player.objects.get(no=attributes['NoPlayerA2'])
                player_b1 = Player.objects.get(no=attributes['NoPlayerB1'])
                player_b2 = Player.objects.get(no=attributes['NoPlayerB2'])

                # Erstellen eines neuen BeachMatch-Objekts
                BeachMatch.objects.create(
                    **attributes,
                    team_a=team_a,
                    team_b=team_b,
                    no_round=beach_round,
                    no_player_a1=player_a1,
                    no_player_a2=player_a2,
                    no_player_b1=player_b1,
                    no_player_b2=player_b2
                )

                logger.info(f"Successfully imported match with ID {attributes['NoInTournament']}")
            except Exception as e:
                logger.error(f"Failed to import match with ID {attributes['NoInTournament']}: {str(e)}")
                logger.error(f"Match details: {attributes}")
