from django.contrib import admin

# Enter my models //Simon Löschke



from .models import Player, BeachTeam

class PlayerAdmin(admin.ModelAdmin):
  list_display = ("first_name", "last_name",)

class BeachTeamAdmin(admin.ModelAdmin):
  list_display = ("player1", "player2","no")

# Register your models here.
admin.site.register(Player, PlayerAdmin)
admin.site.register(BeachTeam, BeachTeamAdmin)


