from .base import BaseSerializer
from ..models import ParentGuardian
from rest_framework import serializers

class ParentGuardianSerializer(BaseSerializer):
    school_id = serializers.CharField(source="school.school_id", read_only=True) 

    class Meta:
        model = ParentGuardian
        fields = '__all__'