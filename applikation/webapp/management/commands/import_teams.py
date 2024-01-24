from django.core.management.base import BaseCommand
from xml.etree import ElementTree
import requests
import pandas as pd
import hashlib

from webapp.models import BeachTeam

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

        # Erstellen eines DataFrame aus den gesammelten Daten
        df = pd.DataFrame(data)

        # Filtern der Daten
        df = df.drop_duplicates(subset=['no'])

        # Speichern der Daten in einer CSV-Datei
        csv_file = 'beach_teams_data.csv'
        df.to_csv(csv_file, index=False)

        # Berechnung des SHA256-Hashwerts der CSV-Datei
        with open(csv_file, 'rb') as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()

        # Speichern des Hashwerts in einer Datei
        hash_file = 'beach_teams_data_hash.txt'
        try:
            with open(hash_file, 'r') as f:
                existing_hash = f.read()
        except FileNotFoundError:
            existing_hash = ''

        if file_hash != existing_hash:
            with open(hash_file, 'w') as f:
                f.write(file_hash)

            # Importieren der Daten in die Datenbank
            for index, row in df.iterrows():
                BeachTeam.objects.update_or_create(
                    name=row['name'],
                    no=row['no'],
                    NoPlayer1=row['NoPlayer1'],
                    NoPlayer2=row['NoPlayer2'],
                )
            self.stdout.write(self.style.SUCCESS('BeachTeams erfolgreich importiert.'))
        else:
            self.stdout.write(self.style.SUCCESS('Keine neuen Daten zum Importieren.'))
