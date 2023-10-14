from django.core.management.base import BaseCommand
import requests
from xml.etree import ElementTree
from webapp.models import BeachTeam, Player

class Command(BaseCommand):
    help = 'Imports beach teams from XML request'

    def handle(self, *args, **kwargs):
        url = "https://www.fivb.org/vis2009/XmlRequest.asmx"
        payload = {
            "Request": "<Request Type='GetBeachTeamList' Fields='NoPlayer1 NoPlayer2 Name Rank EarnedPointsTeam EarningsTeam'></Request>"
        }

        response = requests.get(url, params=payload)

        if response.status_code == 200:
            xml_response = ElementTree.fromstring(response.content)
            for team in xml_response.findall('BeachTeam'):
                try:
                    no_player1 = team.attrib.get('NoPlayer1')
                    no_player2 = team.attrib.get('NoPlayer2')
                    player1 = Player.objects.get(no=no_player1)
                    player2 = Player.objects.get(no=no_player2)
                except Player.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"Player not found for Player1 No: {no_player1} or Player2 No: {no_player2}. Skipping this team."))
                    continue
                
                BeachTeam.objects.update_or_create(
                    no=team.attrib.get('No'),
                    defaults={
                        'player1': player1,
                        'player2': player2,
                        'name': team.attrib.get('Name'),
                        'rank': team.attrib.get('Rank') if team.attrib.get('Rank') else None,
                        'earned_points_team': team.attrib.get('EarnedPointsTeam') if team.attrib.get('EarnedPointsTeam') else None,
                        'earnings_team': team.attrib.get('EarningsTeam') if team.attrib.get('EarningsTeam') else None,
                    }
                )
            self.stdout.write(self.style.SUCCESS('Import process completed.'))
        else:
            self.stdout.write(self.style.ERROR(f"Failed to retrieve data: {response.status_code}"))
