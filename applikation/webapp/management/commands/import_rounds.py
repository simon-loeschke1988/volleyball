import requests
from xml.etree import ElementTree
import pandas as pd
from django.core.management.base import BaseCommand
from webapp.models import BeachRound, BeachTournament
import hashlib

class Command(BaseCommand):
    help = "Import BeachRounds from XML API response"

    def handle(self, *args, **kwargs):
        # URL und Payload für die API-Anfrage
        url = "https://www.fivb.org/vis2009/XmlRequest.asmx"
        payload = {
            "Request": "<Requests> <Request Type='GetBeachRoundList' Fields='Code Name Bracket No NoTournament'></Request></Requests>"
        }

        # Ausführen der API-Anfrage
        response = requests.get(url, params=payload)

        if response.status_code != 200:
            self.stdout.write(self.style.ERROR('Failed to retrieve data'))
            return

        # Verarbeiten der XML-Antwort
        xml_response = ElementTree.fromstring(response.content)
        data = []

        for round in xml_response.findall('.//BeachRound'):
            no = round.attrib.get('No')
            code = round.attrib.get('Code')
            name = round.attrib.get('Name')
            bracket = round.attrib.get('Bracket')
            NoTournament_id = round.attrib.get('NoTournament')

            if None not in [no, code, name, bracket, NoTournament_id]:
                data.append({
                    'no': no,
                    'code': code,
                    'name': name,
                    'bracket': bracket,
                    'NoTournament_id': int(NoTournament_id),
                })

        # Erstellen eines DataFrame aus den gesammelten Daten
        df = pd.DataFrame(data)

        # Bereinigen und Filtern der Daten
        df = df.dropna()
        df = df.drop_duplicates(subset=['no'])

        csv_file = 'beach_ROUNDS_data.csv'
        df.to_csv(csv_file, index=False)

        # Berechnung des SHA256-Hashwerts der CSV-Datei
        with open(csv_file, 'rb') as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()

        # Speichern des Hashwerts in einer Datei
        hash_file = 'beach_ROUNDS_data_hash.txt'
        try:
            with open(hash_file, 'r') as f:
                existing_hash = f.read()
        except FileNotFoundError:
            existing_hash = ''
        
        should_import = existing_hash != file_hash

        if  should_import or not BeachRound.objects.exists():
            with open(hash_file, 'w') as f:
                    f.write(file_hash)

            while not BeachTournament.objects.exists():
                self.stdout.write(self.style.ERROR('BeachTournament Tabelle ist leer. Bitte zuerst BeachTournaments importieren.'))
                return
            else:                                                            
                # Importieren der bereinigten Daten in die Datenbank
                for index, row in df.iterrows():
                    tournament_instance = BeachTournament.objects.filter(no=row['NoTournament_id']).first()
                    if tournament_instance:
                        BeachRound.objects.update_or_create(
                            no=row['no'],
                            defaults={
                                'code': row['code'],
                                'name': row['name'],
                                'bracket': row['bracket'],
                                'NoTournament': tournament_instance,
                            }
                        )

                if df.empty:
                    self.stdout.write(self.style.WARNING('Keine BeachRound Elemente zum Importieren gefunden'))
                else:
                    self.stdout.write(self.style.SUCCESS('BeachRounds erfolgreich importiert.'))                        
