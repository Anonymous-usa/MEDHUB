from rest_framework import generics, status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from .models import Notification
from .serializers import NotificationSerializer
from .permissions import IsRecipient


# 🔧 Swagger helper serializers
class NotificationMarkedCountSerializer(serializers.Serializer):
    marked_count = serializers.IntegerField()


class NotificationErrorSerializer(serializers.Serializer):
    error = serializers.CharField()


@extend_schema(
    tags=["Notifications"],
    summary="Список уведомлений",
    description="Возвращает список всех уведомлений текущего пользователя. "
                "Можно фильтровать по статусу (?is_read=true/false).",
    responses={200: NotificationSerializer(many=True)},
)
class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Notification.objects.none()

        qs = Notification.objects.select_related("actor", "recipient").filter(
            recipient=self.request.user
        )

        is_read = self.request.query_params.get("is_read")
        if is_read is not None:
            qs = qs.filter(is_read=is_read.lower() in ["true", "1"])

        return qs.order_by("-created_at")


@extend_schema(
    tags=["Notifications"],
    summary="Пометить уведомление как прочитанное",
    description="Помечает одно уведомление как прочитанное. Доступно только получателю.",
    request=None,
    responses={
        200: NotificationSerializer,
        403: NotificationErrorSerializer,
        404: NotificationErrorSerializer,
    },
)
class NotificationMarkReadView(generics.UpdateAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsRecipient]
    queryset = Notification.objects.all()

    def patch(self, request, *args, **kwargs):
        notification = self.get_object()
        if not notification.is_read:
            notification.is_read = True
            notification.save(update_fields=["is_read", "updated_at"])
        return Response(
            self.get_serializer(notification).data,
            status=status.HTTP_200_OK
        )


@extend_schema(
    tags=["Notifications"],
    summary="Пометить все уведомления прочитанными",
    description="Массовая отметка всех уведомлений текущего пользователя как прочитанных.",
    request=None,
    responses={200: NotificationMarkedCountSerializer},
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
