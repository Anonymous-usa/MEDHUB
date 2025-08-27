"""
Django admin customization for the custom User model using phone number as the unique identifier.

This file defines the CustomUserAdmin class, which configures the Django admin
interface for the CustomUser model, replacing `username` with `phone_number`.
It includes logical field grouping, refined list display and filter options,
full search support, and robust docstring/documentation.

Best practices from the Django documentation and experienced community sources are
incorporated to maximize admin usability and maintainability.

Author: [Your Name/Team]
Created: 2025-08-27
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import DateFieldListFilter
from django.utils.translation import gettext_lazy as _

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class UserTypeListFilter(admin.SimpleListFilter):
    """
    Custom admin list filter for User Type.

    This filter enables intuitive segmentation of users by their user_type.
    """
    title = _('user type')
    parameter_name = 'user_type'

    def lookups(self, request, model_admin):
        # Returns a list of tuples (value, human_readable_name)
        return CustomUser.USER_TYPE_CHOICES

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(user_type=self.value())
        return queryset


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Admin interface for CustomUser with phone_number as USERNAME_FIELD.

    Configures fieldsets for logical grouping, optimized list_display,
    search, and filtering. Uses custom forms for user creation/change.
    """

    # Use the custom forms referencing the custom user model
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    # Fields to display in the admin list view for CustomUser
    list_display = (
        'phone_number', 'email', 'first_name', 'last_name',
        'user_type', 'institution', 'is_active', 'is_staff', 'date_of_birth',
    )

    # Filter options in the sidebar of the user change list view
    list_filter = (
        UserTypeListFilter,           # Custom filter for user_type
        'institution',                # Allows filtering by institution
        ('date_of_birth', DateFieldListFilter),  # Filter by date_of_birth
        'is_staff', 'is_active',
    )

    # Enable searching by phone_number, email, first/last name, institution name
    search_fields = (
        'phone_number',
        'email',
        'first_name',
        'last_name',
        'institution__name',  # if institution is a FK to another model
    )

    # Group fields into sections for readability and admin usability
    fieldsets = (
        (_('Login Credentials'), {
            'fields': ('phone_number', 'password'),
        }),
        (_('Personal Info'), {
            'fields': ('first_name', 'last_name', 'email', 'date_of_birth'),
        }),
        (_('Profile'), {
            'fields': ('user_type', 'institution'),
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important Dates'), {
            'fields': ('last_login', 'date_joined'),
        }),
    )

    # Fieldsets for the Add User page - uses password1/2, excludes last_login/date_joined
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'phone_number',
                'first_name', 'last_name', 'email', 'date_of_birth',
                'user_type', 'institution',
                'password1', 'password2',
                'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'
            ),
        }),
    )

    ordering = ('phone_number',)
    filter_horizontal = ('groups', 'user_permissions')
    readonly_fields = ()
    # readonly_fields could include 'last_login', 'date_joined' if you want these non-editable

    def get_fieldsets(self, request, obj=None):
        """
        Return the fieldsets to use in the admin form.
        """
        return super().get_fieldsets(request, obj)

    def get_add_fieldsets(self, request):
        """
        Return the fieldsets to use on the add user form.
        """
        return self.add_fieldsets

    def get_queryset(self, request):
        """
        Return the QuerySet used by the admin; override to filter users as needed.
        """
        return super().get_queryset(request)


# If CustomUser is not AbstractUser-based (e.g., AbstractBaseUser), additional
# admin tweaks may be needed for handling groups/permissions/date fields.

# End of accounts/admin.py
