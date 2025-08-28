from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    """
    Форма для создания нового пользователя в админке.
    Поля: номер телефона, тип пользователя, учреждение и пароли.
    """
    class Meta:
        model = User
        fields = ('phone_number', 'user_type', 'institution', 'is_verified')

    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get('user_type')
        institution = cleaned_data.get('institution')

        if user_type in [User.UserType.DOCTOR, User.UserType.INSTITUTION_ADMIN] and not institution:
            raise forms.ValidationError("Доктор и администратор учреждения должны быть привязаны к учреждению.")
        if user_type == User.UserType.PATIENT and institution:
            raise forms.ValidationError("Пациент не должен быть привязан к учреждению.")
        return cleaned_data


class CustomUserChangeForm(UserChangeForm):
    """
    Форма для изменения пользователя в админке.
    Поля: номер телефона, тип, учреждение, активность, верификация, суперпользователь и группы.
    """
    class Meta:
        model = User
        fields = (
            'phone_number',
            'user_type',
            'institution',
            'is_active',
            'is_verified',
            'is_superuser',
            'groups',
            'user_permissions',
        )

    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get('user_type')
        institution = cleaned_data.get('institution')

        if user_type in [User.UserType.DOCTOR, User.UserType.INSTITUTION_ADMIN] and not institution:
            raise forms.ValidationError("Доктор и администратор учреждения должны быть привязаны к учреждению.")
        if user_type == User.UserType.PATIENT and institution:
            raise forms.ValidationError("Пациент не должен быть привязан к учреждению.")
        return cleaned_data
