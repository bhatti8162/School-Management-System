from datetime import datetime
from django.db import transaction
from django.http import HttpResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import csv, io

from .base import *
from ..models import School, Student, ParentGuardian
from ..serializers import StudentSerializer


class StudentViewSet(ModelViewSet):
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrAssignedSchoolUser]

    def get_queryset(self):
        return Student.objects.filter(school_id=self.request.user.profile.school)

    # ---------- HELPERS ---------- #
    def parse_date(self, value, errors=None, row=None, field=None):
        value = (value or '').strip()
        if not value:
            return None
        try:
            return datetime.strptime(value, '%m/%d/%Y').date()
        except:
            if errors is not None:
                errors.append(f"Row {row}: Invalid {field} '{value}'")
            return None

    # ---------- IMPORT ---------- #
    @action(detail=False, methods=['post'])
    def import_csv(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "No file uploaded"}, status=400)

        reader = csv.DictReader(io.TextIOWrapper(file.file, encoding='utf-8'))
        errors, to_create, to_update = [], [], []
        existing_students = {s.GR_Id: s for s in Student.objects.all()}

        for i, row in enumerate(reader, 1):
            if not any(row.values()):
                continue

            gr_id = (row.get('GR_Id') or '').strip()
            school_csv_id = (row.get('school_id') or '').strip()
            parent_csv_id = (row.get('family_id') or '').strip()

            if not gr_id or not school_csv_id:
                errors.append(f"Row {i}: Missing GR_Id or school")
                continue

            school = School.objects.filter(school_id=school_csv_id).first()
            if not school:
                errors.append(f"Row {i}: Invalid school id={school_csv_id}")
                continue

            parent = ParentGuardian.objects.filter(family_id=parent_csv_id).first() if parent_csv_id else None

            dob = self.parse_date(row.get('date_of_birth'), errors, i, 'date_of_birth')
            admission_date = self.parse_date(row.get('admission_date'), errors, i, 'admission_date')

            data = {
                'school_id': school,
                'family_id': parent,
                'name': (row.get('name') or '').strip() or 'N/A',
                'gender': (row.get('gender') or '').strip() or None,
                'date_of_birth': dob,
                'age': int(row['age']) if row.get('age') else None,
                'photograph': (row.get('photograph') or '').strip() or None,
                'blood_group': (row.get('blood_group') or '').strip() or None,
                'nationality': (row.get('nationality') or '').strip() or 'N/A',
                'religion': (row.get('religion') or '').strip() or 'N/A',
                'address': (row.get('address') or '').strip() or None,
                'city': (row.get('city') or '').strip() or None,
                'state': (row.get('state') or '').strip() or None,
                'country': (row.get('country') or '').strip() or None,
                'postal_code': (row.get('postal_code') or '').strip() or None,
                'admission_number': (row.get('admission_number') or '').strip() or None,
                'admission_date': admission_date,
                'previous_school': (row.get('previous_school') or '').strip() or 'N/A',
                'transfer_certificate': (row.get('transfer_certificate') or '').strip() or None,
                'admission_class': (row.get('admission_class') or '').strip() or None,
                'section': (row.get('section') or '').strip() or None,
                'academic_year': (row.get('academic_year') or '').strip() or None,
                'admission_status': (row.get('admission_status') or '').strip() or 'active',
            }

            if gr_id in existing_students:
                student = existing_students[gr_id]
                for k, v in data.items():
                    setattr(student, k, v)
                to_update.append(student)
            else:
                to_create.append(Student(GR_Id=gr_id, **data))

        with transaction.atomic():
            if to_create:
                Student.objects.bulk_create(to_create)
            if to_update:
                Student.objects.bulk_update(to_update, fields=list(data.keys()))

        return Response({
            "created": len(to_create),
            "updated": len(to_update),
            "errors": errors
        })

    # ---------- EXPORT ---------- #
    @action(detail=False, methods=["GET"])
    def export_csv(self, request):
        students = self.get_queryset()
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="students.csv"'

        writer = csv.writer(response)
        fields = [f.name for f in students.model._meta.fields]
        writer.writerow(fields)

        for s in students:
            writer.writerow([getattr(s, f, '') for f in fields])

        return response