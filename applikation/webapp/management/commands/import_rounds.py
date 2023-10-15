from django.core.management.base import BaseCommand
from xml.etree import ElementTree
import requests
import logging

from webapp.models import BeachRound

# Konfigurieren Sie das Logging-Modul
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Handler für die Ausgabe der Log-Nachrichten in eine Datei
file_handler = logging.FileHandler('rounds_import.log')
file_handler.setLevel(logging.DEBUG)

# Format für die Log-Nachrichten
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Fügen Sie den Handler zum Logger hinzu
logger.addHandler(file_handler)

class Command(BaseCommand):
    help = "Import BeachRounds from XML API response"

    def handle(self, *args, **kwargs):
        url = "https://www.fivb.org/vis2009/XmlRequest.asmx"
        payload = {
            "Request": "<Requests Type='GetBeachRoundList' Fields='Code Name Bracket Phase StartDate EndDate No'></Requests>"
        }
        payload2 = {
            "Request": "<Requests Type='GetBeachRoundList' Fields='Code Name Bracket Phase StartDate EndDate No'></Requests>"
        }

        response = requests.get(url, params=payload)
        logger.debug(f"URL: {url}")
        logger.debug(f"Payload: {payload}")
        logger.debug(f"Response Status Code: {response.status_code}")
        logger.debug(f"Response Content: {response.content}")

        if response.status_code != 200:
            logger.error(f"Failed to retrieve data with status code: {response.status_code}")
            return

        xml_response = ElementTree.fromstring(response.content)

        for round in xml_response.findall('BeachRound'):
            no = round.attrib.get('No')
            code = round.attrib.get('Code')
            name = round.attrib.get('Name')
            bracket = round.attrib.get('Bracket')
            phase = round.attrib.get('Phase')
            start_date = round.attrib.get('StartDate')
            end_date = round.attrib.get('EndDate')

            # Überprüfen Sie, ob eines der Felder leer ist
            if any(
                not field or field.strip() == ''
                for field in [no, code, name, bracket, phase, start_date, end_date]
            ):
                logger.error(f"Skipping round with missing or empty field. No: {no}")
                continue

            try:
                BeachRound.objects.create(
                    number=no,
                    code=code,
                    name=name,
                    bracket=bracket,
                    phase=phase,
                    start_date=start_date,
                    end_date=end_date
                )

                logger.info(f"Successfully imported round with No: {no}")
            except Exception as e:
                logger.error(f"Failed to import round with No: {no} - {str(e)}")
