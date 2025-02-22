import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Session, Ticket
from django_seed import Seed
class Command(BaseCommand):
    # этот класс наследуестя от бэйскоманд и предоставляет
    # возможность нам работать с ним через manage py
    help = 'Создание пользователей и покупка билетов на сеансы'

    def handle(self, *args, **kwargs):
        seeder = Seed.seeder()

        seeder.add_entity(User, 5, {
            'username': lambda x: seeder.faker.unique.user_name(),
            'password': 'password',
        })

        inserted_pks = seeder.execute()
        sessions = Session.objects.all()

        users = User.objects.all()
        for user in users:
            session = seeder.faker.random_element(elements=sessions)
            Ticket.objects.create(session=session, ticket_price=session.ticket_price, user=user)

        self.stdout.write(self.style.SUCCESS('Сид был выполнен успешно'))


