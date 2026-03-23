from .base import *

from ..models.student import Student
from ..models.attendance import Attendance
from ..models.result import Result
from ..models.fee import Fee

from ..serializers import StudentSerializer, FeeSerializer

class StudentSummaryViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    lookup_field = "name"

    def retrieve(self, request, name=None):
        student = Student.objects.get(name=name)

        attendance = Attendance.objects.filter(student=student).values("date", "status")
        results = Result.objects.filter(student=student).values("date", "test_name", "subject", "marks")

        fees = Fee.objects.filter(student=student).order_by("month")
        fee_serializer = FeeSerializer(fees, many=True)

        return Response({
            "student": StudentSerializer(student).data,
            "attendance": list(attendance),
            "results": list(results),
            "fees": fee_serializer.data,
        })