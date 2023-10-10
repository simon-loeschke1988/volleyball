import requests
import xml.etree.ElementTree as ET
from django.core.management.base import BaseCommand
from webapp.models import Player  # Ersetzen Sie 'myapp' durch den Namen Ihrer Django-App

class Command(BaseCommand):
    help = 'Wipes all Data from database'

    def handle(self, *args, **kwargs):
        Player.objects.all().delete()