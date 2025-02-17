from django.contrib import admin
from .models import Movie, Director, Actor, Genre, Session


class MovieAdmin(admin.ModelAdmin):
    list_display = ('movie_name', 'release_date', 'image')


class ActorAdmin(admin.ModelAdmin):
    list_display = ('name', 'sex', 'oscars', 'image')


admin.site.register(Movie, MovieAdmin)
admin.site.register(Director)
admin.site.register(Actor, ActorAdmin)
admin.site.register(Genre)
admin.site.register(Session)
