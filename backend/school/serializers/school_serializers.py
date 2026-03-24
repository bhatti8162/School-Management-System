from .base import BaseSerializer
from ..models import School

class SchoolSerializer(BaseSerializer):
    class Meta:
        model = School
        fields = '__all__'
        lookup_field = 'school_id'