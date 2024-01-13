from django.core.management.base import BaseCommand
from xml.etree import ElementTree
import requests
#import logging

from webapp.models import BeachRound

# Konfigurieren Sie das Logging-Modul
#logger = logging.get#logger(__name__)
#logger.setLevel(logging.DEBUG)

# Handler für die Ausgabe der Log-Nachrichten in eine Datei
file_handler = logging.FileHandler('logs/rounds_import.log')
file_handler.setLevel(logging.DEBUG)

# Format für die Log-Nachrichten
#formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
#file_handler.setFormatter(formatter)

# Fügen Sie den Handler zum #logger hinzu
#logger.addHandler(file_handler)

class Command(BaseCommand):
    help = "Import BeachRounds from XML API response"

    def handle(self, *args, **kwargs):
        #logger.debug("Starting import process")

        # URL und Payload für die API-Anfrage
        url = "https://www.fivb.org/vis2009/XmlRequest.asmx"
        payload = {
            "Request": "<Requests> <Request Type='GetBeachRoundList' Fields='Code Name Bracket Phase StartDate EndDate No'></Request></Requests>"
        }

        # Ausführen der API-Anfrage
    
        response = requests.get(url, params=payload)
        #logger.debug(f"URL: {url}")
        #logger.debug(f"Payload: {payload}")
        

        if response.status_code != 200:
            #logger.error(f"Failed to retrieve data with status code: {response.status_code}")
            return
        #logger.debug("vor der verarbeitung")
        # Verarbeiten der XML-Antwort
        xml_response = ElementTree.fromstring(response.content)
        #logger.debug(f"XML Response: {ElementTree.tostring(xml_response, encoding='utf8').decode('utf8')}")

# Überprüfen, ob das Element BeachRound vorhanden ist
        if xml_response.findall('.//BeachRound'):
            #logger.debug("BeachRound Elemente gefunden")
            for round in xml_response.findall('.//BeachRound'):
            # Ihr vorhandener Code zur Verarbeitung jedes BeachRound-Elements
                #logger.debug("In der for schleife")
                no = round.attrib.get('No')
                code = round.attrib.get('Code')
                name = round.attrib.get('Name')
                bracket = round.attrib.get('Bracket')
                phase = round.attrib.get('Phase')
                start_date = round.attrib.get('StartDate')
                end_date = round.attrib.get('EndDate')
                #logger.debug("vor erstellung des objekts")   # Versuch, Daten in die Datenbank zu importieren
                BeachRound.objects.get_or_create(
                    number=no,
                    defaults={
                        'code': code,
                        'name': name,
                        'bracket': bracket,
                        'phase': phase,
                        'start_date': start_date,  # Keine Konvertierung
                        'end_date': end_date,      # Keine Konvertierung
                        
                    }
                )
                #logger.debug("nach erstellung des objekts")
                #logger.info(f"Successfully imported round with No: {no}")
        else:
            print("Keine BeachRound Elemente gefunden")
            
              

            
        
        
                

        try:
            raise Exception("An error occurred")
        except Exception as e:
            print(e)
            #logger.error(f"Failed to import round with No: {no} - {str(e)}")

            
