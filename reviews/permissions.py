from rest_framework import permissions


class IsPatient(permissions.BasePermission):
    """
    Доступ разрешён только аутентифицированным пользователям с ролью «пациент».
    Используется для создания и просмотра собственных отзывов.
    """

    def has_permission(self, request, view) -> bool:
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and hasattr(user, "is_patient")
            and callable(user.is_patient)
            and user.is_patient()
        )

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Дополнительно ограничиваем доступ к объекту:
        пациент может работать только со своими отзывами.
        """
        user = request.user
        return (
            self.has_permission(request, view)
            and hasattr(obj, "appointment")
            and obj.appointment.patient_id == user.id
        )
