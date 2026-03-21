from rest_framework import viewsets, serializers
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.apps import apps
from django.db.models import Q
from datetime import date


from .permissions import IsSuperAdminOrAssignedSchoolUser 

from .models.parent_guardian import ParentGuardian
from .models.student import Student
from .models.school import School
from .models.attendance import Attendance
from .models.admission import Admission
from .models.teacher import Teacher
from .models.result import Result
from .models.fee import Fee
from .serializers import (
    SchoolSerializer,
    AttendanceSerializer,
    ParentGuardianSerializer,
    StudentSerializer,
    AdmissionSerializer,
    TeacherSerializer,
    ResultSerializer,
    FeeSerializer,
)

class SchoolViewSet(ModelViewSet):
    serializer_class = SchoolSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrAssignedSchoolUser]

    def get_queryset(self):
        user = self.request.user
        profile = user.profile

        # Superadmin sees all schools
        if profile.role == "superadmin":
            return School.objects.all()

        # School user sees only their assigned school
        if profile.role == "school" and profile.school:
            return School.objects.filter(id=profile.school.id)

        # If no school assigned, return empty queryset
        return School.objects.none()

    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        Returns the logged-in user's school
        Superadmin sees all schools
        """
        user = request.user
        profile = user.profile

        if profile.role == "superadmin":
            queryset = School.objects.all()
            serializer = self.get_serializer(queryset, many=True)
        else:
            school = profile.school
            if not school:
                return Response({"detail": "No school assigned"}, status=404)
            serializer = self.get_serializer(school)
        return Response(serializer.data)

class ParentGuardianViewSet(ModelViewSet):
    queryset = ParentGuardian.objects.all()
    serializer_class = ParentGuardianSerializer
    lookup_field = "family_id"


class StudentViewSet(ModelViewSet):
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrAssignedSchoolUser ]
    lookup_field = "GR_id"

    def get_queryset(self):
        # Only return students from the user's assigned school
        user_school = self.request.user.profile.school
        return Student.objects.filter(school=user_school)


class AdmissionViewSet(ModelViewSet):
    queryset = Admission.objects.all()
    serializer_class = AdmissionSerializer
    lookup_field = "admission_number"


class TeacherViewSet(ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


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
            month_number = (current_month.month + i - 1) % 12 + 1
            month_year = current_month.year + ((current_month.month + i - 1) // 12)
            month_date = current_month.replace(year=month_year, month=month_number)
            upcoming_months.append({"month": month_date, "amount": None})

        return Response({
            "student": StudentSerializer(student).data,
            "attendance": list(attendance),
            "results": list(results),
            "fees": fee_serializer.data,
            "upcoming_fees": upcoming_months
        })


class UniversalSearchViewSet(viewsets.ViewSet):
    """
    Universal search for any model.
    URL: /api/search/<model_name>/?q=<keyword>
    """

    def get_model_by_name(self, model_name):
        """
        Search all installed apps for a model by name (case-insensitive)
        """
        for app_config in apps.get_app_configs():
            for name, model in app_config.models.items():
                if name.lower() == model_name.lower():
                    return model
        return None

    @action(detail=False, methods=['get'], url_path=r'(?P<model_name>\w+)')
    def search(self, request, model_name=None):
        keyword = request.query_params.get("q")
        if not keyword:
            return Response({"error": "Please provide a search keyword using ?q="}, status=400)

        model = self.get_model_by_name(model_name)
        if not model:
            return Response({"error": f"Model '{model_name}' not found."}, status=400)

        text_fields = [f.name for f in model._meta.get_fields() if f.get_internal_type() in ('CharField', 'TextField')]
        if not text_fields:
            return Response({"error": f"No searchable fields found in '{model_name}'."}, status=400)

        query = Q()
        for field in text_fields:
            query |= Q(**{f"{field}__icontains": keyword})

        results = model.objects.filter(query)

        def get_api_url(self, obj):
            return f"/api/{model_name.lower()}/{obj.pk}/"

        serializer_class = type(
            f"{model_name}DynamicSerializer",
            (serializers.ModelSerializer,),
            {
                "Meta": type("Meta", (), {"model": model, "fields": [f.name for f in model._meta.fields] + ["api_url"]}),
                "get_api_url": get_api_url,
                "api_url": serializers.SerializerMethodField()
            }
        )

        serializer = serializer_class(results, many=True)
        return Response(serializer.data)

    def list(self, request):
        try:
            school_app = apps.get_app_config('school')
            model_list = list(school_app.models.keys())
        except LookupError:
            model_list = []

        return Response({
            "Example": "Please provide a model name in the URL, e.g. /api/search/Student/?q=John",
            "available_models": model_list
        })