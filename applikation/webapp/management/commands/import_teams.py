from django.core.management.base import BaseCommand
from xml.etree import ElementTree
import requests
#import logging

from webapp.models import Player, BeachTeam

#logger = logging.get#logger(__name__)
#logger.setLevel(logging.DEBUG)  # Setzen Sie das gewünschte Log-Level

# Handler für die Ausgabe der Log-Nachrichten in eine Datei
file_handler = logging.FileHandler('logs/team_import.log')
file_handler.setLevel(logging.DEBUG)  # Setzen Sie das gewünschte Log-Level für den Handler

# Format für die Log-Nachrichten
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Fügen Sie den Handler zum #logger hinzu
#logger.addHandler(file_handler)

class Command(BaseCommand):
    help = "Import BeachTeams from XML API response"

    def handle(self, *args, **kwargs):
        url = "https://www.fivb.org/vis2009/XmlRequest.asmx"
        payload = {
            "Request": "<Request Type='GetBeachTeamList' Fields='NoPlayer1 NoPlayer2 Name Rank EarnedPointsTeam EarningsTeam'> </Request>"
        }

        response = requests.get(url, params=payload)
        if response.status_code != 200:
            #logger.error(f"Failed to retrieve data with status code: {response.status_code}")
            return

        xml_response = ElementTree.fromstring(response.content)

        for team in xml_response.findall('BeachTeam'):
            no_value = team.attrib.get('No')
            no_player1 = team.attrib.get('NoPlayer1')
            no_player2 = team.attrib.get('NoPlayer2')
            
            if not no_player1 or not no_player1.isdigit() or not no_player2 or not no_player2.isdigit():
                #logger.warning(f"Invalid player numbers for team: {team.attrib.get('Name')}")
                continue

            if not no_value or not no_value.isdigit():
                #logger.error(f"Missing or empty 'No' value for team {team.attrib.get('Name')}. Skipping this team.")
                continue

            try:
                no_as_number = int(no_value)
            except ValueError:
                #logger.error(f"Invalid 'No' value '{no_value}' for team {team.attrib.get('Name')}. Skipping this team.")
                continue

            # Überprüfen, ob beide Spieler existieren
            player1_instance = Player.objects.filter(no=no_player1).first()
            player2_instance = Player.objects.filter(no=no_player2).first()

            if not player1_instance:
                #logger.warning(f"Player with number {no_player1} not found. Skipping team {team.attrib.get('Name')}.")
                continue

            if not player2_instance:
                #logger.warning(f"Player with number {no_player2} not found. Skipping team {team.attrib.get('Name')}.")
                continue

            # Wenn beide Spieler existieren, dann erstellen oder aktualisieren Sie das BeachTeam
            rank = team.attrib.get('Rank') or None
            if rank and rank.strip() != '':
                try:
                    rank = int(rank)
                except ValueError:
                    #logger.error(f"Invalid rank value '{rank}' for team {team.attrib.get('Name')}. Skipping this team.")
                    continue

            earned_points_team = int(team.attrib.get('EarnedPointsTeam') or 0)
            earnings_team = int(team.attrib.get('EarningsTeam') or 0)

            BeachTeam.objects.update_or_create(
                player1=player1_instance,
                player2=player2_instance,
                name=team.attrib.get('Name'),
                defaults={
                    'no': no_as_number,
                    'rank': rank,
                    'earned_points_team': earned_points_team,
                    'earnings_team': earnings_team
                }
            )

            #logger.info(f"Successfully imported/updated team {team.attrib.get('Name')}")
