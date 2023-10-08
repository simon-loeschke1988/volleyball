from django.db import models

class Players(models.Model):
    name = models.CharField(max_length=200)
    age = models.IntegerField(default=0)
    
    class Meta:
        verbose_name_plural = "Players"
class Cities(models.Model):
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    
    class Meta:
        verbose_name_plural = "Cities"

class Teams(models.Model):
    name = models.CharField(max_length=200)
    members = models.ManyToManyField(Players)
    
    class Meta:
        verbose_name_plural = "Teams"

class Rounds(models.Model):
    name = models.CharField(max_length=200)
    teams = models.ManyToManyField(Teams)
    winner = models.ForeignKey(Teams, on_delete=models.CASCADE, related_name='round_winner')
    loser = models.ForeignKey(Teams, on_delete=models.CASCADE, related_name='round_loser')
    date = models.DateTimeField('date played')
    roundNumber = models.IntegerField(default=2)
    
    class Meta:
        verbose_name_plural = "Rounds"

class Courts(models.Model):
    name = models.CharField(max_length=200)
    round = models.ForeignKey(Rounds, on_delete=models.CASCADE, related_name='court_round')
    date = models.DateTimeField('date played')
    roundNumber = models.IntegerField(default=2)
    
    class Meta:
        verbose_name_plural = "Courts"
    
class Matches(models.Model):
    team1 = models.ForeignKey(Teams, on_delete=models.CASCADE, related_name='match_team1')
    team2 = models.ForeignKey(Teams, on_delete=models.CASCADE, related_name='match_team2')
    winner = models.ForeignKey(Teams, on_delete=models.CASCADE, related_name='match_winner')
    loser = models.ForeignKey(Teams, on_delete=models.CASCADE, related_name='match_loser')
    date = models.DateTimeField('date played')
    round = models.ForeignKey(Rounds, on_delete=models.CASCADE, related_name='match_round')
    
    class Meta:
        verbose_name_plural = "Matches"
    

class Tournament(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateTimeField('date played')
    round = models.ForeignKey(Rounds, on_delete=models.CASCADE, related_name='tournament_round')
    court = models.ForeignKey(Courts, on_delete=models.CASCADE, related_name='tournament_court')
    winner = models.ForeignKey(Teams, on_delete=models.CASCADE, related_name='tournament_winner')
    loser = models.ForeignKey(Teams, on_delete=models.CASCADE, related_name='tournament_loser')
    city = models.ForeignKey(Cities, on_delete=models.CASCADE, related_name='tournament_city')
    matches = models.ManyToManyField(Matches)
    
    class Meta:
        verbose_name_plural = "Tournaments"
    

    
    