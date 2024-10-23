from django.db import models

class Genre(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Movie(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    release_date = models.DateField()
    duration = models.IntegerField()
    description = models.TextField()
    poster = models.TextField(default='path/to/default/poster.jpg')

    def __str__(self):
        return self.title 
    
class Showtimes(models.Model):
    id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    showtime = models.DateTimeField()
    ticket_price = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.movie.title} at {self.showtime}"
    
class Seat(models.Model):
    showtime = models.ForeignKey(Showtimes, on_delete=models.CASCADE)
    row = models.CharField(max_length=1)
    number = models.IntegerField()
    is_available = models.BooleanField(default=True)

class Ticket(models.Model):
    id = models.AutoField(primary_key=True)
    showtime = models.ForeignKey(Showtimes, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=5)
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"Seat {self.seat_number} for {self.showtime}"