from django.contrib import admin

# Enter my models //Simon Löschke



from .models import Player

class PlayerAdmin(admin.ModelAdmin):
  list_display = ("first_name", "last_name",)

# Register your models here.
admin.site.register(Player, PlayerAdmin)


