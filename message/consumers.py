import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from accounts.models import User
from .models import Message

logger = logging.getLogger(__name__)


class ChatConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer для чата между пользователями.
    Ограничение: чат возможен только между doctor и patient.
    """

    async def connect(self):
        user = self.scope.get("user")
        other_id = int(self.scope["url_route"]["kwargs"]["user_id"])

        # Проверка: авторизован ли пользователь и не пишет ли сам себе
        if not user or user.is_anonymous or user.id == other_id:
            logger.warning("❌ Connect rejected: invalid user or self-chat attempt")
            await self.close()
            return

        # Проверка: существует ли другой пользователь
        other_user = await self._get_user(other_id)
        if not other_user:
            logger.warning(f"❌ Connect rejected: user {other_id} not found")
            await self.close()
            return

        # Проверка ролей: только doctor ↔ patient
        roles = {user.user_type, other_user.user_type}
        if roles != {"doctor", "patient"}:
            logger.warning(f"❌ Connect rejected: invalid roles {roles}")
            await self.close()
            return

        # Создание уникальной комнаты (doctor_id, patient_id)
        a, b = sorted([user.id, other_id])
        self.room_group_name = f"chat_{a}_{b}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        logger.info(f"✅ WebSocket connected: {user} joined {self.room_group_name}")

    async def disconnect(self, close_code):
        if hasattr(self, "room_group_name"):
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
            logger.info(f"🔌 WebSocket disconnected: {self.room_group_name}")

    async def receive(self, text_data):
        """
        Получение сообщения от клиента.
        """
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            logger.error("❌ Invalid JSON received")
            return

        content = (data.get("content") or "").strip()
        if not content:
            logger.warning("⚠️ Empty message ignored")
            return

        sender = self.scope["user"]
        receiver_id = int(self.scope["url_route"]["kwargs"]["user_id"])

        if sender.id == receiver_id:
            logger.warning("⚠️ Attempt to send message to self ignored")
            return

        # Создание сообщения в БД
        msg = await self._create_message(sender.id, receiver_id, content)

        # Отправка в группу
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",  # ✅ читаемее
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


    async def chat_message(self, event):
        """
        Отправка сообщения всем участникам комнаты.
        """
        await self.send(text_data=json.dumps(event["message"]))

    # ---------------- DB helpers ---------------- #

    @database_sync_to_async
    def _get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

    @database_sync_to_async
    def _create_message(self, sender_id, receiver_id, content):
        return Message.objects.create(
            sender_id=sender_id,
            receiver_id=receiver_id,
            content=content
        )
