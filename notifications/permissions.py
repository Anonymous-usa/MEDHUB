# notification/permissions.py
from rest_framework import permissions


class IsRecipient(permissions.BasePermission):
    """
    Разрешает доступ только к уведомлениям,
    получателем которых является текущий аутентифицированный пользователь.
    """
    def has_object_permission(self, request, view, obj) -> bool:
        return (
            request.user.is_authenticated
            and hasattr(obj, 'recipient_id')
            and obj.recipient_id == request.user.id
        )
