from django.shortcuts import render, get_object_or_404
from .models import Movie, Showtimes

def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'movies/movie_list.html', {'movies': movies})

def movie_details(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    showtimes = Showtimes.objects.filter(movie=movie)
    return render(request, 'movies/movie_details.html', {'movie': movie, 'showtimes': showtimes})