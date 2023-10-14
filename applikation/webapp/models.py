from django.db import models

class Player(models.Model):

    GENDER_CHOICES = [
        (0, 'Male'),
        (1, 'Female'),
        (3, 'Other'),
    ]

    federation_code = models.CharField(max_length=5)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.IntegerField(choices=GENDER_CHOICES)
    plays_beach = models.BooleanField()
    plays_volley = models.BooleanField()
    team_name = models.CharField(max_length=100)
    no = models.IntegerField(unique=True)
    

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.no})"
    class Meta:
        verbose_name_plural = "Players"


class BeachTeam(models.Model):
    player1 = models.ForeignKey(Player, related_name="team_as_player1", on_delete=models.CASCADE)
    player2 = models.ForeignKey(Player, related_name="team_as_player2", on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True, blank=True)
    rank = models.IntegerField(null=True, blank=True)  # Kann IntegerField sein, wenn negative Ränge möglich sind.
    earned_points_team = models.PositiveIntegerField(null=True, blank=True)
    earnings_team = models.PositiveIntegerField(null=True, blank=True)  # Angenommen, es handelt sich um einen Ganzzahlwert.
    no = models.PositiveIntegerField(unique=True)
    version = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.player1} / {self.player2} ({self.no})"   
    
    class Meta:
        verbose_name_plural = "BeachTeams"
        unique_together = ('player1', 'player2', 'name')
        ordering = ['no']
        
  