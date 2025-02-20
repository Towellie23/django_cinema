from django.contrib import admin
from .models import Movie, Director, Actor, Genre, Session


@admin.action(description='Скидка 30 процентов на билеты')
def sale_tickets(modeladmin, request, queryset):
    for session in queryset:
        session.ticket_price = int(session.ticket_price * 0.7)
        session.save()
    modeladmin.message_user(request, 'Скидка была применена к выбранным сеансам')



class SessionInline(admin.TabularInline):
    model = Session
    extra = 1


class MovieAdmin(admin.ModelAdmin):
    list_display = ('movie_name', 'release_date', 'image')
    list_filter = ('actors', 'genres', 'director')
    search_fields = ('movie_name',)
    ordering = ('movie_name',)
    inlines = [SessionInline]

class ActorAdmin(admin.ModelAdmin):
    list_display = ('name', 'sex', 'oscars', 'image')


class SessionAdmin(admin.ModelAdmin):
    list_display = ('movie', 'start_time', 'ticket_price')
    list_editable = ('ticket_price',)
    actions = [sale_tickets]


admin.site.register(Movie, MovieAdmin)
admin.site.register(Director)
admin.site.register(Actor, ActorAdmin)
admin.site.register(Genre)
admin.site.register(Session, SessionAdmin)
