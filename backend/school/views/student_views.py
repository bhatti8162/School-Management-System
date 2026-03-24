import csv, io
from datetime import datetime
from django.db import transaction
from django.http import HttpResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .base import *
from ..models import School, Student, ParentGuardian
from ..serializers import StudentSerializer


class StudentViewSet(ModelViewSet):
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrAssignedSchoolUser]
    lookup_field = "GR_Id"

    def get_queryset(self):
        return Student.objects.filter(school=self.request.user.profile.school)

    # ---------- HELPERS ---------- #

    def clean_text(self, v):
        return str(v).strip() if v and str(v).strip() else None

    def clean_int(self, v, errors, row, field):
        try:
            return int(v) if v else None
        except:
            errors.append(f"Row {row}: Invalid {field}")
            return None

    def parse_date(self, v, errors, row, field):
        try:
            return datetime.strptime(v.strip(), '%m/%d/%Y').date() if v else None
        except:
            errors.append(f"Row {row}: Invalid {field}")
            return None

    # ---------- IMPORT ---------- #
    @action(detail=False, methods=['post'])
    def import_csv(self, request):
        file = request.FILES.get('file')
        if not file:
            print("[ERROR] No file uploaded")
            return Response({"error": "No file uploaded"}, status=400)

        print("[INFO] CSV import started")

        reader = csv.DictReader(io.TextIOWrapper(file.file, encoding='utf-8'))

        errors, to_create, to_update = [], [], []
        existing = {s.GR_Id: s for s in Student.objects.all()}

        print(f"[INFO] Existing students loaded: {len(existing)}")

        for i, row in enumerate(reader, 1):
            print(f"\n[ROW {i}] Raw data: {row}")

            if not any(row.values()):
                print(f"[ROW {i}] Skipped (empty row)")
                continue

            try:
                gr_id = self.clean_text(row.get('GR_Id'))
                school_id = self.clean_text(row.get('school'))

                print(f"[ROW {i}] GR_Id: {gr_id}, School: {school_id}")

                if not gr_id or not school_id:
                    msg = f"Row {i}: Missing GR_Id or school"
                    print(f"[ROW {i}] ERROR: {msg}")
                    errors.append(msg)
                    continue

                school = School.objects.filter(id=school_id).first()
                if not school:
                    msg = f"Row {i}: Invalid school id={school_id}"
                    print(f"[ROW {i}] ERROR: {msg}")
                    errors.append(msg)
                    continue

                parent_id = self.clean_text(row.get('parent_guardian'))
                parent = ParentGuardian.objects.filter(id=parent_id).first() if parent_id else None
                print(f"[ROW {i}] Parent: {parent_id} -> {parent}")

                # Dates (DOB and admission can now be None)
                dob = self.parse_date(row.get('date_of_birth'), errors, i, 'date_of_birth')
                if not dob:
                    print(f"[ROW {i}] WARNING: Missing DOB → saving as None")
                admission_date = self.parse_date(row.get('admission_date'), errors, i, 'admission_date')
                if not admission_date:
                    print(f"[ROW {i}] INFO: Missing admission_date → saving as None")

                data = {
                    'school': school,
                    'parent_guardian': parent,
                    'name': self.clean_text(row.get('name')),
                    'gender': self.clean_text(row.get('gender')),
                    'date_of_birth': dob,
                    'age': self.clean_int(row.get('age'), errors, i, 'age'),
                    'blood_group': self.clean_text(row.get('blood_group')),
                    'nationality': self.clean_text(row.get('nationality')),
                    'religion': self.clean_text(row.get('religion')),
                    'address': self.clean_text(row.get('address')),
                    'city': self.clean_text(row.get('city')),
                    'state': self.clean_text(row.get('state')),
                    'country': self.clean_text(row.get('country')),
                    'postal_code': self.clean_text(row.get('postal_code')),
                    'admission_number': self.clean_text(row.get('admission_number')),
                    'admission_date': admission_date,
                    'previous_school': self.clean_text(row.get('previous_school')),
                    'admission_class': self.clean_text(row.get('admission_class')),
                    'section': self.clean_text(row.get('section')),
                    'academic_year': self.clean_text(row.get('academic_year')),
                    'admission_status': self.clean_text(row.get('admission_status')),
                }

                print(f"[ROW {i}] Cleaned data: {data}")

                if gr_id in existing:
                    print(f"[ROW {i}] Updating existing student")
                    student = existing[gr_id]
                    for k, v in data.items():
                        setattr(student, k, v)
                    to_update.append(student)
                else:
                    print(f"[ROW {i}] Creating new student")
                    to_create.append(Student(GR_Id=gr_id, **data))

            except Exception as e:
                msg = f"Row {i}: {str(e)}"
                print(f"[ROW {i}] EXCEPTION: {msg}")
                errors.append(msg)

        print("\n[INFO] Processing complete")
        print(f"[INFO] To Create: {len(to_create)}")
        print(f"[INFO] To Update: {len(to_update)}")
        print(f"[INFO] Errors: {len(errors)}")

        # ---------------- SAVE ---------------- #
        with transaction.atomic():
            if to_create:
                Student.objects.bulk_create(to_create)
                print(f"[DB] Created {len(to_create)} students")
            if to_update:
                Student.objects.bulk_update(to_update, fields=list(data.keys()))
                print(f"[DB] Updated {len(to_update)} students")

        total_students = Student.objects.count()
        print(f"[DB] Total students in DB: {total_students}")

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