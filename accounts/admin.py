# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .models import User

# @admin.register(User)
# class CustomUserAdmin(UserAdmin):
#     list_display = ('phone_number', 'email', 'first_name', 'last_name', 
#                    'user_type', 'is_staff', 'is_active')
#     list_filter = ('user_type', 'is_staff', 'is_active')
#     search_fields = ('phone_number', 'email', 'first_name', 'last_name')
    
#     fieldsets = (
#         (None, {'fields': ('phone_number', 'password')}),
#         ('Personal info', {'fields': ('first_name', 'last_name', 'email', 
#                                      'date_of_birth', 'user_type')}),
#         ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
#                                    'groups', 'user_permissions')}),
#         ('Important dates', {'fields': ('last_login', 'date_joined')}),
#         ('Institution', {'fields': ('institution',)}),
#     )
    
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('phone_number', 'email', 'password1', 'password2',
#                       'first_name', 'last_name', 'user_type')}
#         ),
#     )
    
#     ordering = ('phone_number',)