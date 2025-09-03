from django import forms
from .models import Institution, Department

class InstitutionForm(forms.ModelForm):
    class Meta:
        model = Institution
        fields = [
            'name', 'slug', 'institution_type', 'ownership_type',
             'city', 'address', 'phone', 'email',
            'description', 'is_active', 'is_top'
        ]


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'institution', 'description']
