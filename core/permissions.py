from rest_framework import permissions

class IsSuperAdmin(permissions.BasePermission):
    """
    Доступ только для супер-админов (госорганов).
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_super_admin()


class IsInstitutionAdmin(permissions.BasePermission):
    """
    Доступ только для администраторов учреждений.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_institution_admin()


class IsDoctor(permissions.BasePermission):
    """
    Доступ только для врачей.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_doctor()


class IsInstitutionStaff(permissions.BasePermission):
    """
    Доступ для всех сотрудников, привязанных к учреждению.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.institution is not None


class IsOwnInstitution(permissions.BasePermission):
    """
    Доступ к объектам, связанным с учреждением пользователя.
    """
    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated and
            hasattr(obj, 'institution') and
            obj.institution == request.user.institution
        )
