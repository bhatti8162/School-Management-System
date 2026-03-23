from .base import *
from ..models.teacher import Teacher
from ..serializers import TeacherSerializer

class TeacherViewSet(ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer