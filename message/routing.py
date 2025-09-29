# message/routing.py
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    # 📩 WebSocket для чата
    path("ws/messages/<int:chat_id>/", consumers.ChatConsumer.as_asgi()),
]
