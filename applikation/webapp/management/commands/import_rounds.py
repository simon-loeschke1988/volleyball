import requests
from xml.etree import ElementTree
import pandas as pd
from django.core.management.base import BaseCommand
from webapp.models import BeachRound, BeachTournament

class Command(BaseCommand):
    help = "Import BeachRounds from XML API response"

    def handle(self, *args, **kwargs):
        # Löschen der Tabelle BeachTournament, da Fremdschlüsselbeziehung zu BeachRound
        BeachTournament.objects.all().delete()

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
            NoTournament = round.attrib.get('NoTournament')

            if None not in [no, code, name, bracket, NoTournament]:
                data.append({
                    'no': no,
                    'code': code,
                    'name': name,
                    'bracket': bracket,
                    'NoTournament': NoTournament,
                })

        # Erstellen eines DataFrame aus den gesammelten Daten
        df = pd.DataFrame(data)

        # Bereinigen und Filtern der Daten
        df = df.dropna()
        df = df.drop_duplicates(subset=['no'])

        # Importieren der bereinigten Daten in die Datenbank
        for index, row in df.iterrows():
            BeachRound.objects.update_or_create(
                no=row['no'],
                defaults={
                    'code': row['code'],
                    'name': row['name'],
                    'bracket': row['bracket'],
                    'NoTournament': row['NoTournament'],
                }
            )

        if df.empty:
            self.stdout.write(self.style.WARNING('Keine BeachRound Elemente zum Importieren gefunden'))
        else:
            self.stdout.write(self.style.SUCCESS('BeachRounds erfolgreich importiert.'))

        
                

        try:
            raise Exception("An error occurred")
        except Exception as e:
            print(e)
            #logger.error(f"Failed to import round with No: {no} - {str(e)}")

            
