from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _
from django.urls import path
from django.template.response import TemplateResponse
from appointments.models import AppointmentRequest
from institutions.models import Institution
from accounts.models import User
from reviews.models import Review

class MedhubAdminSite(AdminSite):
    site_header = _("MEDHUB.TJ Админ-панель")
    site_title = _("MEDHUB.TJ")
    index_title = _("Управление медицинскими учреждениями")

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("dashboard/", self.admin_view(self.dashboard_view), name="dashboard"),
        ]
        return custom_urls + urls

    def dashboard_view(self, request):
        stats = {
            "appointments_total": AppointmentRequest.objects.count(),
            "appointments_accepted": AppointmentRequest.objects.filter(status="accepted").count(),
            "appointments_pending": AppointmentRequest.objects.filter(status="pending").count(),
            "appointments_rejected": AppointmentRequest.objects.filter(status="rejected").count(),
            "institutions_total": Institution.objects.count(),
            "doctors_total": User.objects.filter(user_type="worker").count(),
            "reviews_total": Review.objects.count(),
        }
        context = dict(self.each_context(request), stats=stats)
        return TemplateResponse(request, "admim_custom/dashboard.html", context)

admin_site = MedhubAdminSite(name='medhub_admin')
