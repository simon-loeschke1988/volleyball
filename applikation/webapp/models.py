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
  