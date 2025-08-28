# admin_custom/views.py
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, render
from appointments.models import AppointmentRequest
from accounts.models import User
from institutions.models import Department, Institution
from reviews.models import Review
from django.core.paginator import Paginator



@staff_member_required
def institutions_view(request):
    if not request.user.is_super_admin():
        return render(request, '403.html')

    region = request.GET.get('region')
    institutions = Institution.objects.all()
    if region:
        institutions = institutions.filter(region__icontains=region)

    paginator = Paginator(institutions, 20)  # < = 20 учреждений на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'institutions.html', {'page_obj': page_obj})


@staff_member_required
def dashboard_view(request):
    if not request.user.is_super_admin():
        return render(request, '403.html')

    stats = {
        'appointments_total': AppointmentRequest.objects.count(),
        'appointments_accepted': AppointmentRequest.objects.filter(status='accepted').count(),
        'appointments_pending': AppointmentRequest.objects.filter(status='pending').count(),
        'appointments_rejected': AppointmentRequest.objects.filter(status='rejected').count(),
        'institutions_total': Institution.objects.count(),
        'reviews_total': Review.objects.count(),
        'doctors_total': User.objects.filter(user_type='doctor').count(),
    }

    return render(request, 'dashboard.html', {'stats': stats})


@staff_member_required
def doctors_view(request):
    if not request.user.is_super_admin():
        return render(request, '403.html')

    institution_id = request.GET.get('institution')
    doctors = User.objects.filter(user_type='doctor').select_related('institution')
    if institution_id:
        doctors = doctors.filter(institution_id=institution_id)

    paginator = Paginator(doctors, 25)  # < = 25 врачей на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'doctors.html', {'page_obj': page_obj})


@staff_member_required
def institution_detail_view(request, institution_id):
    if not request.user.is_super_admin():
        return render(request, '403.html')

    institution = get_object_or_404(Institution, id=institution_id)
    departments = Department.objects.filter(institution=institution)
    doctors = User.objects.filter(institution=institution, user_type='doctor')
    appointments = AppointmentRequest.objects.filter(doctor__institution=institution)
    reviews = Review.objects.filter(appointment__doctor__institution=institution)

    context = {

        'institution': institution,
        'departments': departments,
        'doctors': doctors,
        'appointments': appointments,
        'reviews': reviews,

    }

    return render(request, 'institution_detail.html', context)



@staff_member_required
def my_institution_view(request):
    if not request.user.is_institution_admin():
        return render(request, '403.html')

    institution = request.user.institution
    departments = Department.objects.filter(institution=institution)
    doctors = User.objects.filter(institution=institution, user_type='doctor')
    appointments = AppointmentRequest.objects.filter(doctor__institution=institution)
    reviews = Review.objects.filter(appointment__doctor__institution=institution)

    context = {
        'institution': institution,
        'departments': departments,
        'doctors': doctors,
        'appointments': appointments,
        'reviews': reviews,
    }
    return render(request, 'my_institution.html', context)


@staff_member_required
def my_appointments_view(request):
    if not request.user.is_institution_admin():
        return render(request, '403.html')

    appointments = AppointmentRequest.objects.filter(doctor__institution=request.user.institution)
    return render(request, 'my_appointments.html', {'appointments': appointments})


@staff_member_required
def my_reviews_view(request):
    if not request.user.is_institution_admin():
        return render(request, '403.html')

    reviews = Review.objects.filter(appointment__doctor__institution=request.user.institution)
    return render(request, 'my_reviews.html', {'reviews': reviews})
