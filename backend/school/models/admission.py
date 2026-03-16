from django.db import models
from .student import Student

class Admission(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("inactive", "Inactive"),
        ("pending", "Pending"),
        ("withdrawn", "Withdrawn"),
    ]
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    admission_number = models.CharField(max_length=50, unique=True)
    admission_date = models.DateField()
    previous_school = models.CharField(max_length=100, blank=True, null=True)
    transfer_certificate = models.FileField(upload_to='admissions/tc/', blank=True, null=True)
    admission_class = models.CharField(max_length=50)
    section = models.CharField(max_length=20)
    roll_number = models.CharField(max_length=20)
    academic_year = models.CharField(max_length=20)
    admission_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")

    def __str__(self):
        return f"{self.admission_number} - {self.student}"
