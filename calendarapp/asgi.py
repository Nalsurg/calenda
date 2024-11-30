
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'calendarapp.settings')

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from schedule.consumers import EventConsumer

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path("ws/events/", EventConsumer.as_asgi()),
        ])
    ),
})
