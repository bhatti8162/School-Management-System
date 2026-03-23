import csv
from .base import *

from ..models.student import Student
from ..serializers import StudentSerializer

class StudentViewSet(ModelViewSet):
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrAssignedSchoolUser]
    lookup_field = "GR_Id"

    def get_queryset(self):
        user_school = self.request.user.profile.school
        return Student.objects.filter(school=user_school)

    @action(detail=False, methods=["POST"])
    def import_csv(self, request):
        file = request.FILES.get("file")

        if not file:
            return Response({"error": "No file uploaded"}, status=400)

        decoded_file = file.read().decode("utf-8").splitlines()
        reader = csv.DictReader(decoded_file)

        created, updated, errors = 0, 0, []

        for i, row in enumerate(reader, start=2):
            row = {k.strip(): v for k, v in row.items()}
            gr_id = row.get("GR_Id")

            if not gr_id:
                errors.append({"row": i, "errors": "GR_Id is required"})
                continue

            try:
                obj, created_flag = Student.objects.update_or_create(
                    GR_Id=gr_id,
                    defaults={
                        "name": row.get("name"),
                        "admission_number": row.get("admission_number"),
                        "gender": row.get("gender"),
                        "city": row.get("city"),
                    },
                )

                if created_flag:
                    created += 1
                else:
                    updated += 1

            except Exception as e:
                errors.append({"row": i, "errors": str(e)})

        return Response({"created": created, "updated": updated, "errors": errors})

    @action(detail=False, methods=["GET"])
    def export_csv(self, request):
        students = self.get_queryset()  # ✅ FIXED (important)

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="students.csv"'

        writer = csv.writer(response)
        writer.writerow(["GR_Id", "name", "admission_number", "gender", "city"])

        for s in students:
            writer.writerow([s.GR_Id, s.name, s.admission_number, s.gender, s.city])

        return response