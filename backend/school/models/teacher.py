from django.db import models

class Teacher(models.Model):
    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    ]
    teacher_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    qualification = models.CharField(max_length=100)
    experience = models.PositiveIntegerField(help_text="Years of experience")
    specialization = models.CharField(max_length=100, blank=True, null=True)
    photo = models.ImageField(upload_to='teachers/photos/', blank=True, null=True)
    joining_date = models.DateField()

    def __str__(self):
        return self.name
