from django.core.management.base import BaseCommand
from xml.etree import ElementTree
import requests
import pandas as pd
from webapp.models import BeachMatch, BeachTournament, BeachRound, BeachTeam

class Command(BaseCommand):
    help = "Import BeachMatches from XML API response"

    def handle(self, *args, **kwargs):
        url = "https://www.fivb.org/vis2009/XmlRequest.asmx"
        payload = {
            "Request": "<Request Type='GetBeachMatchList' Fields='NoInTournament LocalDate LocalTime NoTeamA NoTeamB Court MatchPointsA MatchPointsB NoRound NoTournament No'></Request>"
        }

        response = requests.get(url, params=payload)
        if response.status_code != 200:
            self.stdout.write(self.style.ERROR(f'Failed to retrieve data with status code: {response.status_code}'))
            return

        xml_response = ElementTree.fromstring(response.content)
        data = []

        for match in xml_response.findall('BeachMatch'):
            local_date = match.attrib.get('LocalDate')
            local_time = match.attrib.get('LocalTime')

            # Nur Daten hinzufügen, wenn LocalDate und LocalTime vorhanden sind
            if local_date and local_time:
                match_data = {
                    'No': match.attrib.get('No'),
                    'NoInTournament': match.attrib.get('NoInTournament'),
                    'LocalDate': local_date,
                    'LocalTime': local_time,
                    'NoTeamA': match.attrib.get('NoTeamA'),
                    'NoTeamB': match.attrib.get('NoTeamB'),
                    'Court': match.attrib.get('Court'),
                    'MatchPointsA': match.attrib.get('MatchPointsA'),
                    'MatchPointsB': match.attrib.get('MatchPointsB'),
                    'NoRound': match.attrib.get('NoRound'),
                    'NoTournament': match.attrib.get('NoTournament'),
                }
                data.append(match_data)

        df = pd.DataFrame(data)
        df = df.dropna()
        df = df.drop_duplicates(subset=['No'])

        if not (BeachRound.objects.exists() and BeachTournament.objects.exists() and BeachTeam.objects.exists()):
            self.stdout.write(self.style.WARNING('Bitte importieren Sie zuerst die BeachRound, BeachTournament und BeachTeam Daten'))
            return

        for index, row in df.iterrows():
            if row['NoTeamA'] and row['NoTeamB']:
                try:
                    TeamA = BeachTeam.objects.get(no=row['NoTeamA'])
                    TeamB = BeachTeam.objects.get(no=row['NoTeamB'])
                    Round = BeachRound.objects.get(no=row['NoRound'])
                    Tournament = BeachTournament.objects.get(no=row['NoTournament'])

                    BeachMatch.objects.update_or_create(
                        No=row['No'],
                        defaults={
                            'NoInTournament': row['NoInTournament'],
                            'LocalDate': pd.to_datetime(row['LocalDate']).date(),
                            'LocalTime': pd.to_datetime(row['LocalTime']).time(),
                            'NoTeamA': TeamA,
                            'NoTeamB': TeamB,
                            'Court': row['Court'],
                            'MatchPointsA': row['MatchPointsA'],
                            'MatchPointsB': row['MatchPointsB'],
                            'NoRound': Round,
                            'NoTournament': Tournament,
                        }
                    )
                except (BeachTeam.DoesNotExist, BeachRound.DoesNotExist, BeachTournament.DoesNotExist) as e:
                    self.stdout.write(self.style.WARNING(f'Fehler beim Importieren eines Matches: {e}'))

        self.stdout.write(self.style.SUCCESS('BeachMatch Daten erfolgreich importiert.'))
