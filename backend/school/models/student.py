from django.db import models
from .parent_guardian import ParentGuardian
from .school import School

class Student(models.Model):
    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    ]
    BLOOD_GROUP_CHOICES = [
        ("A+", "A+"), ("A-", "A-"), ("B+", "B+"), ("B-", "B-"),
        ("O+", "O+"), ("O-", "O-"), ("AB+", "AB+"), ("AB-", "AB-")
    ]
    STATUS_CHOICES = [
        ("active", "Active"),
        ("inactive", "Inactive"),
        ("pending", "Pending"),
        ("withdrawn", "Withdrawn"),
    ]

    GR_Id = models.CharField(max_length=50, unique=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="students", blank=True, null=True)
    parent_guardian = models.ForeignKey(
        ParentGuardian,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="students"
    )
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    photograph = models.ImageField(upload_to='students/photos/', blank=True, null=True)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, blank=True, null=True)
    nationality = models.CharField(max_length=50, blank=True, null=True)
    religion = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    admission_number = models.CharField(max_length=50, unique=True, blank=True, null=True)
    admission_date = models.DateField(blank=True, null=True)
    previous_school = models.CharField(max_length=100, blank=True, null=True)
    transfer_certificate = models.FileField(upload_to='admissions/tc/', blank=True, null=True)
    admission_class = models.CharField(max_length=50, blank=True, null=True)
    section = models.CharField(max_length=20, blank=True, null=True)
    academic_year = models.CharField(max_length=20, blank=True, null=True)
    admission_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active", blank=True, null=True)

    def __str__(self):
        return f"{self.name}"
