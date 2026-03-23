from .base import BaseSerializer
from ..models import Teacher

class TeacherSerializer(BaseSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'