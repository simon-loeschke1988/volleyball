import requests
import xml.etree.ElementTree as ET
from django.core.management.base import BaseCommand
from webapp.models import Player 
class Command(BaseCommand):
    help = 'Import players from the specified XML request'

    #############################
    # Bei Änderungen von Fields müssen die Felder in der Datenbank gelöscht werden, models.py, admin.py anpassen und dann folgende Befehle ausführen:
    # python manage.py db_wipe
    # python manage.py migrate
    # python manage.py import_player
    #############################


    def handle(self, *args, **kwargs):
        Player.objects.all().delete()
        url = "https://www.fivb.org/vis2009/XmlRequest.asmx"
        payload = {
            "Request": "<Request Type='GetPlayerList' Fields='FederationCode FirstName Gender LastName Nationality PlaysBeach PlaysVolley TeamName No'/>"
        }
        response = requests.get(url, params=payload)

        if response.status_code == 200:
            root = ET.fromstring(response.content)
            
            for player in root.findall('Player'):
               #no_element = player.get('No')
                federation_code = player.get('FederationCode')
                first_name = player.get('FirstName')
                last_name = player.get('LastName')
                gender_text = player.get('Gender')
                gender = 0 if gender_text.lower() == 'male' else 1
                plays_beach = player.get('PlaysBeach').lower == 'true' if player.get('PlaysBeach') is not None else False
                plays_volley = player.get('PlaysVolley').lower == 'true' if player.get('PlaysVolley') is not None else False
                team_name = player.get('TeamName')
                no_text = player.get('No')
                no = int(no_text) 


                player_obj = Player(
                    federation_code=federation_code,
                    first_name=first_name,
                    last_name=last_name,
                    gender=gender,
                    plays_beach=plays_beach,
                    plays_volley=plays_volley,
                    team_name=team_name,
                    no=no
                )
                player_obj.save()
        else:
            self.stdout.write(self.style.ERROR(f'Failed to retrieve data: {response.status_code}'))
