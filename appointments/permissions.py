from rest_framework import permissions

class IsPatient(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_patient()

class IsDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_doctor()

class IsOwnerOrDoctor(permissions.BasePermission):
    """
    Пациент может видеть и создавать свои заявки.
    Врач — видеть и обрабатывать свои входящие заявки.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_patient():
            return obj.patient_id == request.user.id
        if request.user.is_doctor():
            return obj.doctor_id == request.user.id
        return False
