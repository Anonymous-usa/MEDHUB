from rest_framework import permissions

class IsRecipient(permissions.BasePermission):
    """
    Пользователь может работать только со своими уведомлениями.
    """
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj.recipient_id == request.user.id
