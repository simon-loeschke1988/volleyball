from django.contrib import admin

# Enter my models //Simon Löschke



from .models import Player, BeachTeam

class PlayerAdmin(admin.ModelAdmin):
  list_display = ("first_name", "last_name",)

class BeachTeamAdmin(admin.ModelAdmin):
  list_display = ("player1", "player2","no")
  raw_id_fields = ('player1', 'player2')


# Register your models here.
admin.site.register(Player, PlayerAdmin)
admin.site.register(BeachTeam, BeachTeamAdmin)


