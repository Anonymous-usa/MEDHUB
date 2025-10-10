from rest_framework.permissions import BasePermission
from accounts.models import User  # adjust import if needed

class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view) -> bool:
        return (
            request.user.is_authenticated and (
                request.user.is_super_admin() or
                request.user.user_type == User.UserType.SUPERUSER
            )
        )

class IsInstitutionAdmin(BasePermission):
    def has_permission(self, request, view) -> bool:
        return (
            request.user.is_authenticated and (
                request.user.is_institution_admin() or
                request.user.user_type == User.UserType.SUPERUSER
            )
        )

class IsDoctor(BasePermission):
    def has_permission(self, request, view) -> bool:
        return (
            request.user.is_authenticated and (
                request.user.is_doctor() or
                request.user.user_type == User.UserType.SUPERUSER
            )
        )

class IsPatient(BasePermission):
    def has_permission(self, request, view) -> bool:
        return (
            request.user.is_authenticated and (
                request.user.is_patient() or
                request.user.user_type == User.UserType.SUPERUSER
            )
        )
