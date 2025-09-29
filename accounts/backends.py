from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class PhoneNumberBackend(ModelBackend):
    """
    Аутентификация по phone_number вместо username.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        phone = kwargs.get('phone_number') or username
        if not phone or not password:
            return None
        try:
            user = User.objects.get(phone_number=phone)
        except User.DoesNotExist:
            return None
        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
