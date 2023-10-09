from django.db import models

class Player(models.Model):
    """ FEDERATION_CHOICES = [
        ('USA', 'USA'),
        ('ITA', 'Italy'),
        # ... Andere FederationCodes hinzufügen
    ]
     """
    GENDER_CHOICES = [
        (0, 'Male'),
        (1, 'Female'),
        (3, 'Other'),
    ]

    federation_code = models.CharField(max_length=5, choices=FEDERATION_CHOICES)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.IntegerField(choices=GENDER_CHOICES)
    nationality = models.CharField(max_length=5)  # Kann auch zu einem CHOICES-Feld gemacht werden
    plays_beach = models.BooleanField()
    plays_volley = models.BooleanField()
    team_name = models.CharField(max_length=100)
    no = models.IntegerField(unique=True)
    version = models.IntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.no})"
    class Meta:
        verbose_name_plural = "Players"
        
""" class Cities(models.Model):
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    
    def __str__(self) -> str:
        return f"{self.name} {self.country}"
    class Meta:
        verbose_name_plural = "Cities"
 """
""" class Teams(models.Model):
    name = models.CharField(max_length=200)
    #memeber 1 darf nicht gleich member 2 sein
    member1 = models.ForeignKey(Players, on_delete=models.CASCADE, related_name='team_member1', null=True)
    member2 = models.ForeignKey(Players, on_delete=models.CASCADE, related_name='team_member2', null=True)
    
    
    
    def __str__(self) -> str:
        return f"{self.name}"
    
    class Meta:
        verbose_name_plural = "Teams" """

""" class Rounds(models.Model):
    name = models.CharField(max_length=200)
    teams = models.ManyToManyField(Teams)
    winner = models.ForeignKey(Teams, on_delete=models.CASCADE, related_name='round_winner')
    loser = models.ForeignKey(Teams, on_delete=models.CASCADE, related_name='round_loser')
    date = models.DateTimeField('date played', null=True)
    roundNumber = models.IntegerField(default=2)
    
    class Meta:
        verbose_name_plural = "Rounds" """

""" class Courts(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateTimeField('date played')
    time = models.DateTimeField('time played', null=True)
    roundNumber = models.IntegerField(default=2)
    
    def __str__(self) -> str:
        return f"{self.name}"
    
    class Meta:
        verbose_name_plural = "Courts" """
    
""" class Matches(models.Model):
    team1 = models.ForeignKey(Teams, on_delete=models.CASCADE, related_name='match_team1')
    team2 = models.ForeignKey(Teams, on_delete=models.CASCADE, related_name='match_team2')
    winner = models.ForeignKey(Teams, on_delete=models.CASCADE, related_name='match_winner')
    loser = models.ForeignKey(Teams, on_delete=models.CASCADE, related_name='match_loser')
    date = models.DateTimeField('date played', null=True)
    round = models.ForeignKey(Rounds, on_delete=models.CASCADE, related_name='match_round')
    
    def __str__(self) -> str:
        return f"{self.team1} vs {self.team2}"
    
    class Meta:
        verbose_name_plural = "Matches"
    
 """
""" class Tournament(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateTimeField('date played', null=True)
    round = models.ForeignKey(Rounds, on_delete=models.CASCADE, related_name='tournament_round')
    court = models.ForeignKey(Courts, on_delete=models.CASCADE, related_name='tournament_court')
    winner = models.ForeignKey(Teams, on_delete=models.CASCADE, related_name='tournament_winner')
    loser = models.ForeignKey(Teams, on_delete=models.CASCADE, related_name='tournament_loser')
    city = models.ForeignKey(Cities, on_delete=models.CASCADE, related_name='tournament_city')
    matches = models.ManyToManyField(Matches)
    
    def __str__(self) -> str:
        return f"{self.name}"
    
    class Meta:
        verbose_name_plural = "Tournaments"
     """

    
    