from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class PhoneNumberBackend(ModelBackend):
    def authenticate(self, request, phone_number=None, password=None, **kwargs):
        if phone_number is None or password is None:
            return None
        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            return None

        if not user.check_password(password):
            return None
        if not user.is_active:
            return None
        if hasattr(user, 'is_verified') and not user.is_verified:
            return None

        return user
