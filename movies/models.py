from django.db import models

class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    release_date = models.DateField()
    director = models.CharField(max_length=100)
    duration = models.DurationField()
    description = models.TextField()

    def __str__(self):
        return self.title 
    
class Theatre(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    total_seats = models.IntegerField()

    def __str__(self):
        return self.name
    
class Showtimes(models.Model):
    id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    theatre = models.ForeignKey(Theatre, on_delete=models.CASCADE)
    showtime = models.DateTimeField()

    def __str__(self):
        return f"{self.movie.title} at {self.theatre.name} on {self.showtime}"
    
class Ticket(models.Model):
    id = models.AutoField(primary_key=True)
    showtime = models.ForeignKey(Showtimes, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=5)
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"Seat {self.seat_number} for {self.showtime}"