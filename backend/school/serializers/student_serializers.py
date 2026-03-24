from .base import BaseSerializer
from ..models import Student
from rest_framework import serializers

class StudentSerializer(BaseSerializer):

    class Meta:
        model = Student
        fields = '__all__'
        lookup_field = 'GR_Id'