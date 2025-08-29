from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
from appointments.models import AppointmentRequest
from accounts.models import User
from institutions.models import Department, Institution
from reviews.models import Review

@staff_member_required
def dashboard_view(request):
    stats = {
        'appointments_total': AppointmentRequest.objects.count(),
        'appointments_accepted': AppointmentRequest.objects.filter(status='accepted').count(),
        'appointments_pending': AppointmentRequest.objects.filter(status='pending').count(),
        'appointments_rejected': AppointmentRequest.objects.filter(status='rejected').count(),
        'institutions_total': Institution.objects.count(),
        'reviews_total': Review.objects.count(),
        'doctors_total': User.objects.filter(user_type='worker').count(),
    }
    return render(request, 'admim_custom/dashboard.html', {'stats': stats})

@staff_member_required
def institutions_view(request):
    region = request.GET.get('region')
    institutions = Institution.objects.all()
    if region:
        institutions = institutions.filter(city__region__icontains=region)
    paginator = Paginator(institutions, 20)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'admim_custom/institutions.html', {'page_obj': page_obj})

@staff_member_required
def institution_detail_view(request, institution_id):
    institution = get_object_or_404(Institution, id=institution_id)
    departments = Department.objects.filter(institution=institution)
    doctors = User.objects.filter(institution=institution, user_type='worker')
    appointments = AppointmentRequest.objects.filter(doctor__institution=institution)
    reviews = Review.objects.filter(appointment__doctor__institution=institution)
    context = {
        'institution': institution,
        'departments': departments,
        'doctors': doctors,
        'appointments': appointments,
        'reviews': reviews,
    }
    return render(request, 'admim_custom/institution_detail.html', context)

@staff_member_required
def doctors_view(request):
    institution_id = request.GET.get('institution')
    doctors = User.objects.filter(user_type='worker').select_related('institution')
    if institution_id:
        doctors = doctors.filter(institution_id=institution_id)
    paginator = Paginator(doctors, 25)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'admim_custom/doctors.html', {'page_obj': page_obj})

@staff_member_required
def my_institution_view(request):
    institution = request.user.institution
    departments = Department.objects.filter(institution=institution)
    doctors = User.objects.filter(institution=institution, user_type='worker')
    appointments = AppointmentRequest.objects.filter(doctor__institution=institution)
    reviews = Review.objects.filter(appointment__doctor__institution=institution)
    context = {
        'institution': institution,
        'departments': departments,
        'doctors': doctors,
        'appointments': appointments,
        'reviews': reviews,
    }
    return render(request, 'admim_custom/my_institution.html', context)

@staff_member_required
def my_appointments_view(request):
    appointments = AppointmentRequest.objects.filter(doctor__institution=request.user.institution)
    return render(request, 'admim_custom/my_appointments.html', {'appointments': appointments})

@staff_member_required
def my_reviews_view(request):
    reviews = Review.objects.filter(appointment__doctor__institution=request.user.institution)
    return render(request, 'admim_custom/my_reviews.html', {'reviews': reviews})

@staff_member_required
def my_requests_view(request):
    appointments = AppointmentRequest.objects.filter(doctor=request.user)
    return render(request, 'admim_custom/my_requests.html', {'appointments': appointments})
