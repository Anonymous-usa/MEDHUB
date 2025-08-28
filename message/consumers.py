# message/consumers.py
import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.core.exceptions import PermissionDenied
from .models import Message

logger = logging.getLogger(__name__)


class ChatConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer для приватного чата между двумя пользователями.
    """
    async def connect(self) -> None:
        user = self.scope.get("user")
        other_id = int(self.scope["url_route"]["kwargs"]["user_id"])

        # Отказ неавторизованным
        if not user or user.is_anonymous:
            await self.close()
            return

        # Запретить соединение с самим собой
        if user.id == other_id:
            await self.close()
            return

        # Уникальное имя комнаты — комбинация ID пользователей в порядке возрастания
        a, b = sorted([user.id, other_id])
        self.room_group_name = f"chat_{a}_{b}"

        # Подписываемся на группу и даём коннект
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        logger.info(f"WS connected: user {user.id} → room {self.room_group_name}")

    async def disconnect(self, close_code: int) -> None:
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        logger.info(f"WS disconnected: {self.scope['user'].id} from {self.room_group_name}")

    async def receive(self, text_data: str) -> None:
        """
        Обрабатывает входящее сообщение от клиента.
        """
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            logger.warning("Invalid JSON received over WS")
            return

        content = (data.get("content") or "").strip()
        if not content:
            return  # Игнор пустых сообщений

        sender = self.scope["user"]
        receiver_id = int(self.scope["url_route"]["kwargs"]["user_id"])

        # Запрет на отправку самому себе
        if sender.id == receiver_id:
            raise PermissionDenied("Нельзя отправить сообщение самому себе")

        # Сохраняем в БД
        msg = await self._create_message(sender.id, receiver_id, content)

        # Рассылаем событие всем участникам чата
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat.message",
                "message": {
                    "id": msg.id,
                    "sender": sender.id,
                    "receiver": receiver_id,
                    "content": content,
                    "created_at": msg.created_at.isoformat(),
                    "is_read": msg.is_read,
                }
            }
        )

    async def chat_message(self, event: dict) -> None:
        """
        Отправляет сообщение всем клиентам, подписанным на комнату.
        """
        await self.send(text_data=json.dumps(event["message"]))

    @database_sync_to_async
    def _create_message(self, sender_id: int, receiver_id: int, content: str) -> Message:
        """
        Создаёт запись в базе данных для нового сообщения.
        """
        msg = Message.objects.create(
            sender_id=sender_id,
            receiver_id=receiver_id,
            content=content
        )
        logger.info(f"Message {msg.id} saved: {sender_id} → {receiver_id}")
        return msg
