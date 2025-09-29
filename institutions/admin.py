from django.contrib import admin
from .models import Institution, Department


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'institution_type',
        'ownership_type',
        'city',
        'region',
        'is_top',
        'is_active',
        'created_at',
    )
    list_filter = (
        'institution_type',
        'ownership_type',
        'is_top',
        'is_active',
        'city__region',
    )
    search_fields = ('name', 'slug', 'city__name', 'city__region__name')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-is_top', 'name')

    fieldsets = (
        (None, {
            'fields': (
                'name',
                'slug',
                'description',
                'institution_type',
                'ownership_type',
                'city',
                'address',
                'phone',
                'email',
                'logo',
                'is_top',
                'is_active',
            )
        }),
        ('Геолокация', {
            'fields': ('latitude', 'longitude'),
            'classes': ('collapse',),
        }),
        ('Служебная информация', {
            'fields': ('created_at', 'updated_at'),
        }),
    )


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'institution',
        'is_active',
        'created_at',
    )
    list_filter = ('institution', 'is_active')
    search_fields = ('name', 'institution__name')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('institution__name', 'name')
