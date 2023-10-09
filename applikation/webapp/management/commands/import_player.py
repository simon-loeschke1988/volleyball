import requests
import xml.etree.ElementTree as ET
from django.core.management.base import BaseCommand
from webapp.models import Player  # Ersetzen Sie 'myapp' durch den Namen Ihrer Django-App

class Command(BaseCommand):
    help = 'Import players from the specified XML request'

    def handle(self, *args, **kwargs):
        url = "https://www.fivb.org/vis2009/XmlRequest.asmx"
        payload = {
            "Request": "<Request Type='GetPlayerList' Fields='FederationCode FirstName Gender LastName Nationality PlaysBeach PlaysVolley TeamName No'/>"
        }
        response = requests.get(url, params=payload)

        if response.status_code == 200:
            root = ET.fromstring(response.content)
            
            for player in root.findall('Player'):
                federation_code = player.find('FederationCode').text if player.find('FederationCode') is not None else ''
                first_name = player.find('FirstName').text if player.find('FirstName') is not None else ''
                last_name = player.find('LastName').text if player.find('LastName') is not None else ''
                gender_text = player.find('Gender').text if player.find('Gender') is not None else ''
                gender = 0 if gender_text.lower() == 'male' else 1
                nationality = player.find('Nationality').text if player.find('Nationality') is not None else ''
                plays_beach = player.find('PlaysBeach').text.lower() == 'true' if player.find('PlaysBeach') is not None else False
                plays_volley = player.find('PlaysVolley').text.lower() == 'true' if player.find('PlaysVolley') is not None else False
                team_name = player.find('TeamName').text if player.find('TeamName') is not None else ''
                no_text = player.find('No').text if player.find('No') is not None else None
                no = int(no_text) if no_text is not None else None

                player_obj = Player(
                    federation_code=federation_code,
                    first_name=first_name,
                    last_name=last_name,
                    gender=gender,
                    nationality=nationality,
                    plays_beach=plays_beach,
                    plays_volley=plays_volley,
                    team_name=team_name,
                    no=no
                )
                player_obj.save()
        else:
            self.stdout.write(self.style.ERROR(f'Failed to retrieve data: {response.status_code}'))
