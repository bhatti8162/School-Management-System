# models.py
from django.contrib.auth.models import User
from django.db import models
from .school import School

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('superadmin', 'Super Admin'),
        ('school', 'School User'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='school')
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        if self.role == 'superadmin':
            return f"{self.user.username} → Super Admin"
        return f"{self.user.username} → {self.school.name if self.school else 'No School'}"

    @property
    def is_superadmin(self):
        return self.role == 'superadmin'