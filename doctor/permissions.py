# doctor/permissions.py
from rest_framework.permissions import BasePermission

class CanDeleteDoctor(BasePermission):
    """
    Разрешает удаление врача супер-админу или администратору учреждения,
    но только если врач принадлежит той же организации.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_super_admin() or request.user.is_institution_admin()
        )

    def has_object_permission(self, request, view, obj):
        if not obj.is_doctor():
            return False

        if request.user.is_super_admin():
            return True

        # Админ может удалять только врачей из своей организации
        return obj.institution_id == request.user.institution_id
