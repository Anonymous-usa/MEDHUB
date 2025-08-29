from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from accounts.forms import CustomUserCreationForm, CustomUserChangeForm
from admim_custom.admin_site import admin_site
from institutions.models import Institution, Department
from appointments.models import AppointmentRequest

User = get_user_model()

# 🔐 Админка для всех пользователей (включая врачей)
class CustomUserAdmin(DjangoUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ('phone_number', 'user_type', 'institution', 'is_active')
    list_filter = ('user_type', 'is_active', 'institution')
    ordering = ['phone_number']
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        ('Права', {'fields': ('user_type', 'institution', 'is_active', 'is_superuser')}),
        ('Группы и разрешения', {'fields': ('groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'user_type', 'institution', 'password1', 'password2'),
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            for field in ['is_superuser', 'groups', 'user_permissions']:
                if field in form.base_fields:
                    form.base_fields[field].disabled = True
        return form

admin_site.register(User, CustomUserAdmin)

# 🏥 Inline отделения
class DepartmentInline(admin.TabularInline):
    model = Department
    extra = 0
    fields = ('name', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')

# 🏥 Учреждения
@admin.register(Institution, site=admin_site)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'institution_type', 'ownership_type', 'region', 'is_top', 'is_active', 'created_at')
    list_filter = ('institution_type', 'ownership_type', 'city__region', 'is_top', 'is_active')
    search_fields = ('name', 'slug', 'city__region', 'address', 'phone', 'email')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    inlines = [DepartmentInline]
    actions = ['mark_active', 'mark_inactive', 'mark_top', 'remove_top']

    @admin.display(description="Регион")
    def region(self, obj):
        return getattr(obj.city, 'region', None) or "-"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user
        if user.is_superuser or user.is_super_admin():
            return qs
        if user.is_institution_admin():
            return qs.filter(id=user.institution_id)
        return qs.none()

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

# 🏥 Отделения
@admin.register(Department, site=admin_site)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'institution', 'created_at')
    list_filter = ('institution',)
    search_fields = ('name', 'institution__name')
    raw_id_fields = ('institution',)
    readonly_fields = ('created_at', 'updated_at')

# 📋 Заявки
@admin.register(AppointmentRequest, site=admin_site)
class AppointmentRequestAdmin(admin.ModelAdmin):
    list_display = ('get_patient_name', 'doctor', 'status', 'created_at')
    list_filter = ('status', 'doctor__institution')
    search_fields = ('patient__first_name', 'patient__last_name', 'doctor__phone_number')
    readonly_fields = ('created_at', 'updated_at')

    @admin.display(description="Пациент")
    def get_patient_name(self, obj):
        return obj.patient.get_full_name() if obj.patient else "-"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user
        if user.is_doctor():
            return qs.filter(doctor=user)
        if user.is_institution_admin():
            return qs.filter(doctor__institution=user.institution)
        if user.is_super_admin() or user.is_superuser:
            return qs
        return qs.none()

