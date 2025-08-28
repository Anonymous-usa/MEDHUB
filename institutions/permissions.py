# institutions/permissions.py
from rest_framework import permissions


class IsSuperAdmin(permissions.BasePermission):
    """
    Только супер-админ может создавать/удалять любые учреждения.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and hasattr(request.user, 'is_super_admin')
            and request.user.is_super_admin()
        )


class IsInstitutionOwnerOrSuper(permissions.BasePermission):
    """
    Админ учреждения может редактировать своё учреждение,
    супер-админ — любое.
    """
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        # Супер-админ имеет доступ ко всем учреждениям
        if hasattr(request.user, 'is_super_admin') and request.user.is_super_admin():
            return True

        # Админ учреждения — только к своему
        return (
            hasattr(request.user, 'is_institution_admin')
            and request.user.is_institution_admin()
            and getattr(request.user, 'institution_id', None) == obj.id
        )
