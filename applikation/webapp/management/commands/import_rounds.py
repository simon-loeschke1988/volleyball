import requests
import logging
from xml.etree import ElementTree
from xml.dom import minidom
from django.core.management.base import BaseCommand
from webapp.models import BeachRound  # Ändere 'yourapp' auf den tatsächlichen Namen deiner Django-App

# Konfiguriere das Logging-Modul
logging.basicConfig(filename='runden_import.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Command(BaseCommand):
    help = 'Import data from XML response into the database'

    def handle(self, *args, **kwargs):
        # URL und Payload definieren
        url = "https://www.fivb.org/vis2009/XmlRequest.asmx"
        payload = {
            "Request": "<Requests><Request Type='GetBeachRoundList' Fields='Code Name Bracket Phase StartDate EndDate No NoTournement'></Request></Requests>"
        }

        # HTTP-Anfrage senden
        response = requests.post(url, data=payload)

        # Überprüfen, ob die Anfrage erfolgreich war
        if response.status_code == 200:
            # Antwort in XML umwandeln
            xml_response = ElementTree.fromstring(response.content)

            # Iteriere durch die BeachRound-Elemente in der XML-Antwort und erstelle Django-Objekte.
            for beach_round_elem in xml_response.findall('.//BeachRound'):
                try:
                    BeachRound.objects.create(
                        code=beach_round_elem.get('Code'),
                        name=beach_round_elem.get('Name'),
                        bracket=beach_round_elem.get('Bracket'),
                        phase=beach_round_elem.get('Phase'),
                        start_date=beach_round_elem.get('StartDate'),
                        end_date=beach_round_elem.get('EndDate'),
                        number=beach_round_elem.get('No'),
                        version=beach_round_elem.get('Version')
                    )
                    logging.info(f"Imported round: {beach_round_elem.get('Name')}")
                except Exception as e:
                    logging.warning(f"Skipped round: {beach_round_elem.get('Name')} - {e}")

            self.stdout.write(self.style.SUCCESS('Successfully imported data from XML response.'))
        else:
            self.stdout.write(self.style.ERROR(f'Failed to retrieve data: {response.status_code}'))
