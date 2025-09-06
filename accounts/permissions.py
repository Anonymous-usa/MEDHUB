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


from rest_framework.permissions import BasePermission

class IsInstitutionOwnerOrSuper(BasePermission):
    """
    Доступ разрешён InstitutionAdmin для своего учреждения или SuperAdmin.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user.is_authenticated:
            return False
        if user.is_super_admin() or user.is_superuser:
            return True
        if user.is_institution_admin():
            return obj.institution == user.institution
        return False

    def has_permission(self, request, view):
        # Для методов без объекта (например, PUT без retrieve)
        return request.user.is_authenticated and (
            request.user.is_super_admin() or request.user.is_superuser or request.user.is_institution_admin()
        )
