import requests
from django.core.management.base import BaseCommand
from movies.models import Genre
from django.conf import settings

class Command(BaseCommand):
    help = 'Fetch genres from the TMDb API to populate the database'

    def handle (self, *args, **kwargs):
        Genre.objects.all().delete()

        api_key = settings.TMDB_API_KEY
        genres_url = f'https://api.themoviedb.org/3/genre/movie/list?api_key={api_key}&language=en-US'

        genres_response = requests.get(genres_url)

        if genres_response.status_code == 200:
            genres_data = genres_response.json().get('genres', [])

            for genre_data in genres_data:
                genre, created = Genre.objects.get_or_create(
                    id = genre_data['id'],
                    defaults={
                        'name': genre_data['name']
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Added genre: {genre.name}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Genre {genre.name} already exists"))
        else:
            self.stdout.write(self.style.ERROR(f"Failed to fetch genres: {genres_response.status_code}"))