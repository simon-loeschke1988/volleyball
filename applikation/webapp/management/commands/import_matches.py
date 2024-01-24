from django.core.management.base import BaseCommand
from xml.etree import ElementTree
import requests


from webapp.models import BeachMatch



class Command(BaseCommand):
    help = "Import BeachMatches from XML API response"

    def handle(self, *args, **kwargs):
        url = "https://www.fivb.org/vis2009/XmlRequest.asmx"
        payload = {
            "Request": "<Request Type='GetBeachMatchList' Fields='NoInTournament LocalDate LocalTime NoTeamA NoTeamB Court MatchPointsA MatchPointsB PointsTeamASet1 PointsTeamBSet1 PointsTeamASet2 PointsTeamBSet2 PointsTeamASet3 PointsTeamBSet3 DurationSet1 DurationSet2 DurationSet3 NoRound NoTournament NoPlayerA1 NoPlayerA2 NoPlayerB1 NoPlayerB2'> </Request>"
        }

        response = requests.get(url, params=payload)
        if response.status_code != 200:
            #logger.error(f"Failed to retrieve data with status code: {response.status_code}")
            return

        xml_response = ElementTree.fromstring(response.content)

        for match in xml_response.findall('BeachMatch'):
            try:
                BeachMatch.objects.create(
                    no_in_tournament=match.attrib.get('NoInTournament'),
                    local_date=match.attrib.get('LocalDate'),
                    local_time=match.attrib.get('LocalTime'),
                    team_a=match.attrib.get('NoTeamA'),
                    team_b=match.attrib.get('NoTeamB'),
                    court=match.attrib.get('Court'),
                    match_points_a=match.attrib.get('MatchPointsA'),
                    match_points_b=match.attrib.get('MatchPointsB'),
                    points_team_a_set1=match.attrib.get('PointsTeamASet1'),
                    points_team_b_set1=match.attrib.get('PointsTeamBSet1'),
                    points_team_a_set2=match.attrib.get('PointsTeamASet2'),
                    points_team_b_set2=match.attrib.get('PointsTeamBSet2'),
                    points_team_a_set3=match.attrib.get('PointsTeamASet3'),
                    points_team_b_set3=match.attrib.get('PointsTeamBSet3'),
                    duration_set1=match.attrib.get('DurationSet1'),
                    duration_set2=match.attrib.get('DurationSet2'),
                    duration_set3=match.attrib.get('DurationSet3'),
                    no_round=match.attrib.get('NoRound'),
                    no_tournament=match.attrib.get('NoTournament'),
                    no_player_a1=match.attrib.get('NoPlayerA1'),
                    no_player_a2=match.attrib.get('NoPlayerA2'),
                    no_player_b1=match.attrib.get('NoPlayerB1'),
                    no_player_b2=match.attrib.get('NoPlayerB2')
                )
            
            except Exception as e:
                pass
              

