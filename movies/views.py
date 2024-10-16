from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Movie, Showtimes, Genre

def movie_list(request):
    search_query = request.GET.get('search', '')
    selected_genre = request.GET.get('genre', '')

    movies = Movie.objects.all()

    # Filter movies based on search query and selected genre
    if search_query:
        movies = movies.filter(title__icontains=search_query)
    if selected_genre:
        movies = movies.filter(genre__id=selected_genre)

    genres = Genre.objects.all()

    context = {
        'movies': movies,
        'genres': genres,
        'search_query': search_query,
        'selected_genre': selected_genre
    }

    # Check if request is AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'movies/movie_list_partial.html', context)

    # If request is not AJAX, render the full template
    return render(request, 'movies/movie_list.html', context)

def movie_details(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    showtimes = Showtimes.objects.filter(movie=movie)
    return render(request, 'movies/movie_details.html', {'movie': movie, 'showtimes': showtimes})