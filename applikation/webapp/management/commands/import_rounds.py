from django.core.management.base import BaseCommand
from xml.etree import ElementTree
import requests


from webapp.models import BeachRound


class Command(BaseCommand):
    help = "Import BeachRounds from XML API response"

    def handle(self, *args, **kwargs):
     

        # URL und Payload für die API-Anfrage
        url = "https://www.fivb.org/vis2009/XmlRequest.asmx"
        payload = {
            "Request": "<Requests> <Request Type='GetBeachRoundList' Fields='Code Name Bracket Phase StartDate EndDate No'></Request></Requests>"
        }

        # Ausführen der API-Anfrage
    
        response = requests.get(url, params=payload)
     

        if response.status_code != 200:
          
            return
       
        # Verarbeiten der XML-Antwort
        xml_response = ElementTree.fromstring(response.content)
      

# Überprüfen, ob das Element BeachRound vorhanden ist
        if xml_response.findall('.//BeachRound'):
          
            for round in xml_response.findall('.//BeachRound'):
            # Ihr vorhandener Code zur Verarbeitung jedes BeachRound-Elements
                
                no = round.attrib.get('No')
                code = round.attrib.get('Code')
                name = round.attrib.get('Name')
                bracket = round.attrib.get('Bracket')
                phase = round.attrib.get('Phase')
                start_date = round.attrib.get('StartDate')
                end_date = round.attrib.get('EndDate')
              
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
                
        else:
            print("Keine BeachRound Elemente gefunden")
            
              

            
        
        
                

        try:
            raise Exception("An error occurred")
        except Exception as e:
            print(e)
            #logger.error(f"Failed to import round with No: {no} - {str(e)}")

            
