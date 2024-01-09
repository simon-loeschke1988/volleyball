import requests
import logging
from xml.etree import ElementTree as ET

# Logger einrichten
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('applikation/logs/event_import.log')
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

# URL und Payload definieren
url = "https://www.fivb.org/vis2009/XmlRequest.asmx"
payload = {
    "Request": "<Request Type='GetEventList' Fields='Code Name StartDate EndDate'>"
               "<Filter IsVisManaged='True' NoParentEvent='0' HasBeachTournament='True' /></Request>"
}

# HTTP-Anfrage senden
response = requests.get(url, params=payload)

# Logge den Statuscode und die Statusmeldung
logger.info(f"Response Status Code: {response.status_code}")
logger.info(f"Response Status Message: {response.reason}")

# Speichern der Antwort in eine XML-Datei, wenn erfolgreich
if response.status_code == 200:
    with open('eventlist.xml', 'wb') as file:
        file.write(response.content)
else:
    logger.error("Failed to retrieve data")
