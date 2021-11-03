from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone


class Command(BaseCommand):
    def handle(self, *args, **options):
        print(timezone.now())
        print(timezone.now().today())
        print(timezone.datetime.now())
        print(timezone.datetime.today())