from django.core.management.base import BaseCommand
from xml.etree import ElementTree
import requests
#import logging
from datetime import datetime

from webapp.models import BeachTournament

#logger = logging.get#logger(__name__)
#logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('logs/tournament_import.log')
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

#logger.addHandler(file_handler)

class Command(BaseCommand):
    help = "Import BeachTournaments from XML API response"

    def handle(self, *args, **kwargs):
        # URL und Payload definieren
        url = "https://www.fivb.org/vis2009/XmlRequest.asmx"

        # Payload für den Request erstellen
        payload_gettournamentlist = {
            "Request": "<Request Type='GetBeachTournamentList' Fields='Code Name StartDate EndDate FederationCode No'> </Request>"
        }

        # HTTP-Anfrage senden
        response = requests.get(url, params=payload_gettournamentlist)
        if response.status_code != 200:
            #logger.error(f"Failed to retrieve data with status code: {response.status_code}")
            return

        xml_response = ElementTree.fromstring(response.content)

        for tournament in xml_response.findall('BeachTournament'):
            code = tournament.attrib.get('Code')
            name = tournament.attrib.get('Name')
            #start_date_str = tournament.attrib.get('StartDate')
            #end_date_str = tournament.attrib.get('EndDate')
            federation_code = tournament.attrib.get('FederationCode')
            no = tournament.attrib.get('No')

            #if start_date_str:
             #   start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            #else:
            #    start_date = None

            #if end_date_str:
             #   end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
           # else:
            #    end_date = None

            BeachTournament.objects.update_or_create(
                code=code,
                defaults={
                    'name': name,
                 #   'start_date': start_date,
                 #   'end_date': end_date,
                    'federation_code': federation_code,
                    'no': no
                }
            )

            #logger.info(f"Successfully imported/updated tournament {name}")
