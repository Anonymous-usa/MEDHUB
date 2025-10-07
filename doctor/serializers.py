# doctor/serializers.py
from rest_framework import serializers
from accounts.models import User

class DoctorPublicSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id',  'email', 'phone_number', 'institution']


