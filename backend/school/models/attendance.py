from django.db import models
from .student import Student

class Attendance(models.Model):

    class Status(models.TextChoices):
        PRESENT = "present", "Present"
        ABSENT = "absent", "Absent"
        LATE = "late", "Late"
        LEAVE = "leave", "Leave"

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="attendances",
        db_index=True
    )

    date = models.DateField(db_index=True)

    status = models.CharField(
        max_length=10,
        choices=Status.choices
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["student", "date"],
                name="unique_student_attendance"
            )
        ]
