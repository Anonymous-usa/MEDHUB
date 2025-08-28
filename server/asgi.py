# server/asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from message.routing import websocket_urlpatterns  # ✅ прямой импорт для читаемости

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    # HTTP requests → стандартное Django ASGI приложение
    "http": django_asgi_app,

    # WebSocket → через Channels с аутентификацией
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})
