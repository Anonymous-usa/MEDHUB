# institutions/permissions.py
from rest_framework import permissions

class IsSuperAdmin(permissions.BasePermission):
    """
    Только супер-админ может создавать/удалять любые учреждения.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
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
        if request.user.is_super_admin():
            return True
        return (
            request.user.is_institution_admin()
            and request.user.institution_id == obj.id
        )
