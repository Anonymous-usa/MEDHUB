# # message/views.py
# from django.db.models import Q, Max
# from rest_framework import generics, permissions, status, views
# from rest_framework.response import Response
# from .models import Message
# from .serializers import MessageSerializer
# import logging

# logger = logging.getLogger(__name__)


# class DialogListView(generics.ListAPIView):
#     """
#     Список последних сообщений в диалогах пользователя.
#     Показывает по одному последнему сообщению на каждую уникальную пару.
#     """
#     serializer_class = MessageSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user

#         # Получаем время последнего сообщения для каждой пары
#         dialogs = (
#             Message.objects.filter(Q(sender=user) | Q(receiver=user))
#             .values("sender", "receiver")
#             .annotate(last_message=Max("created_at"))
#         )

#         # Строим фильтр по последним сообщениям
#         q = Q()
#         for d in dialogs:
#             q |= Q(created_at=d["last_message"])

#         return (
#             Message.objects
#             .select_related("sender", "receiver")
#             .filter(q)
#             .order_by("-created_at")
#         )


# class ChatView(generics.ListCreateAPIView):
#     """
#     История переписки между текущим пользователем и другим пользователем.
#     """
#     serializer_class = MessageSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         other_user_id = self.kwargs['user_id']

#         return (
#             Message.objects
#             .select_related("sender", "receiver")
#             .filter(
#                 Q(sender=user, receiver_id=other_user_id) |
#                 Q(sender_id=other_user_id, receiver=user)
#             )
#             .order_by("created_at")
#         )

#     def perform_create(self, serializer):
#         other_user_id = self.kwargs['user_id']
#         if other_user_id == self.request.user.id:
#             raise ValueError("Нельзя отправить сообщение самому себе")
#         instance = serializer.save(sender=self.request.user, receiver_id=other_user_id)
#         logger.info(f"Сообщение отправлено {instance.sender} → {instance.receiver}")


# class MarkAsReadView(views.APIView):
#     """
#     Отмечает сообщение как прочитанное, если оно адресовано текущему пользователю.
#     """
#     permission_classes = [permissions.IsAuthenticated]

#     def patch(self, request, pk):
#         try:
#             message = Message.objects.get(pk=pk, receiver=request.user)
#             message.is_read = True
#             message.save(update_fields=["is_read"])
#             logger.info(f"Сообщение {pk} помечено как прочитанное пользователем {request.user}")
#             return Response({"status": "read"}, status=status.HTTP_200_OK)
#         except Message.DoesNotExist:
#             return Response({"error": "Message not found"}, status=status.HTTP_404_NOT_FOUND)


from django.db.models import Q, Max
from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from accounts.models import User
from .models import Message
from .serializers import MessageSerializer
import logging

logger = logging.getLogger(__name__)

class DialogListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        messages = Message.objects.filter(Q(sender=user) | Q(receiver=user))
        latest_by_pair = {}
        for msg in messages:
            pair = tuple(sorted([msg.sender_id, msg.receiver_id]))
            if pair not in latest_by_pair or msg.created_at > latest_by_pair[pair].created_at:
                latest_by_pair[pair] = msg
        return sorted(latest_by_pair.values(), key=lambda m: m.created_at, reverse=True)

class ChatView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        other_user_id = self.kwargs['user_id']
        return Message.objects.select_related("sender", "receiver").filter(
            Q(sender=user, receiver_id=other_user_id) |
            Q(sender_id=other_user_id, receiver=user)
        ).order_by("created_at")

    def perform_create(self, serializer):
        other_user_id = self.kwargs['user_id']
        if other_user_id == self.request.user.id:
            raise ValidationError(_("Нельзя отправить сообщение самому себе"))
        other_user = User.objects.get(id=other_user_id)
        roles = {self.request.user.user_type, other_user.user_type}
        if roles != {"doctor", "patient"}:
            raise ValidationError(_("Чат разрешён только между доктором и пациентом"))
        serializer.save(sender=self.request.user, receiver=other_user)

class MarkAsReadView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        try:
            message = Message.objects.get(pk=pk, receiver=request.user)
            message.is_read = True
            message.save(update_fields=["is_read"])
            return Response({"status": "read"}, status=status.HTTP_200_OK)
        except Message.DoesNotExist:
            return Response({"error": "Message not found"}, status=status.HTTP_404_NOT_FOUND)
