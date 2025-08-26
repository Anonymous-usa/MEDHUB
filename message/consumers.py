
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from accounts.models import User
from channels.db import database_sync_to_async
from .models import Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]           # текущий юзер
        self.other_user_id = self.scope["url_route"]["kwargs"]["user_id"]
        self.room_name = f"chat_{min(self.user.id, int(self.other_user_id))}_{max(self.user.id, int(self.other_user_id))}"
        self.room_group_name = f"chat_{self.room_name}"

        # Подключаемся к группе
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]

        # сохраняем сообщение в БД
        msg = await self.save_message(self.user.id, self.other_user_id, message)

        # шлём его в группу
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender": self.user.id,
                "receiver": self.other_user_id,
                "created_at": str(msg.created_at),
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender": event["sender"],
            "receiver": event["receiver"],
            "created_at": event["created_at"],
        }))

    @database_sync_to_async
    def save_message(self, sender_id, receiver_id, content):
        return Message.objects.create(sender_id=sender_id, receiver_id=receiver_id, content=content)