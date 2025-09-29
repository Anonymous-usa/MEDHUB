# statistics/permissions.py
from rest_framework import permissions


class IsSuperAdmin(permissions.BasePermission):
    """
    Доступ только для аутентифицированных супер-администраторов.
    """
    def has_permission(self, request, view) -> bool:
        return (
            request.user.is_authenticated
            and hasattr(request.user, "is_super_admin")
            and callable(request.user.is_super_admin)
            and request.user.is_super_admin()
        )


class IsInstitutionOwnerOrSuper(permissions.BasePermission):
    """
    Доступ для супер-админа или администратора своего учреждения.
    Проверка объекта идёт по полю `institution_id`.
    """
    def has_permission(self, request, view) -> bool:
        user = request.user
        if not user.is_authenticated:
            return False

        # Супер-админ — всегда можно
        if hasattr(user, "is_super_admin") and user.is_super_admin():
            return True

        # Админ учреждения — общий доступ (детальнее в has_object_permission)
        if hasattr(user, "is_institution_admin") and user.is_institution_admin():
            return True

        return False

    def has_object_permission(self, request, view, obj) -> bool:
        user = request.user
        if not user.is_authenticated:
            return False

        # Супер-админ — всегда можно
        if hasattr(user, "is_super_admin") and user.is_super_admin():
            return True

        # Только админ своего учреждения
        return (
            hasattr(user, "is_institution_admin")
            and user.is_institution_admin()
            and getattr(user, "institution_id", None) == getattr(obj, "id", None)
        )
