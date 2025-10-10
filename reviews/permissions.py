from rest_framework import permissions
from accounts.models import User  # adjust import if needed

class IsPatient(permissions.BasePermission):
    """
    Доступ разрешён для пациентов и супер-админов.
    Используется для создания и просмотра собственных отзывов.
    """

    def has_permission(self, request, view) -> bool:
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and (
                (hasattr(user, "is_patient") and callable(user.is_patient) and user.is_patient()) or
                user.user_type == User.UserType.SUPERUSER
            )
        )

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Пациент может работать только со своими отзывами.
        Супер-админ имеет доступ ко всем отзывам.
        """
        user = request.user
        if user.user_type == User.UserType.SUPERUSER:
            return True

        return (
            self.has_permission(request, view)
            and hasattr(obj, "appointment")
            and obj.appointment.patient_id == user.id
        )
