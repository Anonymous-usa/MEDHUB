from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes
from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отправки и получения сообщений.
    Отправитель определяется автоматически из request.user.
    """

    sender_name = serializers.SerializerMethodField()
    receiver_name = serializers.SerializerMethodField()

    @extend_schema_field(OpenApiTypes.STR)
    def get_sender_name(self, obj):
        return obj.sender.get_full_name() if obj.sender else None

    @extend_schema_field(OpenApiTypes.STR)
    def get_receiver_name(self, obj):
        return obj.receiver.get_full_name() if obj.receiver else None

    class Meta:
        model = Message
        fields = [
            'id',
            'sender', 'sender_name',
            'receiver', 'receiver_name',
            'content',
            'created_at', 'updated_at',
            'is_read', 'status', 'attachment'
        ]
        read_only_fields = [
            'id', 'created_at', 'updated_at',
            'sender', 'sender_name', 'receiver_name',
            'status'
        ]

    def validate(self, attrs):
        sender = self.context['request'].user
        receiver = attrs.get('receiver')

        if not receiver:
            raise serializers.ValidationError(_("Не указан получатель"))

        if sender.id == receiver.id:
            raise serializers.ValidationError(_("Нельзя отправить сообщение самому себе"))

        roles = {sender.user_type, receiver.user_type}
        if roles != {"doctor", "patient"}:
            raise serializers.ValidationError(_("Чат разрешён только между доктором и пациентом"))

        return attrs

    def create(self, validated_data):
        validated_data['sender'] = self.context['request'].user
        return super().create(validated_data)
