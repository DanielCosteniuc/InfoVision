import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import keyboard_mouse.routing  # Importă rutele WebSocket din aplicația ta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_project.settings')  # Schimbă 'my_project' cu numele tău

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            keyboard_mouse.routing.websocket_urlpatterns  # Conectează WebSocket-urile din aplicația keyboard_mouse
        )
    ),
})
