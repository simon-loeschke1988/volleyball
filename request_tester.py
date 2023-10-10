import requests
from xml.etree import ElementTree
from xml.dom import minidom

# URL und Payload definieren
url = "https://www.fivb.org/vis2009/XmlRequest.asmx"
#payload = {
 #   "Request": "<Request Type='GetPlayerList' Fields='FederationCode FirstName Gender LastName Nationality PlaysBeach PlaysVolley TeamName No'/>"
#}

payload = {
    
"Request": "<Request Type='GetBeachTeamList' Fields='NoPlayer1 NoPlayer2 Name Rank EarnedPointsTeam EarningsTeam'> </Request>"
}



# HTTP-Anfrage senden
response = requests.get(url, params=payload)

# Überprüfen, ob die Anfrage erfolgreich war
if response.status_code == 200:
    # Antwort in XML umwandeln
    xml_response = ElementTree.fromstring(response.content)
    
    # XML mit minidom für eine "hübsche" Formatierung umwandeln
    rough_string = ElementTree.tostring(xml_response, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    pretty_xml_str = reparsed.toprettyxml(indent="  ")

    
    
    # Formatierten XML in eine Datei schreiben
    with open("output.xml", "w", encoding="utf-8") as file:
        file.write(pretty_xml_str)
else:
    print(f"Failed to retrieve data: {response.status_code}")
