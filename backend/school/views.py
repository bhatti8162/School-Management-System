
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
        
        # Attendance
        attendance = Attendance.objects.filter(student=student).values("date", "status")
        
        # Results
        results = Result.objects.filter(student=student).values("date", "test_name", "subject", "marks")
        
        # Fees
        fees = Fee.objects.filter(student=student).order_by("month")
        fee_serializer = FeeSerializer(fees, many=True)
        
        # Upcoming months
        upcoming_months = []
        current_month = date.today().replace(day=1)
        for i in range(1, 4):  # next 3 months
            month_date = current_month.replace(month=current_month.month + i if current_month.month + i <= 12 else (current_month.month + i) % 12)
            upcoming_months.append({"month": month_date, "amount": None})
        
        return Response({
            "student": StudentSerializer(student).data,
            "attendance": list(attendance),
            "results": list(results),
            "fees": fee_serializer.data,
            "upcoming_fees": upcoming_months
        })