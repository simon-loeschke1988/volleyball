import requests
import xml.etree.ElementTree as ET



class RequestHandler:
    def __init__(self):
        pass

    # die urls werden in den jeweiligen funktionen angegeben


    def get_player(self):
        player_number = 99999
        all_responses = []

        # Füge eine Begrenzung hinzu, um endlose Anfragen zu vermeiden
        max_attempts = 100000000
        attempts = 0

       
        response = requests.get(f"https://www.fivb.org/vis2009/XmlRequest.asmx?Request=<Request Type='GetPlayerList' Fields='FederationCode FirstName Gender LastName Nationality PlaysBeach PlaysVolley TeamName No'/>")
            
          
        all_responses.append(response.content.decode())

          
        # Schreibe alle Antworten in die XML-Datei
        with open('spieler.xml', 'w', encoding="utf-8") as f:
            f.write("<Players>")
            for response in all_responses:
                f.write(response)
            f.write("</Players>")
