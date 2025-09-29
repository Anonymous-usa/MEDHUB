from django.contrib import admin
from .models import AppointmentRequest


@admin.register(AppointmentRequest)
class AppointmentRequestAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'patient',
        'doctor',
        'status',
        'appointment_time',
        'is_active',
        'created_at',
    )
    list_filter = ('status', 'is_active', 'created_at', 'updated_at')
    search_fields = (
        'patient__username',
        'patient__phone_number',
        'doctor__username',
        'doctor__phone_number',
    )
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': ('patient', 'doctor', 'note', 'status', 'appointment_time', 'is_active')
        }),
        ('Служебная информация', {
            'fields': ('created_at', 'updated_at'),
        }),
    )
