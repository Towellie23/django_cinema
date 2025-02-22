# your_app/serializers.py
from rest_framework import serializers
from .models import Movie, Session, Ticket

class MovieSerializer(serializers.ModelSerializer):
    director_name = serializers.CharField(source='director.name', read_only=True)
    actors_names = serializers.StringRelatedField(many=True, source='actors')
    genres_names = serializers.StringRelatedField(many=True, source='genres')
    class Meta:
        model = Movie
        fields = '__all__'

class SessionSerializer(serializers.ModelSerializer):
    movie_name = serializers.CharField(source='movie.movie_name', read_only=True)
    class Meta:
        model = Session
        fields = '__all__'

class TicketSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    session_start_time = serializers.DateTimeField(source='session.start_time', read_only=True)
    class Meta:
        model = Ticket
        fields = '__all__'
