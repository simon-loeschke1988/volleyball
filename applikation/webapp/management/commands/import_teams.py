import requests
from xml.etree import ElementTree
import pandas as pd
import hashlib
from django.core.management.base import BaseCommand
from webapp.models import BeachTeam, Player

class Command(BaseCommand):
    help = "Import BeachTeams from XML API response"

    def handle(self, *args, **kwargs):
        url = "https://www.fivb.org/vis2009/XmlRequest.asmx"
        payload = {
            "Request": "<Request Type='GetBeachTeamList' Fields='Name No NoPlayer1 NoPlayer2'></Request>"
        }

        response = requests.get(url, params=payload)
        if response.status_code != 200:
            self.stdout.write(self.style.ERROR(f'Failed to retrieve data: {response.status_code}'))
            return

        xml_response = ElementTree.fromstring(response.content)
        data = []

        for team in xml_response.findall('BeachTeam'):
            no_value = team.attrib.get('No')
            name = team.attrib.get('Name')
            NoPlayer1 = team.attrib.get('NoPlayer1')
            NoPlayer2 = team.attrib.get('NoPlayer2')

            if name and '?' not in name and no_value:
                data.append({
                    'name': name,
                    'no': no_value,
                    'NoPlayer1': NoPlayer1,
                    'NoPlayer2': NoPlayer2,
                })

        df = pd.DataFrame(data)
        df = df.drop_duplicates(subset=['no'])

        csv_file = 'beach_teams_data.csv'
        df.to_csv(csv_file, index=False)

        with open(csv_file, 'rb') as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()

        hash_file = 'beach_teams_data_hash.txt'
        try:
            with open(hash_file, 'r') as f:
                existing_hash = f.read()
        except FileNotFoundError:
            existing_hash = ''

        if file_hash != existing_hash:
            with open(hash_file, 'w') as f:
                f.write(file_hash)

            while not Player.objects.exists():
                self.stdout.write(self.style.ERROR('Player Tabelle ist leer. Bitte zuerst Player importieren.'))
                return
            else:

                for index, row in df.iterrows():
                    # Sicherstellen, dass die Spieler-IDs korrekt als Integer behandelt werden
                    player_1_id = pd.to_numeric(row['NoPlayer1'], errors='coerce', downcast='integer')
                    player_2_id = pd.to_numeric(row['NoPlayer2'], errors='coerce', downcast='integer')

                    # Suchen der Player-Objekte
                    player_1 = Player.objects.filter(no=player_1_id).first() if not pd.isna(player_1_id) else None
                    player_2 = Player.objects.filter(no=player_2_id).first() if not pd.isna(player_2_id) else None

                    if player_1 and player_2:
                        BeachTeam.objects.update_or_create(
                            no=row['no'],
                            defaults={
                                'name': row['name'],
                                'NoPlayer1': player_1,
                                'NoPlayer2': player_2,
                            }
                        )
                    else:
                        self.stdout.write('Es konnte keine Instanz des Teams angelegt werden. Player nicht gefunden')
                else:
                    self.stdout.write(self.style.SUCCESS('Successfully imported BeachTeams'))

