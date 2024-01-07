import psycopg2
import requests
from xml.etree import ElementTree
import logging

# Konfigurieren Sie das Logging-Modul
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Handler für die Ausgabe der Log-Nachrichten in eine Datei
file_handler = logging.FileHandler('matches_log.log')
file_handler.setLevel(logging.DEBUG)

# Format für die Log-Nachrichten
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Fügen Sie den Handler zum Logger hinzu
logger.addHandler(file_handler)

# Datenbankverbindungsdaten
db_params = {
    "dbname": "volley",
    "user": "volley",
    "password": "volley",
    "host": "localhost",
}

def import_matches():
    url = "https://www.fivb.org/vis2009/XmlRequest.asmx"
    payload = {
        "Request": "<Request Type='GetBeachMatchList' Fields='...'></Request>"
    }

    response = requests.get(url, params=payload)
    if response.status_code != 200:
        logger.error(f"Failed to retrieve data with status code: {response.status_code}")
        return

    xml_response = ElementTree.fromstring(response.content)

    # Verbindung zur Datenbank herstellen
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    for match in xml_response.findall('BeachMatch'):
        # Daten aus dem XML extrahieren
        no_in_tournament = match.attrib.get('NoInTournament')
        local_date = match.attrib.get('LocalDate')
        local_time = match.attrib.get('LocalTime')
        no_team_a = match.attrib.get('NoTeamA')
        no_team_b = match.attrib.get('NoTeamB')
        court = match.attrib.get('Court')
        match_points_a = match.attrib.get('MatchPointsA')
        match_points_b = match.attrib.get('MatchPointsB')
        # Fügen Sie hier zusätzliche notwendige Felder hinzu

        # SQL-Abfrage zum Einfügen der Daten
        insert_query = """
        INSERT INTO beach_match (no_in_tournament, local_date, local_time, no_team_a, no_team_b, court, match_points_a, match_points_b) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        try:
            cur.execute(insert_query, (no_in_tournament, local_date, local_time, no_team_a, no_team_b, court, match_points_a, match_points_b))
        except psycopg2.Error as e:
            logger.error(f"Failed to import match with ID {no_in_tournament}: {str(e)}")
            continue

    # Änderungen commiten und Verbindung schließen
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    import_matches()
