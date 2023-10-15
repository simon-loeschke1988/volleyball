import requests
import xml.etree.ElementTree as ET
from django.core.management.base import BaseCommand
from webapp.models import Player, BeachMatch, BeachRound, BeachTeam  # Ersetzen Sie 'myapp' durch den Namen Ihrer Django-App

class Command(BaseCommand):
    help = 'Wipes all Data from database'

    def handle(self, *args, **kwargs):
       # Player.objects.all().delete()
        #BeachTeam.objects.all().delete()
       # BeachMatch.objects.all().delete()
        BeachRound.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully wiped database.'))
        