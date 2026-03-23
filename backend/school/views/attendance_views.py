from .base import *

from ..models.attendance import Attendance
from ..serializers import AttendanceSerializer


class AttendanceViewSet(ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer