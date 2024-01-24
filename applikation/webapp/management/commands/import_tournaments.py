import requests
from xml.etree import ElementTree
import pandas as pd
import hashlib
from datetime import datetime
from django.core.management.base import BaseCommand
from webapp.models import BeachTournament, Event

class Command(BaseCommand):
    help = "Import BeachTournaments from XML API response"

    def handle(self, *args, **kwargs):
        
        # löschen der Tabelle Event da Fremdschlüssel
        
        
        url = "https://www.fivb.org/vis2009/XmlRequest.asmx"
        payload_gettournamentlist = {
            "Request": "<Request Type='GetBeachTournamentList' Fields='Code Name StartDateMainDraw EndDateMainDraw FederationCode No Gender NoEvent'> </Request>"
        }

        response = requests.get(url, params=payload_gettournamentlist)
        if response.status_code != 200:
            self.stdout.write(self.style.ERROR('Failed to retrieve data'))
            return

        xml_response = ElementTree.fromstring(response.content)
        data = []

        for tournament in xml_response.findall('BeachTournament'):
            start_date_str = tournament.attrib.get('StartDateMainDraw')
            end_date_str = tournament.attrib.get('EndDateMainDraw')
            if start_date_str and end_date_str:
                data.append({
                    'code': tournament.attrib.get('Code'),
                    'name': tournament.attrib.get('Name'),
                    'start_date_str': tournament.attrib.get('StartDateMainDraw'),
                    'end_date_str': tournament.attrib.get('EndDateMainDraw'),
                    'federation_code': tournament.attrib.get('FederationCode'),
                    'no': int(tournament.attrib.get('No')),
                    'gender': tournament.attrib.get('Gender'),
                    'noevent': tournament.attrib.get('NoEvent'),
                })

        df = pd.DataFrame(data)
       
        df['start_date'] = pd.to_datetime(df['start_date_str'], errors='coerce')
        df['end_date'] = pd.to_datetime(df['end_date_str'], errors='coerce')
        df['start_date'] = df['start_date'].apply(lambda x: x if pd.notna(x) else None)
        df['end_date'] = df['end_date'].apply(lambda x: x if pd.notna(x) else None)
        df = df.drop(['start_date_str', 'end_date_str'], axis=1)
        df = df.drop_duplicates(subset=['no'])
        df['noevent'] = df['noevent'].replace('', '0')
        df['noevent'] = pd.to_numeric(df['noevent'], errors='coerce').fillna(0).astype(int)
       # df = df.dropna(subset=['no','noevent'])
       
       
       

        
     

        # Speichern der Daten in einer CSV-Datei
        csv_file = 'beach_tournaments_data.csv'
        df.to_csv(csv_file, index=False)

        # Berechnung des SHA256-Hashwerts der CSV-Datei
        with open(csv_file, 'rb') as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()

        # Speichern des Hashwerts in einer Datei
        hash_file = 'beach_tournaments_data_hash.txt'
        try:
            with open(hash_file, 'r') as f:
                existing_hash = f.read()
        except FileNotFoundError:
            existing_hash = ''

        # Prüfen, ob die Tabelle leer ist oder sich der Hashwert geändert hat
        should_import = not BeachTournament.objects.exists() or file_hash != existing_hash


        while not Event.objects.exists():
            self.stdout.write(self.style.ERROR('Event Tabelle ist leer. Bitte zuerst Events importieren.'))

        else:
            if should_import:
                with open(hash_file, 'w') as f:
                    f.write(file_hash)
                
                        

                # Importieren der Daten in die Datenbank
                for index, row in df.iterrows():
                    BeachTournament.objects.update_or_create(
                        code=row['code'],
                        no=row['no'],
                        defaults={
                            'name': row['name'],
                            'start_date': row['start_date'],
                            'end_date': row['end_date'],
                            'federation_code': row['federation_code'],
                            'gender': row['gender'],
                            
                            'eventnummer': row['noevent'],
                        }
                    )
                self.stdout.write(self.style.SUCCESS('BeachTournaments erfolgreich importiert.'))
            else:
                self.stdout.write(self.style.SUCCESS('Keine neuen Daten zum Importieren.'))
