from django.db.models import Q
from rest_framework import generics, permissions, status, views, serializers
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from django.utils.translation import gettext_lazy as _
from accounts.models import User
from .models import Message
from .serializers import MessageSerializer
import logging

logger = logging.getLogger(__name__)


# 🔧 Swagger helper serializers
class MessageStatusSerializer(serializers.Serializer):
    status = serializers.CharField()


class MessageErrorSerializer(serializers.Serializer):
    error = serializers.CharField()


@extend_schema(
    tags=["Messages"],
    summary="Список диалогов",
    description="Возвращает список последних сообщений в диалогах текущего пользователя. "
                "Для каждой уникальной пары (sender, receiver) берётся только последнее сообщение.",
    responses={200: MessageSerializer(many=True)},
)
class DialogListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Message.objects.none()

        user = self.request.user
        messages = Message.objects.filter(Q(sender=user) | Q(receiver=user))

        latest_by_pair = {}
        for msg in messages:
            pair = tuple(sorted([msg.sender_id, msg.receiver_id]))
            if pair not in latest_by_pair or msg.created_at > latest_by_pair[pair].created_at:
                latest_by_pair[pair] = msg

        return sorted(latest_by_pair.values(), key=lambda m: m.created_at, reverse=True)


@extend_schema_view(
    get=extend_schema(
        tags=["Messages"],
        summary="История переписки",
        description="Возвращает историю сообщений между текущим пользователем и другим пользователем.",
        parameters=[
            OpenApiParameter(
                name="user_id",
                location=OpenApiParameter.PATH,
                required=True,
                type=int,
                description="ID второго пользователя в чате"
            )
        ],
        responses={200: MessageSerializer(many=True)},
    ),
    post=extend_schema(
        tags=["Messages"],
        summary="Отправить сообщение",
        description="Отправка нового сообщения другому пользователю. "
                    "Чат разрешён только между доктором и пациентом.",
        request=MessageSerializer,
        responses={201: MessageSerializer, 400: MessageErrorSerializer},
    )
)
class ChatView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Message.objects.none()

        user = self.request.user
        other_user_id: int = self.kwargs['user_id']

        return (
            Message.objects
            .select_related("sender", "receiver")
            .filter(
                Q(sender=user, receiver_id=other_user_id) |
                Q(sender_id=other_user_id, receiver=user)
            )
            .order_by("created_at")
        )

    def perform_create(self, serializer):
        other_user_id = self.kwargs['user_id']

        if other_user_id == self.request.user.id:
            raise ValidationError(_("Нельзя отправить сообщение самому себе"))

        try:
            other_user = User.objects.get(id=other_user_id)
        except User.DoesNotExist:
            raise ValidationError(_("Получатель не найден"))

        roles = {self.request.user.user_type, other_user.user_type}
        if roles != {"doctor", "patient"}:
            raise ValidationError(_("Чат разрешён только между доктором и пациентом"))

        instance = serializer.save(sender=self.request.user, receiver=other_user)
        logger.info(f"Сообщение отправлено {instance.sender} → {instance.receiver}")


@extend_schema(
    tags=["Messages"],
    summary="Пометить сообщение как прочитанное",
    description="Помечает сообщение как прочитанное, если оно адресовано текущему пользователю.",
    request=None,
    responses={200: MessageStatusSerializer, 404: MessageErrorSerializer},
)
class MarkAsReadView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk: int):
        try:
            message = Message.objects.get(pk=pk, receiver=request.user)
            message.is_read = True
            message.status = Message.MessageStatus.READ
            message.save(update_fields=["is_read", "status"])
            logger.info(f"Сообщение {pk} помечено как прочитанное пользователем {request.user}")
            return Response({"status": "read"}, status=status.HTTP_200_OK)
        except Message.DoesNotExist:
            return Response({"error": "Message not found"}, status=status.HTTP_404_NOT_FOUND)
