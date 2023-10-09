import requests
from xml.etree import ElementTree

# URL und Payload definieren
url = "https://www.fivb.org/vis2009/XmlRequest.asmx"
payload = {
    "Request": "<Request Type='GetPlayerList' Fields='FederationCode FirstName Gender LastName Nationality PlaysBeach PlaysVolley TeamName No'/>"
}

# HTTP-Anfrage senden
response = requests.get(url, params=payload)

# Überprüfen, ob die Anfrage erfolgreich war
if response.status_code == 200:
    # Antwort in XML umwandeln
    xml_response = ElementTree.fromstring(response.content)
    
    # XML in eine Datei schreiben
    with open("output.xml", "wb") as file:
        file.write(ElementTree.tostring(xml_response))
else:
    print(f"Failed to retrieve data: {response.status_code}")
