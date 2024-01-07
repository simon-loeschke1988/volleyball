from fastapi import FastAPI
import requests
import xml.etree.ElementTree as ET
import redis
import json

app = FastAPI()
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

@app.get("/fetch-data")
async def fetch_data():
    url = "https://www.fivb.org/vis2009/XmlRequest.asmx"
    payload = {
        "Request": "<Requests><Request Type='GetBeachRoundList' Fields='Code Name Bracket Phase StartDate EndDate No NoTournement'></Request>"
    }
    
    # Asynchronen HTTP-Request senden
    response = await requests.get(url, params=payload)

    # XML-Daten parsen
    root = ET.fromstring(response.text)

    # Daten in ein JSON-Format umwandeln
    data_list = []
    for element in root.findall(".//"):
        data = {child.tag: child.text for child in element}
        if data:
            data_list.append(data)

    # JSON-Daten in Redis speichern unter dem Schlüssel 'beach_round_list'
    json_data = json.dumps(data_list)
    redis_client.set("beach_round_list", json_data)

    # JSON-Daten auf der Konsole ausgeben
    print(data_list)

    # JSON-Daten als Liste zurückgeben
    return data_list
