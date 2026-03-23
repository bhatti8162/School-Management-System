import csv
import io
from datetime import datetime
from .base import *

from ..models import School, Student, ParentGuardian, Teacher, Result, Fee
from ..serializers import StudentSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import HttpResponse


class StudentViewSet(ModelViewSet):
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrAssignedSchoolUser]
    lookup_field = "GR_Id"

    def get_queryset(self):
        user_school = self.request.user.profile.school
        return Student.objects.filter(school=user_school)

    @action(detail=False, methods=['post'])
    def import_csv(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "No file uploaded"}, status=400)

        decoded_file = io.TextIOWrapper(file.file, encoding='utf-8')
        reader = csv.DictReader(decoded_file)  # comma-separated CSV

        created_count = 0
        updated_count = 0
        errors = []

        for row_number, row in enumerate(reader, start=1):
            # Skip empty rows
            if not any(row.values()):
                print(f"[DEBUG] Skipping empty row {row_number}")
                continue

            try:
                print(f"[DEBUG] Processing row {row_number}: {row}")

                # Lookup school
                school_instance = None
                if row.get('school'):
                    try:
                        school_instance = School.objects.get(id=row['school'])
                    except School.DoesNotExist:
                        errors.append(f"Row {row_number}: School id={row.get('school')} not found")
                        continue
                else:
                    errors.append(f"Row {row_number}: Missing school id")
                    continue

                # Lookup parent (optional)
                parent_instance = None
                if row.get('parent_guardian'):
                    try:
                        parent_instance = ParentGuardian.objects.get(id=row['parent_guardian'])
                    except ParentGuardian.DoesNotExist:
                        errors.append(f"Row {row_number}: Parent id={row.get('parent_guardian')} not found")
                        parent_instance = None

                # Parse dates to YYYY-MM-DD
                date_of_birth = None
                admission_date = None
                dob_str = row.get('date_of_birth', '').replace('“','').replace('”','')
                admission_str = row.get('admission_date', '').replace('“','').replace('”','')

                if dob_str:
                    try:
                        date_of_birth = datetime.strptime(dob_str, '%m/%d/%Y').date()
                    except Exception as e:
                        errors.append(f"Row {row_number}: Invalid date_of_birth '{dob_str}'")
                        date_of_birth = None

                if admission_str:
                    try:
                        admission_date = datetime.strptime(admission_str, '%m/%d/%Y').date()
                    except Exception as e:
                        errors.append(f"Row {row_number}: Invalid admission_date '{admission_str}'")
                        admission_date = None

                # Update or create student
                student, created = Student.objects.update_or_create(
                    GR_Id=row['GR_Id'],
                    defaults={
                        'school': school_instance,
                        'parent_guardian': parent_instance,
                        'name': row.get('name', ''),
                        'gender': row.get('gender', ''),
                        'date_of_birth': date_of_birth,
                        'age': row.get('age') or None,
                        'photograph': row.get('photograph', ''),
                        'blood_group': row.get('blood_group', ''),
                        'nationality': row.get('nationality', ''),
                        'religion': row.get('religion', ''),
                        'address': row.get('address', ''),
                        'city': row.get('city', ''),
                        'state': row.get('state', ''),
                        'country': row.get('country', ''),
                        'postal_code': row.get('postal_code', ''),
                        'admission_number': row.get('admission_number', ''),
                        'admission_date': admission_date,
                        'previous_school': row.get('previous_school', ''),
                        'transfer_certificate': row.get('transfer_certificate', ''),
                        'admission_class': row.get('admission_class', ''),
                        'section': row.get('section', ''),
                        'academic_year': row.get('academic_year', ''),
                        'admission_status': row.get('admission_status', ''),
                    }
                )

                if created:
                    created_count += 1
                    print(f"[DEBUG] Created student {student.GR_Id}")
                else:
                    updated_count += 1
                    print(f"[DEBUG] Updated student {student.GR_Id}")

            except Exception as e:
                error_msg = f"Row {row_number}, GR_Id={row.get('GR_Id')}: {e}"
                errors.append(error_msg)
                print(f"[ERROR] {error_msg}")

        return Response({
            "created": created_count,
            "updated": updated_count,
            "errors": errors
        })

    @action(detail=False, methods=["GET"])
    def export_csv(self, request):
        students = self.get_queryset()

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="students.csv"'

        writer = csv.writer(response)
        field_names = [field.name for field in students.model._meta.fields]
        writer.writerow(field_names)

        for s in students:
            row = [getattr(s, field, '') for field in field_names]
            writer.writerow(row)

        return response