from .base import BaseSerializer
from ..models import Student
from rest_framework import serializers

class StudentSerializer(BaseSerializer):
    family_id = serializers.CharField(source="parent_guardian.family_id", read_only=True)
    school_id = serializers.CharField(source="parent_guardian.school.school_id", read_only=True) 
    school_name = serializers.CharField(source="parent_guardian.school.name", read_only=True) 

    class Meta:
        model = Student
        exclude = ['id'] 