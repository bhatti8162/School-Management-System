
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Admin, Student, Attendance, Result, Fee
from .serializers import (
    AdminSerializer,
    StudentSerializer,
    AttendanceSerializer,
    ResultSerializer,
    FeeSerializer
)


class AdminViewSet(ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer


class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class AttendanceViewSet(ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer


class ResultViewSet(ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer


class FeeViewSet(ModelViewSet):
    queryset = Fee.objects.all()
    serializer_class = FeeSerializer

class StudentSummaryViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = "name"

    def retrieve(self, request, name=None):
        student = Student.objects.get(name=name)
        

        attendance = Attendance.objects.filter(student=student).values(
            "date", "status"
        )

        results = Result.objects.filter(student=student).values(
            "date","test_name","subject", "marks"
        )

        fees = Fee.objects.filter(student=student).values(
            "month", "amount"
        )

        data = {
            "student": student.name,
            "admin": student.admin.name,
            "class_name": student.class_name,
            "attendance": list(attendance),
            "results": list(results),
            "fees": list(fees),
        }

        return Response(data)