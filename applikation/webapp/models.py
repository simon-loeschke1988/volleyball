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
    rank = models.IntegerField(null=True, blank=True)
    earned_points_team = models.PositiveIntegerField(null=True, blank=True)
    earnings_team = models.PositiveIntegerField(null=True, blank=True)
    no = models.PositiveIntegerField(unique=True)
    version = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.player1} / {self.player2} ({self.no})"

    class Meta:
        verbose_name_plural = "BeachTeams"
        unique_together = ('player1', 'player2', 'name')
        ordering = ['no']

class BeachRound(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=255)
    bracket = models.CharField(max_length=10)
    phase = models.CharField(max_length=10)
    start_date = models.DateField()
    end_date = models.DateField()
    number = models.IntegerField(unique=True)  # BeachRound-Nummer eindeutig machen
    version = models.IntegerField()

    def __str__(self):
        return self.name
class BeachMatch(models.Model):
    no_in_tournament = models.IntegerField()
    local_date = models.DateField()
    local_time = models.TimeField()
    team_a = models.ForeignKey(BeachTeam, on_delete=models.CASCADE, related_name='matches_team_a', null=True)
    team_b = models.ForeignKey(BeachTeam, on_delete=models.CASCADE, related_name='matches_team_b', null=True)
    court = models.CharField(max_length=10)
    match_points_a = models.IntegerField()
    match_points_b = models.IntegerField()
    points_team_a_set1 = models.IntegerField()
    points_team_b_set1 = models.IntegerField()
    points_team_a_set2 = models.IntegerField()
    points_team_b_set2 = models.IntegerField()
    points_team_a_set3 = models.IntegerField(null=True, blank=True)
    points_team_b_set3 = models.IntegerField(null=True, blank=True)
    duration_set1 = models.IntegerField()
    duration_set2 = models.IntegerField()
    duration_set3 = models.IntegerField(null=True, blank=True)
    no_round = models.ForeignKey(BeachRound, on_delete=models.CASCADE, related_name='matches')
    no_tournament = models.IntegerField()
    no_player_a1 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='matches_as_player_a1', null=True)
    no_player_a2 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='matches_as_player_a2', null=True)
    no_player_b1 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='matches_as_player_b1', null=True)
    no_player_b2 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='matches_as_player_b2', null=True)

    def __str__(self):
        return f"Match {self.id}: {self.team_a} vs. {self.team_b} ({self.no_round})"

    class Meta:
        verbose_name_plural = "Matches"
        unique_together = ('team_a', 'team_b', 'no_round')
        ordering = ['id']
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
    # end_date = models.DateField(null=True, blank=True)
    # location = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.code})"
    
    class Meta:
        verbose_name_plural = "BeachTournaments"
        ordering = ['code']
        