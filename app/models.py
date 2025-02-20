from django.db import models
from django.contrib.auth.models import User

class BaseModel(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    sex = models.CharField(max_length=10)
    image = models.ImageField(upload_to='movies/', blank=True)


    class Meta:
        abstract = True


class Director(BaseModel):
    film_count = models.IntegerField()

    def __str__(self):
        return self.name

class Actor(BaseModel):
    oscars = models.IntegerField()


    def __str__(self):
        return self.name

class Genre(models.Model):
    genre_name = models.CharField(max_length=100)
    pg_rating = models.IntegerField()

    def __str__(self):
        return self.genre_name


class Movie(models.Model):
    movie_name = models.CharField(max_length=100)
    description = models.TextField()
    director = models.ForeignKey(Director, on_delete=models.CASCADE)
    actors = models.ManyToManyField(Actor)
    genres = models.ManyToManyField(Genre)
    release_date = models.DateField()
    image = models.ImageField(upload_to='movies/', blank=True)

    def __str__(self):
        return self.movie_name


class Session(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, default=1)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    ticket_price = models.IntegerField(default=50)
    ticket_total = models.IntegerField(default=100)
    ticket_sold = models.IntegerField(default=0)

    def __str__(self):
        return f'Сеанс на {self.start_time}'

class Ticket(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    ticket_price = models.IntegerField(default=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Ticket for {self.session} by {self.user}'
