from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'phone_number', 'email', 'user_type', 'institution', 'is_super_admin_flag')
    list_filter = ('user_type', 'institution', 'is_super_admin_flag',)
    search_fields = ('username', 'phone_number', 'email', 'first_name', 'last_name')
    readonly_fields = ('last_login', 'date_joined')
