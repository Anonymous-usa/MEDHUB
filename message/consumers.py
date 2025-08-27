# message/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]
        other_id = int(self.scope["url_route"]["kwargs"]["user_id"])

        # неавторизованным — отказ
        if user.is_anonymous:
            await self.close()
            return

        # формируем уникальное имя комнаты
        a, b = sorted([user.id, other_id])
        self.room_group_name = f"chat_{a}_{b}"

        # подписываемся на группу и даём коннект
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        content = data.get("content", "").strip()
        if not content:
            return

        sender = self.scope["user"]
        receiver_id = int(self.scope["url_route"]["kwargs"]["user_id"])

        # сохраняем в БД
        msg = await self._create_message(sender.id, receiver_id, content)

        # рассылка события группе
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

    async def chat_message(self, event):
        # отсылаем JSON всем участникам
        await self.send(text_data=json.dumps(event["message"]))

    @database_sync_to_async
    def _create_message(self, sender_id, receiver_id, content):
        return Message.objects.create(
            sender_id=sender_id,
            receiver_id=receiver_id,
            content=content
        )
