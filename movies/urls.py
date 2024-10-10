from django.urls import path
from . import views

urlpatterns = [
    path('', views.movie_list, name='movie_list'),
    path('movies/<int:movie_id>/', views.movie_details, name='movie_details')
]