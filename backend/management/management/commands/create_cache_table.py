from django.core.management.base import BaseCommand
from django.db import connection
from django.core.management import call_command

from settings import settings


class Command(BaseCommand):
    help = 'Check and create cache table if not exists'

    def handle(self, *args, **options):
        if settings.CACHE_ENGINE == 0:
            call_command('createcachetable')
        else:
            self.stdout.write(self.style.SUCCESS('Cache table not needed.'))
