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
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True, blank=True, related_name="students")
    parent_guardian = models.ForeignKey(
        ParentGuardian,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="students"
    )
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    age = models.PositiveIntegerField()
    photograph = models.ImageField(upload_to='students/photos/', blank=True, null=True)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, blank=True, null=True)
    nationality = models.CharField(max_length=50, blank=True, null=True)
    religion = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=20)
    admission_number = models.CharField(max_length=50, unique=True)
    admission_date = models.DateField()
    previous_school = models.CharField(max_length=100, blank=True, null=True)
    transfer_certificate = models.FileField(upload_to='admissions/tc/', blank=True, null=True)
    admission_class = models.CharField(max_length=50)
    section = models.CharField(max_length=20)
    academic_year = models.CharField(max_length=20)
    admission_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")

    def __str__(self):
        return f"{self.name}"
