from accounts.forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.admin import AdminSite

#custom admin site
class MedhubAdminSite(AdminSite):
    site_header = 'Medhub Admin'
    site_title  = 'Medhub'
    index_title = 'Администрирование'

admin_site = MedhubAdminSite(name='medhub_admin')

User = get_user_model()

#customuser
class CustomUserAdmin(DjangoUserAdmin):
    add_form      = CustomUserCreationForm
    form          = CustomUserChangeForm
    list_display  = ('phone_number', 'user_type', 'is_active')
    list_filter   = ('user_type', 'is_active')
    ordering      = ['phone_number']  
    fieldsets     = (
        (None, {'fields': ('phone_number', 'password')}),
        ('Права', {'fields': ('user_type', 'is_active', 'is_superuser')}),
        ('Группы и разрешения', {'fields': ('groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'user_type', 'password1', 'password2'),
        }),
    )

admin_site.register(User, CustomUserAdmin)




#department and institution
from django.contrib import admin
from admin_custom.admin import admin_site
from institutions.models import Institution, Department


class DepartmentInline(admin.TabularInline):
    model = Department
    extra = 0
    fields = ('name', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Institution, site=admin_site)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'institution_type',
        'ownership_type',
        'region',
        'is_top',
        'is_active',
        'created_at',
    )
    list_filter = (
        'institution_type',
        'ownership_type',
        'region',
        'is_top',
        'is_active',
    )
    search_fields = (
        'name',
        'slug',
        'region',
        'address',
        'phone',
        'email',
    )
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    inlines = [DepartmentInline]
    actions = [
        'mark_active',
        'mark_inactive',
        'mark_top',
        'remove_top',
    ]

    def mark_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} учреждений активированы.")
    mark_active.short_description = "Отметить как активные"

    def mark_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} учреждений деактивированы.")
    mark_inactive.short_description = "Отметить как неактивные"

    def mark_top(self, request, queryset):
        updated = queryset.update(is_top=True)
        self.message_user(request, f"{updated} учреждений помечены ТОП.")
    mark_top.short_description = "Пометить как ТОП"

    def remove_top(self, request, queryset):
        updated = queryset.update(is_top=False)
        self.message_user(request, f"{updated} учреждений убраны из ТОП.")
    remove_top.short_description = "Убрать из ТОП"


@admin.register(Department, site=admin_site)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'institution', 'created_at')
    list_filter = ('institution',)
    search_fields = ('name', 'institution__name')
    raw_id_fields = ('institution',)
    readonly_fields = ('created_at', 'updated_at')

