import time

from django.core.management.base import BaseCommand

import ngrok


class Command(BaseCommand):
    help = 'TO START NGROK TUNNEL RUN COMMAND: python manage.py start_ngrok'

    def add_arguments(self, parser):
        parser.add_argument(nargs='?', type=int, dest='port', default=8000)

    def handle(self, *args, **options):
        port = options.get('port', 8000)
        ngrok.kill()
        time.sleep(2)
        listener = ngrok.connect(port, authtoken_from_env=True)
        self.stdout.write(self.style.SUCCESS(f'Ngrok tunnel opened at: {listener.url()}'))
        try:
            while True:
                time.sleep(2)
        except KeyboardInterrupt:
            ngrok.kill()
