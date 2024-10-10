from django.core.management.base import BaseCommand
from movies.models import Movie, Showtimes
from datetime import timedelta
from django.utils import timezone

class Command(BaseCommand):
    help = "Fetch showtimes and populate the database"

    def handle(self, *args, **kwargs):
        Showtimes.objects.all().delete()

        for movie in Movie.objects.all():
            showtimes = self.generate_showtimes_for_movie(movie)

            for showtime in showtimes:

                hour = showtime.hour
                if hour == 14:
                    ticket_price = 12
                elif hour == 17:
                    ticket_price = 18
                elif hour == 20:
                    ticket_price = 15
                else:
                    ticket_price = 15 

                Showtimes.objects.create(
                    movie=movie,
                    showtime=showtime,
                    ticket_price=ticket_price
                )

            self.stdout.write(self.style.SUCCESS(f'Added showtimes for {movie.title}'))

    def generate_showtimes_for_movie(self, movie):
        showtimes = []
        now = timezone.now()
        for day in range(7):
            showtimes.append(now + timedelta(days=day, hours=14))
            showtimes.append(now + timedelta(days=day, hours=17))
            showtimes.append(now + timedelta(days=day, hours=20))
        return showtimes