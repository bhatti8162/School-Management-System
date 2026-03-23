from .base import BaseSerializer
from ..models import Attendance

class AttendanceSerializer(BaseSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'