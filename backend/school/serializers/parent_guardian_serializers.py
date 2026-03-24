from .base import BaseSerializer
from ..models import ParentGuardian
from rest_framework import serializers

class ParentGuardianSerializer(BaseSerializer):

    class Meta:
        model = ParentGuardian
        fields = '__all__'
        lookup_field = 'family_id'