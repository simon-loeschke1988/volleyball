import requests

url = "https://www.fivb.org/vis2009/XmlRequest.asmx"
payload = {
            "Request": "<Request Type='GetPlayerList' Fields='FederationCode FirstName Gender LastName Nationality PlaysBeach PlaysVolley TeamName No'/>"
        }
response = requests.get(url, params=payload)
        


if response.status_code == 200:
    print(response.content)