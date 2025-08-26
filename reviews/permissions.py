from rest_framework import permissions

class IsPatient(permissions.BasePermission):
    """
    Только аутентифицированный пациент может оставлять и смотреть свои отзывы.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_patient()
