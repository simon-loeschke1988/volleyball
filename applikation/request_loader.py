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

        while attempts < max_attempts:
            response = requests.get(f"https://www.fivb.org/vis2009/XmlRequest.asmx?Request=<Request Type='GetPlayer' No='{player_number}' Fields='FederationCode FirstName Gender LastName Nationality PlaysBeach PlaysVolley TeamName' />")
            
            if response.status_code == 400:
                print(f"Bad request for player number {player_number}. Moving to the next player.")
                player_number += 1
                continue
            elif response.status_code != 200:
                print(f"Error with status code {response.status_code} for player number {player_number}")
                continue

            all_responses.append(response.content.decode())

            player_number += 1
            attempts += 1

        # Schreibe alle Antworten in die XML-Datei
        with open('players.xml', 'w', encoding="utf-8") as f:
            for resp in all_responses:
                f.write(resp)


    def get_match(self):
        response = requests.get('https://www.example.com/data.xml')
        root = ET.fromstring(response.content)

        with open('matches.xml', 'wb') as f:
            f.write(root)
    def get_team(self):
        response = requests.get('https://www.example.com/data.xml')
        root = ET.fromstring(response.content)

        with open('teams.xml', 'wb') as f:
            f.write(root)

    def get_court(self):
        response = requests.get('https://www.example.com/data.xml')
        root = ET.fromstring(response.content)

        with open('courts.xml', 'wb') as f:
            f.write(root)
    def get_city(self):
        response = requests.get('https://www.example.com/data.xml')
        root = ET.fromstring(response.content)

        with open('cities.xml', 'wb') as f:
            f.write(root)
    
    def get_tournament(self):
        response = requests.get('https://www.example.com/data.xml')
        root = ET.fromstring(response.content)

        with open('tournaments.xml', 'wb') as f:
            f.write(root)
    
    def get_round(self):
        response = requests.get('https://www.example.com/data.xml')
        root = ET.fromstring(response.content)

        with open('rounds.xml', 'wb') as f:
            f.write(root)

if __name__ == "__main__":
    request_handler = RequestHandler()
    request_handler.get_player()
   # request_handler.get_match()
   # request_handler.get_team()
   # request_handler.get_court()
   # request_handler.get_city()
   # request_handler.get_tournament()
   # request_handler.get_round()

