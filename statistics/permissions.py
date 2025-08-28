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
            and request.user.is_super_admin()
        )


class IsInstitutionOwnerOrSuper(permissions.BasePermission):
    """
    Доступ для супер-админа или администратора своего учреждения.
    """
    def has_permission(self, request, view) -> bool:
        # Супер-админ — всегда можно
        if (
            request.user.is_authenticated
            and hasattr(request.user, "is_super_admin")
            and request.user.is_super_admin()
        ):
            return True

        # Админ учреждения — общий доступ (проверка объекта в has_object_permission)
        if (
            request.user.is_authenticated
            and hasattr(request.user, "is_institution_admin")
            and request.user.is_institution_admin()
        ):
            return True

        return False

    def has_object_permission(self, request, view, obj) -> bool:
        # Супер-админ — всегда можно
        if (
            hasattr(request.user, "is_super_admin")
            and request.user.is_super_admin()
        ):
            return True

        # Только админ своего учреждения
        return (
            hasattr(request.user, "is_institution_admin")
            and request.user.is_institution_admin()
            and getattr(request.user, "institution_id", None) == getattr(obj, "id", None)
        )
