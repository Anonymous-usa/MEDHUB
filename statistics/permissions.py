from rest_framework import permissions

class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_super_admin()

class IsInstitutionOwnerOrSuper(permissions.BasePermission):
    def has_permission(self, request, view):
        # super-admin всегда может
        if request.user.is_authenticated and request.user.is_super_admin():
            return True
        # админ института может свой
        if request.user.is_authenticated and request.user.is_institution_admin():
            return True
        return False

    def has_object_permission(self, request, view, obj):
        # super-admin всегда может
        if request.user.is_super_admin():
            return True
        # только админ своего учреждения
        return (
            request.user.is_institution_admin() 
            and request.user.institution_id == obj.id
        )
