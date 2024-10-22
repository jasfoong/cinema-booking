import requests
from django.core.management.base import BaseCommand
from movies.models import Movie, Genre
from datetime import datetime, timedelta
from django.conf import settings

class Command(BaseCommand):
    help = 'fetch movies from the TMDb API and populate the database'

    def handle(self, *args, **kwargs):
        Movie.objects.all().delete()

        api_key = settings.TMDB_API_KEY
        now_playing_url = f'https://api.themoviedb.org/3/movie/now_playing?language=en-US&page=1'

        now_playing_response = requests.get(f'{now_playing_url}&api_key={api_key}')

        if now_playing_response.status_code == 200:
            movies_data = now_playing_response.json().get('results', [])

            # Limit number of movies to 5
            movies_data = movies_data[:5]

            for movie_data in movies_data:
                # Fetch movie runtimes from separate API endpoint
                movie_id = movie_data['id']
                details_url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US'
                details_response = requests.get(details_url)

                if details_response.status_code == 200:
                    runtime = details_response.json().get('runtime', 0)

                     # Get the first genre ID from the API response
                    genre_id = movie_data['genre_ids'][0]

                    try:
                        # Fetch the corresponding Genre instance from the database
                        genre = Genre.objects.get(id=genre_id)
                    except Genre.DoesNotExist:
                        self.stdout.write(self.style.ERROR(f"Genre with ID {genre_id} does not exist in the database."))
                        continue  # Skip this movie if the genre doesn't exist

                    # Create or update the movie
                    movie, created = Movie.objects.update_or_create(
                        id = movie_id, 
                        defaults = {
                            'title': movie_data['title'],
                            'genre': genre,
                            'release_date': datetime.strptime(movie_data['release_date'], '%Y-%m-%d'),
                            'duration': runtime,
                            'description': movie_data['overview'],
                        }
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f"Added movie: {movie.title}"))
                    else:
                        self.stdout.write(self.style.WARNING(f"Movie already exists: {movie.title}"))
                else:
                    self.stdout.write(self.style.ERROR(f"Failed to fetch details for movie ID {movie_id}: {details_response.status_code}"))
        else: 
            self.stdout.write(self.style.ERROR(f"Failed to fetch movies: {now_playing_response.status_code}"))
