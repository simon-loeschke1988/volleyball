from django.contrib import admin

# Enter my models //Simon Löschke

from .models import Players, Courts, Matches, Cities, Teams, Tournament

# Register your models here.
admin.site.register(Players)
admin.site.register(Cities)
admin.site.register(Matches)
admin.site.register(Courts)
admin.site.register(Tournament)
admin.site.register(Teams)

