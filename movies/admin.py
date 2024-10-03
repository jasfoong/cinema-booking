from django.contrib import admin
from .models import Movie, Theatre, Showtimes, Ticket

admin.site.register(Movie)
admin.site.register(Theatre)
admin.site.register(Showtimes)
admin.site.register(Ticket)