from django.core.management.base import BaseCommand
from xml.etree import ElementTree
import requests
#import logging

from webapp.models import BeachMatch

# Konfigurieren Sie das Logging-Modul
#logger = logging.get#logger(__name__)
#logger.setLevel(logging.DEBUG)

# Handler für die Ausgabe der Log-Nachrichten in eine Datei
#file_handler = logging.FileHandler('logs/matches_log.log')
#file_handler.setLevel(logging.DEBUG)

# Format für die Log-Nachrichten
#formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
#file_handler.setFormatter(formatter)

# Fügen Sie den Handler zum #logger hinzu
#logger.addHandler(file_handler)

class Command(BaseCommand):
    help = "Import BeachMatches from XML API response"

    def handle(self, *args, **kwargs):
        url = "https://www.fivb.org/vis2009/XmlRequest.asmx"
        payload = {
            "Request": "<Request Type='GetBeachMatchList' Fields='NoInTournament LocalDate LocalTime NoTeamA NoTeamB Court MatchPointsA MatchPointsB PointsTeamASet1 PointsTeamBSet1 PointsTeamASet2 PointsTeamBSet2 PointsTeamASet3 PointsTeamBSet3 DurationSet1 DurationSet2 DurationSet3 NoRound NoTournament NoPlayerA1 NoPlayerA2 NoPlayerB1 NoPlayerB2'> </Request>"
        }

        response = requests.get(url, params=payload)
        if response.status_code != 200:
            #logger.error(f"Failed to retrieve data with status code: {response.status_code}")
            return

        xml_response = ElementTree.fromstring(response.content)

        for match in xml_response.findall('BeachMatch'):
            try:
                BeachMatch.objects.create(
                    no_in_tournament=match.attrib.get('NoInTournament'),
                    local_date=match.attrib.get('LocalDate'),
                    local_time=match.attrib.get('LocalTime'),
                    team_a=match.attrib.get('NoTeamA'),
                    team_b=match.attrib.get('NoTeamB'),
                    court=match.attrib.get('Court'),
                    match_points_a=match.attrib.get('MatchPointsA'),
                    match_points_b=match.attrib.get('MatchPointsB'),
                    points_team_a_set1=match.attrib.get('PointsTeamASet1'),
                    points_team_b_set1=match.attrib.get('PointsTeamBSet1'),
                    points_team_a_set2=match.attrib.get('PointsTeamASet2'),
                    points_team_b_set2=match.attrib.get('PointsTeamBSet2'),
                    points_team_a_set3=match.attrib.get('PointsTeamASet3'),
                    points_team_b_set3=match.attrib.get('PointsTeamBSet3'),
                    duration_set1=match.attrib.get('DurationSet1'),
                    duration_set2=match.attrib.get('DurationSet2'),
                    duration_set3=match.attrib.get('DurationSet3'),
                    no_round=match.attrib.get('NoRound'),
                    no_tournament=match.attrib.get('NoTournament'),
                    no_player_a1=match.attrib.get('NoPlayerA1'),
                    no_player_a2=match.attrib.get('NoPlayerA2'),
                    no_player_b1=match.attrib.get('NoPlayerB1'),
                    no_player_b2=match.attrib.get('NoPlayerB2')
                )
                #logger.info(f"Successfully imported match with ID {match.attrib.get('NoInTournament')}")
            except Exception as e:
                pass
                #logger.error(f"Failed to import match with ID {match.attrib.get('NoInTournament')}: {str(e)}")
                #logger.error(f"Match details: {match.attrib}")

