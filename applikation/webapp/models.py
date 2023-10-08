from django.db import models

class Players(models.Model):
    name = models.CharField(max_length=200)
    age = models.IntegerField(default=0)

class Teams(models.Model):
    name = models.CharField(max_length=200)
    members = models.ManyToManyField(Players)

class rounds(models.Model):
    name = models.CharField(max_length=200)
    teams = models.ManyToManyField(Teams)
    winner = models.ForeignKey(Teams, on_delete=models.CASCADE, related_name='round_winner')
    loser = models.ForeignKey(Teams, on_delete=models.CASCADE, related_name='round_loser')
    date = models.DateTimeField('date played')
    roundNumber = models.IntegerField(default=2)

class courts(models.Model):
    name = models.CharField(max_length=200)
    round = models.ForeignKey(rounds, on_delete=models.CASCADE, related_name='court_round')
    date = models.DateTimeField('date played')
    roundNumber = models.IntegerField(default=2)
    city = models.CharField(max_length=200)
    country = models.CharField(max_length=200)

class matches(models.Model):
    team1 = models.ForeignKey(Teams, on_delete=models.CASCADE, related_name='match_team1')
    team2 = models.ForeignKey(Teams, on_delete=models.CASCADE, related_name='match_team2')
    winner = models.ForeignKey(Teams, on_delete=models.CASCADE, related_name='match_winner')
    loser = models.ForeignKey(Teams, on_delete=models.CASCADE, related_name='match_loser')
    date = models.DateTimeField('date played')
    round = models.ForeignKey(rounds, on_delete=models.CASCADE, related_name='match_round')

class tournament(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateTimeField('date played')
    round = models.ForeignKey(rounds, on_delete=models.CASCADE, related_name='tournament_round')
    court = models.ForeignKey(courts, on_delete=models.CASCADE, related_name='tournament_court')
    winner = models.ForeignKey(Teams, on_delete=models.CASCADE, related_name='tournament_winner')
    loser = models.ForeignKey(Teams, on_delete=models.CASCADE, related_name='tournament_loser')
    city = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    matches = models.ManyToManyField(matches)
    
    