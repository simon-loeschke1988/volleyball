import requests
import xmltodict
import sqlite3
import logging

logging.basicConfig(filename='db_writer.log', level=logging.INFO, format='%(asctime)s - %(message)s')

class Volleyball:

    def __init__(self):
        # Verbindung zur SQLite-Datenbank herstellen
        self.conn = sqlite3.connect('db.sqlite3')
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        # Tabelle erstellen, falls sie nicht existiert
        cursor.execute('''CREATE TABLE IF NOT EXISTS webapp_players 
                          (FederationCode TEXT, FirstName TEXT, LastName TEXT, Gender INTEGER, 
                           Nationality TEXT, PlaysBeach INTEGER, PlaysVolley INTEGER, TeamName TEXT)''')
        self.conn.commit()

    def get_player(self):
        player_number = 999

        # Füge eine Begrenzung hinzu, um endlose Anfragen zu vermeiden
        max_attempts = 100000000
        attempts = 0

        while attempts < max_attempts:
            response = requests.get(f"https://www.fivb.org/vis2009/XmlRequest.asmx?Request=<Request Type='GetPlayer' No='{player_number}' Fields= 'FederationCode FirstName Gender LastName Nationality PlaysBeach PlaysVolley TeamName'/>")
            
            if response.status_code == 400:
                logging.error(f"Bad request for player number {player_number}. Moving to the next player.")
                player_number += 1
                continue
            elif response.status_code != 200:
                logging.error(f"Error with status code {response.status_code} for player number {player_number}")
                continue
            else:
                logging.info(f"{response.status_code} for player number {player_number}")
                logging.info(response.content.decode())

            data = xmltodict.parse(response.content)
            player = data.get('Player')

            if player:
              logging.info("Player found:", player)
              self.insert_into_db(player)
            else:
              logging.info("No player found for player number:", player_number)
            #if player is not None:
            #    self.insert_into_db(player)

            player_number += 1
            attempts += 1

    def insert_into_db(self, player):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO webapp_players VALUES (?, ?, ?, ?, ?, ?, ?, ?)', 
                    (player.get('@FederationCode'), player.get('@FirstName'), player.get('@LastName'), 
                        player.get('@Gender'), player.get('@Nationality'), player.get('@PlaysBeach'), 
                        player.get('@PlaysVolley'), player.get('@TeamName')))
        self.conn.commit()
        logging.info("Inserted player:", player.get('@FirstName'), player.get('@LastName'))

    def insert_test_data(self):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO players (FederationCode, FirstName, LastName) VALUES (?, ?, ?)', 
                    ("TEST", "John", "Doe"))
        self.conn.commit()

    def close_db(self):
        self.conn.close()

    def get_all_players(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM players")
        players = cursor.fetchall()
        logging.info(f"Number of players retrieved: {len(players)}")
        for player in players:
            logging.info(player)


# Beispielverwendung
volley = Volleyball()
volley.create_table()
volley.get_player()
volley.get_all_players()
volley.close_db()