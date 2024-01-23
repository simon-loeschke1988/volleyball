from django.core.management.base import BaseCommand
from xml.etree import ElementTree
import requests
#

from webapp.models import BeachTeam


class Command(BaseCommand):
    help = "Import BeachTeams from XML API response"

    def handle(self, *args, **kwargs):
        url = "https://www.fivb.org/vis2009/XmlRequest.asmx"
        payload = {
            "Request": "<Request Type='GetBeachTeamList' Fields='Name Rank EarnedPointsTeam EarningsTeam No'> </Request>"
        }

        response = requests.get(url, params=payload)
        if response.status_code != 200:
            #logger.error(f"Failed to retrieve data with status code: {response.status_code}")
            return

        xml_response = ElementTree.fromstring(response.content)

        for team in xml_response.findall('BeachTeam'):
            no_value = team.attrib.get('No')
            
            

            try:
                no_as_number = int(no_value)
            except ValueError:
                #logger.error(f"Invalid 'No' value '{no_value}' for team {team.attrib.get('Name')}. Skipping this team.")
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
                name=team.attrib.get('Name'),
                no=no_as_number,
                defaults={
                    
                    'rank': rank,
                    'earned_points_team': earned_points_team,
                    'earnings_team': earnings_team
                }
            )