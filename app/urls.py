from django.urls import path
from . import views



urlpatterns = [
    path('registration/', views.registration, name='registration'),
    path('', views.index, name='home'),
    path('movies_list/', views.movies_list, name='movies_list'),
    path('movies/<int:pk>/', views.movie_detail, name='movie_detail'),
    path('contact', views.contact, name='contact'),
    path('actors/<int:pk>/', views.actor_detail, name='actor_detail'),
    path('session_list/', views.session_list, name='session_list'),
    path('session/<int:pk>/', views.session_detail, name='session_detail'),
    path('session/<int:session_pk>/ticket_buy/', views.ticket_buy, name='ticket_buy'),
    path('director/<int:pk>/', views.director_detail, name='director_detail'),
    path('profile/', views.profile, name='profile'),
    path('run_tasks/', views.parallel_tasks, name='run_tasks'),

]