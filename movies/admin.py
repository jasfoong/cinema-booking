from django.contrib import admin
from .models import Movie, Showtimes, Ticket

admin.site.register(Movie)
admin.site.register(Showtimes)
admin.site.register(Ticket)