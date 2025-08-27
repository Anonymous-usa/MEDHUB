# accounts/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    """
    Форма для создания нового пользователя в админке.
    Поля: номер телефона, тип пользователя и пароли.
    """
    class Meta:
        model = User
        fields = ('phone_number', 'user_type') 

class CustomUserChangeForm(UserChangeForm):
    """
    Форма для изменения пользователя в админке.
    Поля: номер телефона, тип, активность, суперпользователь и группы.
    """
    class Meta:
        model = User
        fields = (
            'phone_number',
            'user_type', 
            'is_active',
            'is_superuser',
            'groups',
            'user_permissions',
        )
