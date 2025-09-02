from rest_framework import generics, status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from .models import Notification
from .serializers import NotificationSerializer
from .permissions import IsRecipient

# 🔧 Swagger helper serializers (renamed to avoid collisions)
class NotificationMarkedCountSerializer(serializers.Serializer):
    marked_count = serializers.IntegerField()

class NotificationErrorSerializer(serializers.Serializer):
    error = serializers.CharField()


@extend_schema(
    responses={200: NotificationSerializer},
    description="Список уведомлений текущего пользователя"
)
class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Notification.objects.none()
        return (
            Notification.objects
            .select_related('actor', 'recipient')
            .filter(recipient=self.request.user)
            .order_by('-created_at')
        )


@extend_schema(
    request=None,
    responses={200: NotificationSerializer, 403: NotificationErrorSerializer, 404: NotificationErrorSerializer},
    description="Пометить одно уведомление прочитанным"
)
class NotificationMarkReadView(generics.UpdateAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsRecipient]
    queryset = Notification.objects.all()

    def patch(self, request, *args, **kwargs):
        notification = self.get_object()
        if not notification.is_read:
            notification.is_read = True
            notification.save(update_fields=['is_read', 'updated_at'])
        return Response(
            self.get_serializer(notification).data,
            status=status.HTTP_200_OK
        )


@extend_schema(
    request=None,
    responses={200: NotificationMarkedCountSerializer},
    description="Пометить все уведомления текущего пользователя прочитанными"
)
class NotificationMarkAllReadView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        qs = Notification.objects.filter(
            recipient=request.user,
            is_read=False
        )
        updated_count = qs.update(is_read=True)
        return Response(
            {"marked_count": updated_count},
            status=status.HTTP_200_OK
        )
