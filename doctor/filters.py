# doctor/filters.py
import django_filters
from accounts.models import User

class DoctorFilter(django_filters.FilterSet):
    institution = django_filters.NumberFilter(field_name='institution_id')

    class Meta:
        model = User
        fields = ['institution']
