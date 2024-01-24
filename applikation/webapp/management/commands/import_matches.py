from django.core.management.base import BaseCommand
from xml.etree import ElementTree
import requests
import pandas as pd
from webapp.models import BeachMatch, BeachTournament, BeachRound, BeachTeam

class Command(BaseCommand):
    help = "Import BeachMatches from XML API response"

    def handle(self, *args, **kwargs):
        # Löschen der Tabellen BeachTournament und BeachRound
        
        

        url = "https://www.fivb.org/vis2009/XmlRequest.asmx"
        payload = {
            "Request": "<Request Type='GetBeachMatchList' Fields='NoInTournament LocalDate LocalTime NoTeamA NoTeamB Court MatchPointsA MatchPointsB NoRound NoTournament No'> </Request>"
        }

        response = requests.get(url, params=payload)
        if response.status_code != 200:
            self.stdout.write(self.style.ERROR(f'Failed to retrieve data with status code: {response.status_code}'))
            return

        xml_response = ElementTree.fromstring(response.content)
        data = []

        # No = models.IntegerField(primary_key=True)
        # NoInTournament = models.IntegerField(null=True, blank=True)
        # LocalDate = models.DateField(null=True, blank=True)
        # LocalTime = models.TimeField(null=True, blank=True)
        # NoTeamA = models.ForeignKey('BeachTeam', on_delete=models.CASCADE, related_name='NoTeamA', null=True, blank=True)
        # NoTeamB = models.ForeignKey('BeachTeam', on_delete=models.CASCADE, related_name='NoTeamB', null=True, blank=True)
        # Court = models.CharField(max_length=100, null=True, blank=True)
        # MatchPointsA = models.IntegerField(null=True, blank=True)
        # MatchPointsB = models.IntegerField(null=True, blank=True)
        # NoRound = models.ForeignKey('BeachRound', on_delete=models.CASCADE, related_name='NoRound', null=True, blank=True)
        # NoTournament = models.ForeignKey('BeachTournament', on_delete=models.CASCADE, related_name='NoTournament', null=True, blank=True)
    

        for match in xml_response.findall('BeachMatch'):
            match_data = {
                'No': match.attrib.get('No'), # 'No' ist ein reserviertes Schlüsselwort in Python und kann nicht als Feldname verwendet werden
                'NoInTournament': match.attrib.get('NoInTournament'),
                'LocalDate': match.attrib.get('LocalDate'),
                'LocalTime': match.attrib.get('LocalTime'),
                'NoTeamA': match.attrib.get('NoTeamA'),
                'NoTeamB': match.attrib.get('NoTeamB'),
                'Court': match.attrib.get('Court'),
                'MatchPointsA': match.attrib.get('MatchPointsA'),
                'MatchPointsB': match.attrib.get('MatchPointsB'),
                'NoRound': match.attrib.get('NoRound'),
                'NoTournament': match.attrib.get('NoTournament'),
            }

            if not any(value is None for value in match_data.values()):
                data.append(match_data)

        # Erstellen eines DataFrame aus den gesammelten Daten
        df = pd.DataFrame(data)

        # Bereinigen und Filtern der Daten
        df = df.dropna()
        df = df.drop_duplicates(subset=['No'])

        if BeachRound.objects.exists() and BeachTournament.objects.exists():
            df = df[df['NoRound'].isin(BeachRound.objects.values_list('no', flat=True))]
            df = df[df['NoTournament'].isin(BeachTournament.objects.values_list('no', flat=True))]
            for index, row in df.iterrows():
                TeamA = BeachTeam.objects.filter(no=row['NoTeamA']).first()
                TeamB = BeachTeam.objects.filter(no=row['NoTeamB']).first()
                Round = BeachRound.objects.filter(no=row['NoRound']).first()
                Tournament = BeachTournament.objects.filter(no=row['NoTournament']).first()

                if TeamA and TeamB and Round and Tournament:

                    BeachMatch.objects.update_or_create(
                    No=row['No'],
                    NoTeamA=TeamA,
                    NoTeamB=TeamB,
                    NoRound=Round,
                    NoTournament=Tournament,
                    defaults=row.to_dict(),
                    )
                else:
                    self.stdout.write(self.style.WARNING('Keine BeachTeam, BeachRound oder BeachTournament Daten zum Importieren gefunden'))
        

            if df.empty:
                self.stdout.write(self.style.WARNING('Keine BeachMatch Daten zum Importieren gefunden'))
            else:
                self.stdout.write(self.style.SUCCESS('BeachMatch Daten erfolgreich importiert.'))
        else:
        # warten bis BeachRound und BeachTournament importiert wurden
            self.stdout.write(self.style.WARNING('Keine BeachRound und BeachTournament Daten zum Importieren gefunden'))
            self.stdout.write(self.style.WARNING('Bitte importieren Sie zuerst die BeachRound und BeachTournament Daten'))


