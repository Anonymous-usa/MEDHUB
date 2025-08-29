from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отправки и получения сообщений.
    Отправитель определяется автоматически из request.user.
    """
    sender_name = serializers.CharField(source='sender.get_full_name', read_only=True)
    receiver_name = serializers.CharField(source='receiver.get_full_name', read_only=True)

    class Meta:
        model = Message
        fields = [
            'id',
            'sender', 'sender_name',
            'receiver', 'receiver_name',
            'content',
            'created_at', 'updated_at',
            'is_read'
        ]
        read_only_fields = [
            'id', 'created_at', 'updated_at',
            'sender', 'sender_name', 'receiver_name'
        ]

    def validate(self, attrs):
        sender = self.context['request'].user
        receiver = attrs.get('receiver')
        roles = {sender.user_type, receiver.user_type}
        if roles != {"doctor", "patient"}:
            raise serializers.ValidationError(_("Чат разрешён только между доктором и пациентом"))
        return attrs

    def create(self, validated_data):
        validated_data['sender'] = self.context['request'].user
        return super().create(validated_data)
