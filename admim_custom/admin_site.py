# from django.contrib.admin import AdminSite
# from django.utils.translation import gettext_lazy as _
# from django.urls import path
# from django.template.response import TemplateResponse
# from django.contrib import admin
# from appointments.models import AppointmentRequest
# from institutions.models import Department, Institution
# from accounts.models import User
# from reviews.models import Review
# from django.http import HttpResponseForbidden

# #  Кастомная админ-панель
# class MedhubAdminSite(AdminSite):
#     site_header = _("MEDHUB.TJ Админ-панель")
#     site_title = _("MEDHUB.TJ")
#     index_title = _("Управление медицинскими учреждениями")

#     def get_urls(self):
#         urls = super().get_urls()
#         custom_urls = [
#             path("dashboard/", self.admin_view(self.dashboard_view), name="dashboard"),
#         ]
#         return custom_urls + urls
#     # Представление dashboard
#     def dashboard_view(self, request):
#         if not request.user.is_superuser and not request.user.is_institution_admin():
#             return HttpResponseForbidden("Нет доступа к дашборду.")
#         stats = {
#             "appointments_total": AppointmentRequest.objects.count(),
#             "appointments_accepted": AppointmentRequest.objects.filter(status="accepted").count(),
#             "appointments_pending": AppointmentRequest.objects.filter(status="pending").count(),
#             "appointments_rejected": AppointmentRequest.objects.filter(status="rejected").count(),
#             "institutions_total": Institution.objects.count(),
#             "doctors_total": User.objects.filter(user_type="worker").count(),
#             "reviews_total": Review.objects.count(),
#         }
#         context = dict(self.each_context(request), stats=stats)
#         return TemplateResponse(request, "admim_custom/dashboard.html", context)

# admin_site = MedhubAdminSite(name='medhub_admin')

# # Кастомная админка для пользователей
# from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

# class CustomUserAdmin(DjangoUserAdmin):
#     list_display = ('phone_number', 'user_type', 'institution', 'is_active')
#     list_filter = ('user_type', 'is_active', 'institution')
#     ordering = ['phone_number']
#     fieldsets = (
#         (None, {'fields': ('phone_number', 'password')}),
#         ('Права', {'fields': ('user_type', 'institution', 'is_active', 'is_superuser')}),
#         ('Группы и разрешения', {'fields': ('groups', 'user_permissions')}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('phone_number', 'user_type', 'institution', 'password1', 'password2'),
#         }),
#     )

#     def get_form(self, request, obj=None, **kwargs):
#         form = super().get_form(request, obj, **kwargs)
#         if not request.user.is_superuser:
#             for field in ['is_superuser', 'groups', 'user_permissions']:
#                 if field in form.base_fields:
#                     form.base_fields[field].disabled = True
#         return form

#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         user = request.user
#         if user.is_superuser or user.is_super_admin():
#             return qs
#         if user.is_institution_admin():
#             return qs.filter(institution=user.institution)
#         return qs.none()


# admin_site.register(User, CustomUserAdmin)

# # Inline отображение отделений внутри учреждения
# class DepartmentInline(admin.TabularInline):
#     model = Department
#     extra = 0
#     fields = ('name', 'created_at', 'updated_at')
#     readonly_fields = ('created_at', 'updated_at')



# # Админка для учреждений
# @admin.register(Institution, site=admin_site)
# class InstitutionAdmin(admin.ModelAdmin):
#     list_display = ('name', 'institution_type', 'ownership_type', 'region', 'is_top', 'is_active', 'created_at')
#     list_filter = ('institution_type', 'ownership_type', 'city__region', 'is_top', 'is_active')
#     search_fields = ('name', 'slug', 'city__region', 'address', 'phone', 'email')
#     prepopulated_fields = {'slug': ('name',)}
#     readonly_fields = ('created_at', 'updated_at')
#     inlines = [DepartmentInline]
#     actions = ['mark_active', 'mark_inactive', 'mark_top', 'remove_top']


#     # Отображение региона
#     @admin.display(description="Регион")
#     def region(self, obj):
#         return getattr(obj.city, 'region', None) or "-"
    
#     # Ограничиваем доступ к учреждениям
#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         user = request.user
#         if user.is_superuser or user.is_super_admin():
#             return qs
#         if user.is_institution_admin():
#             return qs.filter(id=user.institution_id)
#         return qs.none()


#     # Действия
#     def mark_active(self, request, queryset):
#         updated = queryset.update(is_active=True)
#         self.message_user(request, f"{updated} учреждений активированы.")
#     mark_active.short_description = "Отметить как активные"

#     def mark_inactive(self, request, queryset):
#         updated = queryset.update(is_active=False)
#         self.message_user(request, f"{updated} учреждений деактивированы.")
#     mark_inactive.short_description = "Отметить как неактивные"

#     def mark_top(self, request, queryset):
#         updated = queryset.update(is_top=True)
#         self.message_user(request, f"{updated} учреждений помечены ТОП.")
#     mark_top.short_description = "Пометить как ТОП"

#     def remove_top(self, request, queryset):
#         updated = queryset.update(is_top=False)
#         self.message_user(request, f"{updated} учреждений убраны из ТОП.")
#     remove_top.short_description = "Убрать из ТОП"


# @admin.register(Department, site=admin_site)
# class DepartmentAdmin(admin.ModelAdmin):
#     list_display = ('name', 'institution', 'created_at')
#     list_filter = ('institution',)
#     search_fields = ('name', 'institution__name')
#     raw_id_fields = ('institution',)
#     readonly_fields = ('created_at', 'updated_at')

#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         user = request.user
#         if user.is_superuser or user.is_super_admin():
#             return qs
#         if user.is_institution_admin():
#             return qs.filter(institution=user.institution)
#         return qs.none()

# #  Админка для заявок
# @admin.register(AppointmentRequest, site=admin_site)
# class AppointmentRequestAdmin(admin.ModelAdmin):
#     list_display = ('get_patient_name', 'doctor', 'status', 'created_at')
#     list_filter = ('status', 'doctor__institution')
#     search_fields = ('patient__first_name', 'patient__last_name', 'doctor__phone_number')
#     readonly_fields = ('created_at', 'updated_at')


#     # Отображение имени пациента
#     @admin.display(description="Пациент")
#     def get_patient_name(self, obj):
#         return obj.patient.get_full_name() if obj.patient else "-"
    

#     # Ограничиваем доступ к заявкам
#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         user = request.user
#         if user.is_doctor():
#             return qs.filter(doctor=user)
#         if user.is_institution_admin():
#             return qs.filter(doctor__institution=user.institution)
#         if user.is_super_admin() or user.is_superuser:
#             return qs
#         return qs.none()



