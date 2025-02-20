from django.core.management.base import BaseCommand
from django.utils import timezone
from app.models import Ticket

class Command(BaseCommand):
    help = 'Delete tickets for sessions that have ended'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        expired_tickets = Ticket.objects.filter(session__end_time__lt=now)
        expired_tickets.delete()
        self.stdout.write(self.style.SUCCESS(f'Deleted {expired_tickets.count()} expired tickets'))
