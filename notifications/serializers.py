from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    """
    Сериализатор уведомлений.
    Показывает имя инициатора, строковое представление цели и тип уведомления.
    """

    actor_name = serializers.CharField(
        source="actor.get_full_name",
        read_only=True
    )
    actor_id = serializers.IntegerField(source="actor.id", read_only=True)
    target_repr = serializers.SerializerMethodField()

    @extend_schema_field(OpenApiTypes.STR)
    def get_target_repr(self, obj):
        """
        Возвращает читаемое представление связанного объекта.
        """
        return str(obj.target) if obj.target else None

    class Meta:
        model = Notification
        fields = (
            "id",
            "verb",
            "actor_id", "actor_name",
            "target_repr",
            "notification_type",   # 🔑 удобно для UI/фильтрации
            "is_read",
            "created_at", "updated_at",
        )
        read_only_fields = (
            "id",
            "verb",
            "actor_id", "actor_name",
            "target_repr",
            "notification_type",
            "created_at", "updated_at",
        )
