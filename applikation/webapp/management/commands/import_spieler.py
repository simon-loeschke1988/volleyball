from django.core.management.base import BaseCommand
import requests
import xmltodict
from webapp.models import Player
import logging

from django.db.utils import IntegrityError



logging.basicConfig(filename='applikation/db_writer.log', level=logging.INFO, format='%(asctime)s - %(message)s')


class Command(BaseCommand):
    help = 'Import players from XML source'

    def handle(self, *args, **kwargs):
            # Hier kommt der Code von get_player_data_and_insert
        
        Player.objects.all().delete()

        player_number = 99999
        max_attempts = 40000000
        attempts = 0

        while attempts < max_attempts:
            response = requests.get(f"https://www.fivb.org/vis2009/XmlRequest.asmx?Request=<Request Type='GetPlayer' No='{player_number}' Fields='FederationCode FirstName Gender LastName Nationality PlaysBeach PlaysVolley TeamName' />")
            
            if response.status_code == 400:
                logging.info(f"Bad request for player number {player_number}. Moving to the next player.")
                player_number += 1
                continue
            elif response.status_code != 200:
                logging.info(f"Error with status code {response.status_code} for player number {player_number}")
                break

            data = xmltodict.parse(response.content)
            player = data.get('Player')

            if player:
                player_instance = Player(
                    federation_code=player.get('@FederationCode'),
                    first_name=player.get('@FirstName'),
                    last_name=player.get('@LastName'),
                    gender=int(player.get('@Gender')),
                    nationality=player.get('@Nationality'),
                    plays_beach=bool(int(player.get('@PlaysBeach'))),
                    plays_volley=bool(int(player.get('@PlaysVolley'))),
                    team_name=player.get('@TeamName'),
                    no = player.get('@No')
                )
                try:
                    player_instance.save()
                    logging.info(f"Inserted player {player.get('@FirstName')} {player.get('@LastName')} with ID {player_instance.id}")
                except IntegrityError as e:
                    logging.info(f"Failed to insert player with number {player.get('@No')}. Error: {e}")
            else:
                logging.info(f"No player found for player number {player_number}")


    
            player_number += 1
            attempts += 1