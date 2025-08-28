# notification/serializers.py
from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    """
    Сериализатор уведомлений.
    Показывает имя инициатора и строковое представление цели.
    """
    actor_name = serializers.CharField(
        source='actor.get_full_name',
        read_only=True
    )
    actor_id = serializers.IntegerField(source='actor.id', read_only=True)
    target_repr = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = (
            'id',
            'verb',
            'actor_id', 'actor_name',
            'target_repr',
            'is_read',
            'created_at', 'updated_at'
        )
        read_only_fields = (
            'id', 'verb',
            'actor_id', 'actor_name',
            'target_repr',
            'created_at', 'updated_at'
        )

    def get_target_repr(self, obj):
        """
        Возвращает читаемое представление связанного объекта.
        """
        return str(obj.target) if obj.target else None
