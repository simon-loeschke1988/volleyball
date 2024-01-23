from django.core.management.base import BaseCommand
from xml.etree import ElementTree
import requests
#import logging
from datetime import datetime

from webapp.models import Event

##logger = logging.get#logger(__name__)
#logger.setLevel(logging.DEBUG)

#file_handler = logging.FileHandler('logs/event_import.log')
#file_handler.setLevel(logging.DEBUG)

#formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
#file_handler.setFormatter(formatter)

#logger.addHandler(file_handler)

class Command(BaseCommand):
    help = "Import Events from XML API response"

    def handle(self, *args, **kwargs):
        url = "https://www.fivb.org/vis2009/XmlRequest.asmx"
        payload = {
            "Request": "<Request Type='GetEventList' Fields='Code Name StartDate No EndDate'> <Filter IsVisManaged='True' NoParentEvent='0' HasBeachTournament='True' /> </Request>"
        }

        try:
            response = requests.get(url, params=payload)
            if response.status_code != 200:
                #logger.error(f"Failed to retrieve data with status code: {response.status_code}")
                return

            xml_response = ElementTree.fromstring(response.content)

            for event_xml in xml_response.findall('Event'):
                event_data = {
                    'code': event_xml.attrib.get('Code', None),
                    'name': event_xml.attrib.get('Name', None),
                    'start_date': event_xml.attrib.get('StartDate', None),
                    'end_date': event_xml.attrib.get('EndDate', None),
                    'no': event_xml.attrib.get('No', None),
                    'version': int(event_xml.attrib.get('Version')) if event_xml.attrib.get('Version') else None
                }

                Event.objects.update_or_create(
                    no = event_data['no'],
                    
                    defaults=event_data,
                )

                #logger.info(f"Successfully imported/updated event {event_data['name']}")
        except requests.RequestException as e:
            #logger.error(f"Request failed: {e}")

            def parse_date(self, date_string):
                if not date_string:
                    return None

                return datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S')