from django.core.management.base import BaseCommand
from xml.etree import ElementTree
import requests
import pandas as pd
from datetime import datetime
from webapp.models import Event

class Command(BaseCommand):
    help = "Import Events from XML API response"

    def parse_date(self, date_string):
        if not date_string:
            return None
        return datetime.strptime(date_string, '%Y-%m-%d')

    def handle(self, *args, **kwargs):
        url = "https://www.fivb.org/vis2009/XmlRequest.asmx"
        payload = {
            "Request": "<Request Type='GetEventList' Fields='Code Name StartDate No EndDate'> <Filter IsVisManaged='True' NoParentEvent='0' HasBeachTournament='True' /> </Request>"
        }
        
        try:
            response = requests.get(url, params=payload)
            if response.status_code != 200:
                self.stdout.write(self.style.ERROR('Failed to retrieve data'))
                return

            xml_response = ElementTree.fromstring(response.content)
            data = []

            for event_xml in xml_response.findall('Event'):
                start_date = self.parse_date(event_xml.attrib.get('StartDate'))
                end_date = self.parse_date(event_xml.attrib.get('EndDate'))

                if start_date and end_date:
                    data.append({
                        'code': event_xml.attrib.get('Code'),
                        'name': event_xml.attrib.get('Name'),
                        'start_date': start_date,
                        'end_date': end_date,
                        'no': int(event_xml.attrib.get('No')),
                        'version': int(event_xml.attrib.get('Version')) if event_xml.attrib.get('Version') else None
                    })
            # zum dataframe das Event mit der Nummer 0 hinzufügen
            data.append({
                        'code': 0,
                        'name': 'No Event',
                        'start_date': None,
                        'end_date': None,
                        'no': '0',
                        'version': None
                    })

            # Erstellen eines DataFrame aus den gesammelten Daten
            df = pd.DataFrame(data)

            # Filtern der Daten
            df = df.dropna(subset=['start_date', 'end_date', 'no'])
            df = df.drop_duplicates(subset=['no'])

            # Importieren der bereinigten Daten in die Datenbank
            for index, row in df.iterrows():
                Event.objects.update_or_create(
                    no=row['no'],
                    defaults=row.to_dict(),
                )
                

            # auf jeden fall ein Event mit der Nummer 0 anlegen
            

            if df.empty:
                self.stdout.write(self.style.WARNING('Keine Events zum Importieren gefunden'))
            else:
                self.stdout.write(self.style.SUCCESS('Events erfolgreich importiert.'))

        except requests.RequestException as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {e}'))
