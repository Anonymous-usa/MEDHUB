from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    actor_name      = serializers.CharField(source='actor.get_full_name', read_only=True)
    target_repr     = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = (
            'id', 'verb', 'actor_name', 'target_repr',
            'is_read', 'created_at'
        )
        read_only_fields = ('id', 'verb', 'actor_name', 'target_repr', 'created_at')

    def get_target_repr(self, obj):
        return str(obj.target) if obj.target else None
