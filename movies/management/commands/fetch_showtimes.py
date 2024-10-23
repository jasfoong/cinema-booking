from django.core.management.base import BaseCommand
from movies.models import Movie, Showtimes, Seat
from datetime import timedelta
from django.utils import timezone

class Command(BaseCommand):
    help = "Fetch showtimes and populate the database"

    def handle(self, *args, **kwargs):
        Showtimes.objects.all().delete()

        showtime_slots = [10, 13, 15, 18, 20]

        for movie in Movie.objects.all():
            showtimes = self.generate_showtimes_for_movie(movie, showtime_slots)

            for showtime in showtimes:
                created_showtime = Showtimes.objects.create(
                    movie=movie,
                    showtime=showtime,
                    ticket_price=15
                )

                self.generate_seats_for_showtime(created_showtime)

            self.stdout.write(self.style.SUCCESS(f'Added showtimes for {movie.title}'))

    def generate_showtimes_for_movie(self, movie, showtime_slots):
        showtimes = []
        now = timezone.now()

        movie_list = list(Movie.objects.all())

        movie_index = movie_list.index(movie) 

        if movie_index < len(showtime_slots):
            slot_time = showtime_slots[movie_index] 

            for day in range(4): 
                showtime = now.replace(hour=slot_time, minute=0, second=0, microsecond=0) + timedelta(days=day)
                showtimes.append(showtime)

        return showtimes
    
    def generate_seats_for_showtime(self, showtime):
        rows = ['A', 'B', 'C', 'D', 'E', 'F']
        seats_per_row = 10

        for row in rows:
            for seat_number in range(1, seats_per_row + 1):
                Seat.objects.create(
                    showtime=showtime,
                    row=row,
                    number=seat_number,
                    is_available=True
                )
        self.stdout.write(self.style.SUCCESS(f'Added seats for showtime {showtime}'))