import requests
import xml.etree.ElementTree as ET
import pandas as pd
import hashlib
from django.core.management.base import BaseCommand
from webapp.models import Player, BeachTeam, BeachMatch

class Command(BaseCommand):
    help = 'Import players from the specified XML request'

    def handle(self, *args, **kwargs):
        
      
        
        
        # URL und Payload für den Request
        url = "https://www.fivb.org/vis2009/XmlRequest.asmx"
        payload = {
            "Request": "<Request Type='GetPlayerList' Fields='FederationCode FirstName LastName Nationality Gender No'/>"
        }

        # Ausführen des Requests
        response = requests.get(url, params=payload)

        if response.status_code == 200:
            root = ET.fromstring(response.content)
            data = []

            # Extrahieren und Sammeln der Spielerdaten
            for player in root.findall('Player'):
                federation_code = player.get('FederationCode')
                first_name = player.get('FirstName')
                last_name = player.get('LastName')
                no_text = player.get('No')
                no = int(no_text) if no_text is not None else None
                nationality = player.get('Nationality')
                gender = player.get('Gender')

                data.append({
                    'federation_code': federation_code,
                    'first_name': first_name,
                    'last_name': last_name,
                    'no': no,
                    'nationality': nationality,
                    'gender': gender,
                })

            # Erstellen eines DataFrame aus den gesammelten Daten
            df = pd.DataFrame(data)

            # Filtern der Daten
            df = df[df['no'].notnull() & df['first_name'].notnull()]
            df = df[~df['first_name'].str.contains(r'\?|suspended', case=False, na=False)]
            df = df.drop_duplicates(subset=['no'])

            # Speichern der Daten in einer CSV-Datei
            csv_file = 'players_data.csv'
            df.to_csv(csv_file, index=False)

            # Berechnung des SHA256-Hashwerts der CSV-Datei
            with open(csv_file, 'rb') as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()

            # Speichern des Hashwerts in einer Datei
            hash_file = 'players_data_hash.txt'
            try:
                with open(hash_file, 'r') as f:
                    existing_hash = f.read()
            except FileNotFoundError:
                existing_hash = ''

            # Prüfen, ob die Tabelle leer ist oder sich der Hashwert geändert hat
            should_import = not Player.objects.exists() or file_hash != existing_hash

            if should_import:
                with open(hash_file, 'w') as f:
                    f.write(file_hash)
                  # Löschen der Teams in der Datenbank, da Fremdschlüsselbeziehung zu Spielern besteht, wenn die
                  # Tabelle Spieler nicht leer ist
 
                BeachTeam.objects.all().delete()
                BeachMatch.objects.all().delete()
                # Importieren der Daten in die Datenbank
                for index, row in df.iterrows():
                    
                    player_obj = Player(
                        federation_code=row['federation_code'],
                        first_name=row['first_name'],
                        last_name=row['last_name'],
                        no=row['no'],
                        nationality=row['nationality'],
                        gender=row['gender'],
                    )
                    player_obj.save()
                self.stdout.write(self.style.SUCCESS('Spielerdaten erfolgreich importiert.'))
            else:
                self.stdout.write(self.style.SUCCESS('Keine neuen Daten zum Importieren.'))
        else:
            self.stdout.write(self.style.ERROR(f'Fehler beim Abrufen der Daten: {response.status_code}'))

