from rest_framework import permissions

class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'super_admin'

class IsInstitutionAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'institution_admin'

class IsDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'doctor'

class IsInstitutionStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.institution is not None

class IsOwnInstitution(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Для объектов, у которых есть связь с учреждением
        if hasattr(obj, 'institution'):
            return obj.institution == request.user.institution
        return False