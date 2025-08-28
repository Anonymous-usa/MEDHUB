# message/routing.py
from django.urls import re_path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    # WebSocket для приватного чата между пользователями
    re_path(
        r"^ws/chat/(?P<user_id>\d+)/$",
        ChatConsumer.as_asgi(),
        name="private_chat_ws"
    ),
]
