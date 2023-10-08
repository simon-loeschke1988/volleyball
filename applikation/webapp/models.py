from django.db import models

class Players(models.Model):
    name = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200, null=True)
    gender = models.CharField(max_length=200,null=True)
    country = models.CharField(max_length=200, default="None")
    birthdate = models.DateTimeField('date of birth', null=True)
    age = models.IntegerField(default=0)
    
    def __str__(self) -> str:
        return f"{self.name}"
    
    class Meta:
        verbose_name_plural = "Players"
        
class Cities(models.Model):
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    
    def __str__(self) -> str:
        return f"{self.name} {self.country}"
    class Meta:
        verbose_name_plural = "Cities"

class Teams(models.Model):
    name = models.CharField(max_length=200)
    #memeber 1 darf nicht gleich member 2 sein
    member1 = models.ForeignKey(Players, on_delete=models.CASCADE, related_name='team_member1', null=True)
    member2 = models.ForeignKey(Players, on_delete=models.CASCADE, related_name='team_member2', null=True)
    
    
    
    def __str__(self) -> str:
        return f"{self.name}"
    
    class Meta:
        verbose_name_plural = "Teams"

class Rounds(models.Model):
    name = models.CharField(max_length=200)
    teams = models.ManyToManyField(Teams)
    winner = models.ForeignKey(Teams, on_delete=models.CASCADE, related_name='round_winner')
    loser = models.ForeignKey(Teams, on_delete=models.CASCADE, related_name='round_loser')
    date = models.DateTimeField('date played', null=True)
    roundNumber = models.IntegerField(default=2)
    
    class Meta:
        verbose_name_plural = "Rounds"

class Courts(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateTimeField('date played')
    time = models.DateTimeField('time played', null=True)
    roundNumber = models.IntegerField(default=2)
    
    def __str__(self) -> str:
        return f"{self.name}"
    
    class Meta:
        verbose_name_plural = "Courts"
    
class Matches(models.Model):
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
    

class Tournament(models.Model):
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
    

    
    