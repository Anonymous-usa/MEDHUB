from rest_framework.permissions import BasePermission

class IsSuperAdmin(BasePermission):
    """
    Доступ только для пользователей с ролью SUPER_ADMIN.
    """

    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.user_type == 'super_admin'
        )
