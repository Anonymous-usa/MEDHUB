from rest_framework import permissions


class IsRecipient(permissions.BasePermission):
    """
    Доступ только к уведомлениям,
    получателем которых является текущий аутентифицированный пользователь.
    """

    def has_permission(self, request, view) -> bool:
        # Общая проверка: пользователь должен быть аутентифицирован
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj) -> bool:
        # Проверка на уровне конкретного объекта
        return getattr(obj, "recipient_id", None) == request.user.id
