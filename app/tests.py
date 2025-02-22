from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from .models import Movie, Director, Actor, Genre, Session, Ticket
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone

class MovieTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.director = Director.objects.create(name="Christopher Nolan", age=50, sex="male", film_count=10)
        self.actor1 = Actor.objects.create(name="Leonardo DiCaprio", age=45, sex="male", oscars=1)
        self.actor2 = Actor.objects.create(name="Joseph Gordon-Levitt", age=40, sex="male", oscars=0)
        self.genre = Genre.objects.create(genre_name="Sci-Fi", pg_rating=13)
        self.movie = Movie.objects.create(
            movie_name="Inception",
            description="A mind-bending thriller",
            director=self.director,
            release_date="2010-07-16"
        )
        self.movie.actors.set([self.actor1, self.actor2])
        self.movie.genres.set([self.genre])
        self.session = Session.objects.create(
            movie=self.movie,
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(hours=2),
            ticket_price=10,
            ticket_total=100,
            ticket_sold=50
        )
        self.user = User.objects.create_user(username='TestUser', password='password123')

    def test_movie_list_view(self):
        response = self.client.get(reverse('movie-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Inception')

    def test_movie_detail_view(self):
        response = self.client.get(reverse('movie-detail', args=[self.movie.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Inception')
        self.assertContains(response, 'A mind-bending thriller')
        self.assertContains(response, 'Christopher Nolan')
        self.assertContains(response, 'Leonardo DiCaprio')
        self.assertContains(response, 'Joseph Gordon-Levitt')
        self.assertContains(response, 'Sci-Fi')
        self.assertContains(response, '2010-07-16')

    def test_session_detail_view(self):
        response = self.client.get(reverse('session-detail', args=[self.session.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, str(self.session.start_time.isoformat()))
        self.assertContains(response, str(self.session.end_time.isoformat()))
        self.assertContains(response, self.session.ticket_price)
        self.assertContains(response, self.session.ticket_total)
        self.assertContains(response, self.session.ticket_sold)

    def test_ticket_creation(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('ticket-list'), {
            'session': self.session.id,
            'ticket_price': self.session.ticket_price,
            'user': self.user.id,
        })
        self.assertEqual(response.status_code, 201)
        self.assertContains(response, self.user.username)
        self.assertContains(response, str(self.session.start_time))

    def test_unauthorized_ticket_creation(self):
        response = self.client.post(reverse('ticket-list'), {
            'session': self.session.id,
            'ticket_price': self.session.ticket_price,
            'user': self.user.id,
        })
        self.assertEqual(response.status_code, 403)
