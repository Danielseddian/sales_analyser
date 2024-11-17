from django.core.management.base import BaseCommand
import uvicorn


class Command(BaseCommand):
    help = "Run the ASGI server"

    def add_arguments(self, parser):
        parser.add_argument('--host', type=str, default='0.0.0.0', help='Host address')
        parser.add_argument('--port', type=int, default=8000, help='Port number')

    def handle(self, *args, **kwargs):
        host = kwargs.get('host', '0.0.0.0')
        port = kwargs.get('port', 8000)
        uvicorn.run("settings.asgi:application", host=host, port=port)
