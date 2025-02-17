from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.shortcuts import get_object_or_404


def index(request):
    return render(request, 'app/index.html')

def contact(request):
    return render(request, 'app/contact.html')

def movies_list(request):
    movies = Movie.objects.all()
    return render(request, 'app/movies_list.html', {'movies': movies})

def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    actors = movie.actors.all()
    director = movie.director
    return render(request, 'app/movie_detail.html', {'movie': movie, 'actors': actors, 'director': director})

def actor_detail(request, pk):
    actor = get_object_or_404(Actor, pk=pk)
    movies = actor.movie_set.all()
    return render(request, 'app/actor_detail.html', {'actor': actor, 'movies': movies})

def session_list(request):
    sessions = Session.objects.all()
    movies = Movie.objects.all()
    return render(request, 'app/session_list.html', {'sessions': sessions, 'movies': movies})



def session_detail(request, pk):
    session = get_object_or_404(Session, pk=pk)
    movie = session.movie
    return render(request, 'app/session_detail.html', {'session': session, 'movie': movie})

def director_detail(request, pk):
    director = get_object_or_404(Director, pk=pk)
    movies = director.movie_set.all()
    return render(request, 'app/director_detail.html', {'director': director, 'movies': movies})