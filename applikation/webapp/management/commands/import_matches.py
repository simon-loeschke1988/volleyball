from django.core.management.base import BaseCommand
from xml.etree import ElementTree
import requests
import pandas as pd
from webapp.models import BeachMatch, BeachTournament, BeachRound

class Command(BaseCommand):
    help = "Import BeachMatches from XML API response"

    def handle(self, *args, **kwargs):
        # Löschen der Tabellen BeachTournament und BeachRound
        BeachTournament.objects.all().delete()
        BeachRound.objects.all().delete()

        url = "https://www.fivb.org/vis2009/XmlRequest.asmx"
        payload = {
            "Request": "<Request Type='GetBeachMatchList' Fields='NoInTournament LocalDate LocalTime NoTeamA NoTeamB Court MatchPointsA MatchPointsB NoRound NoTournament'> </Request>"
        }

        response = requests.get(url, params=payload)
        if response.status_code != 200:
            self.stdout.write(self.style.ERROR(f'Failed to retrieve data with status code: {response.status_code}'))
            return

        xml_response = ElementTree.fromstring(response.content)
        data = []

        for match in xml_response.findall('BeachMatch'):
            match_data = {
                'no_in_tournament': match.attrib.get('NoInTournament'),
                'local_date': match.attrib.get('LocalDate'),
                'local_time': match.attrib.get('LocalTime'),
                'team_a': match.attrib.get('NoTeamA'),
                'team_b': match.attrib.get('NoTeamB'),
                'court': match.attrib.get('Court'),
                'match_points_a': match.attrib.get('MatchPointsA'),
                'match_points_b': match.attrib.get('MatchPointsB'),
                'no_round': match.attrib.get('NoRound'),
                'no_tournament': match.attrib.get('NoTournament'),
            }

            if not any(value is None for value in match_data.values()):
                data.append(match_data)

        # Erstellen eines DataFrame aus den gesammelten Daten
        df = pd.DataFrame(data)

        # Bereinigen und Filtern der Daten
        df = df.dropna()
        df = df.drop_duplicates(subset=['no_in_tournament'])

        # Importieren der bereinigten Daten in die Datenbank
        for index, row in df.iterrows():
            BeachMatch.objects.update_or_create(
                no_in_tournament=row['no_in_tournament'],
                defaults=row.to_dict(),
            )

        if df.empty:
            self.stdout.write(self.style.WARNING('Keine BeachMatch Daten zum Importieren gefunden'))
        else:
            self.stdout.write(self.style.SUCCESS('BeachMatch Daten erfolgreich importiert.'))
