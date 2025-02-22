from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, TicketBuyForm
from django.contrib.auth import login
from celery import group
from .tasks import task_1
from rest_framework import viewsets
from .serializers import MovieSerializer, SessionSerializer, TicketSerializer
from rest_framework.permissions import IsAuthenticated

def index(request):
    films = Movie.objects.filter(pk__in=[19, 20])
    return render(request, 'app/index.html', {'films': films})

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

def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('session_list')
    else:
        form = UserRegistrationForm()
        return render(request, 'registration.html', {'form': form})


@login_required
def profile(request):
    user = request.user
    tickets = Ticket.objects.filter(user=user)
    return render(request, 'app/profile.html', {'user': user, 'tickets': tickets})

@login_required
def ticket_buy(request, session_pk):
    session = get_object_or_404(Session, pk=session_pk)
    if request.method == 'POST':
        form = TicketBuyForm(request.POST)
        if form.is_valid():
            ticket = Ticket(
                user=request.user,
                session=session,
                ticket_price=session.ticket_price
            )
            ticket.save()
            session.ticket_sold += 1
            session.save()
            return redirect('profile')
    else:
        form = TicketBuyForm()
    return render(request, 'app/ticket_buy.html', {'form': form, 'session': session})



def parallel_tasks(request):
    tasks_group = group(task_1.s(task_id) for task_id in range(1, 6))
    result = tasks_group.apply_async()
    try:
        results = result.get(timeout=20)
    except Exception as e:
        return HttpResponse(f'Ошибка : {e}')

    response_content = '<h1>Результаты задач</h1><ul>'
    for result in results:
        response_content += f'<li>{result}</li>'
    response_content += '</ul>'
    return HttpResponse(response_content)


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]



