from celery import shared_task
from django.core.management import call_command

    #@shared_task
    #def import_player_task():
    #    call_command('import_player')

@shared_task
def import_events_task():
    call_command('import_events')

#@shared_task
#def import_rounds_task():
#    call_command('import_rounds')

#@shared_task
#def import_matches_task():
#    call_command('import_matches')

@shared_task
def import_tournaments_task():
    call_command('import_tournaments')

@shared_task
def import_teams_task():
    call_command('import_teams')
