from django.contrib import admin

# Enter my models //Simon Löschke



from .models import Players, Courts, Matches, Cities, Teams, Tournament

class PlayerAdmin(admin.ModelAdmin):
  list_display = ("name", "lastname",)

# Register your models here.
admin.site.register(Players, PlayerAdmin)
admin.site.register(Cities)
admin.site.register(Matches)
admin.site.register(Courts)
admin.site.register(Tournament)
admin.site.register(Teams)

