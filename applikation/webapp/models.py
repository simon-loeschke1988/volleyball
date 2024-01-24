from django.db import models

class BeachTeam(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    no = models.PositiveIntegerField(primary_key=True)
    NoPlayer1 = models.ForeignKey('Player', on_delete=models.CASCADE, related_name='NoPlayer1', null=True, blank=True)
    NoPlayer2 = models.ForeignKey('Player', on_delete=models.CASCADE, related_name='NoPlayer2', null=True, blank=True)
    
    
class BeachMatch(models.Model):
    No = models.IntegerField(primary_key=True)
    NoInTournament = models.IntegerField(null=True, blank=True)
    LocalDate = models.DateField(null=True, blank=True)
    LocalTime = models.TimeField(null=True, blank=True)
    NoTeamA = models.ForeignKey('BeachTeam', on_delete=models.CASCADE, related_name='NoTeamA', null=True, blank=True)
    NoTeamB = models.ForeignKey('BeachTeam', on_delete=models.CASCADE, related_name='NoTeamB', null=True, blank=True)
    Court = models.CharField(max_length=100, null=True, blank=True)
    MatchPointsA = models.IntegerField(null=True, blank=True)
    MatchPointsB = models.IntegerField(null=True, blank=True)
    NoRound = models.ForeignKey('BeachRound', on_delete=models.CASCADE, related_name='NoRound', null=True, blank=True)
    NoTournament = models.ForeignKey('BeachTournament', on_delete=models.CASCADE, related_name='NoTournament', null=True, blank=True)
    
class BeachRound(models.Model):
    code = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    bracket = models.CharField(max_length=100, null=True, blank=True)
    no = models.IntegerField(primary_key=True)
    NoTournament = models.ForeignKey('BeachTournament', on_delete=models.CASCADE, related_name='NoTournamentRound', null=True, blank=True)
    

class Player (models.Model):
    federation_code= models.CharField(max_length=100, null=True, blank=True)
    first_name= models.CharField(max_length=100, null=True, blank=True)
    last_name= models.CharField(max_length=100, null=True, blank=True)
    nationality= models.CharField(max_length=100, null=True, blank=True)
    plays_beach= models.BooleanField(null=True, blank=True)
    no= models.IntegerField(primary_key=True)
    gender= models.CharField(max_length=100, null=True, blank=True)
   


class BeachTournament(models.Model):
    code = models.CharField(max_length=10, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    start_date = models.CharField(null=True, blank=True)
    federation_code = models.CharField(max_length=10, null=True, blank=True)
    number = models.IntegerField(null=True, blank=True)
    version = models.IntegerField(null=True, blank=True)
    no = models.IntegerField(primary_key=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    eventnummer = models.IntegerField(null=True, blank=True)

    # Hier können Sie weitere Felder hinzufügen, die in Ihren XML-Daten vorhanden sind
    # Zum Beispiel:
    end_date = models.DateField(null=True, blank=True)
    # location = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.code})"
    
class Event(models.Model):
    
    code = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    no = models.IntegerField(primary_key=True)
    version = models.IntegerField(null=True, blank=True)
