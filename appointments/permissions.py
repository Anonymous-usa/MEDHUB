from rest_framework import permissions


class IsPatient(permissions.BasePermission):
    """
    Доступ только для аутентифицированных пациентов.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_patient()


class IsDoctor(permissions.BasePermission):
    """
    Доступ только для аутентифицированных врачей.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_doctor()


class IsSuperAdmin(permissions.BasePermission):
    """
    Доступ только для супер-администраторов системы.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_super_admin()


class IsOwnerOrDoctor(permissions.BasePermission):
    """
    Пациент может видеть и управлять только своими заявками.
    Врач — видеть и обрабатывать только свои входящие заявки.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_patient():
            return obj.patient_id == request.user.id
        if request.user.is_doctor():
            return obj.doctor_id == request.user.id
        if request.user.is_super_admin():
            return True  # 🔥 супер-админ имеет полный доступ
        return False
