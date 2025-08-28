# reviews/permissions.py
from rest_framework import permissions


class IsPatient(permissions.BasePermission):
    """
    Разрешает доступ только аутентифицированному пользователю с ролью «пациент»
    для создания и просмотра собственных отзывов.
    """
    def has_permission(self, request, view) -> bool:
        return (
            request.user.is_authenticated
            and hasattr(request.user, "is_patient")
            and request.user.is_patient()
        )
