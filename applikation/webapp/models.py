from django.db import models

class BeachTeam(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    rank = models.IntegerField(null=True, blank=True)
    earned_points_team = models.PositiveIntegerField(null=True, blank=True)
    earnings_team = models.PositiveIntegerField(null=True, blank=True)
    no = models.PositiveIntegerField(unique=False)
    version = models.PositiveIntegerField(null=True, blank=True)


class BeachTournament(models.Model):
    code = models.CharField(max_length=10, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    federation_code = models.CharField(max_length=10, null=True, blank=True)
    number = models.IntegerField(null=True, blank=True)
    version = models.IntegerField(null=True, blank=True)
    no = models.IntegerField(null=True, blank=True)

    # Hier können Sie weitere Felder hinzufügen, die in Ihren XML-Daten vorhanden sind
    # Zum Beispiel:
    end_date = models.DateField(null=True, blank=True)
    # location = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.code})"
    
class Event(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    no = models.CharField(max_length=100, null=True, blank=True)
    version = models.IntegerField(null=True, blank=True)
