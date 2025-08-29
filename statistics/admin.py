from statistics.models import StatisticRecord
from django.contrib import admin

# If you have a custom admin site, import or define it here. Otherwise, use the default admin.site.
admin_site = admin.site

@admin.register(StatisticRecord, site=admin_site)
class StatisticRecordAdmin(admin.ModelAdmin):
    list_display = ('metric', 'value', 'period_start', 'period_end', 'target')
    list_filter = ('metric', 'period_start', 'period_end')
    search_fields = ('metric',)
    readonly_fields = ('created_at', 'updated_at')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
