from rest_framework import permissions
from accounts.models import User  # adjust if needed

class IsPatient(permissions.BasePermission):
    """
    Доступ для пациентов и супер-админов.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and (
                request.user.is_patient() or
                request.user.user_type == User.UserType.SUPERUSER
            )
        )


class IsDoctor(permissions.BasePermission):
    """
    Доступ для врачей и супер-админов (контроллеров).
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and (
                request.user.is_doctor() or
                request.user.user_type == User.UserType.SUPERUSER
            )
        )


class IsSuperAdmin(permissions.BasePermission):
    """
    Доступ только для супер-администраторов системы.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and (
                request.user.is_super_admin() or
                request.user.user_type == User.UserType.SUPERUSER
            )
        )


class IsOwnerOrDoctor(permissions.BasePermission):
    """
    Пациент может видеть и управлять только своими заявками.
    Врач — видеть и обрабатывать только свои входящие заявки.
    Супер-админ — имеет полный доступ.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.user_type == User.UserType.SUPERUSER:
            return True  # 🔥 супер-админ имеет полный доступ

        if request.user.is_patient():
            return obj.patient_id == request.user.id

        if request.user.is_doctor():
            return obj.doctor_id == request.user.id

        return False
