from django.db import models

class ParentGuardian(models.Model):
    father_name = models.CharField(max_length=100)
    father_phone = models.CharField(max_length=20, blank=True, null=True)
    father_occupation = models.CharField(max_length=100, blank=True, null=True)
    mother_name = models.CharField(max_length=100)
    mother_phone = models.CharField(max_length=20, blank=True, null=True)
    mother_occupation = models.CharField(max_length=100, blank=True, null=True)
    guardian_name = models.CharField(max_length=100, blank=True, null=True)
    guardian_phone = models.CharField(max_length=20, blank=True, null=True)
    guardian_relation = models.CharField(max_length=50, blank=True, null=True)
    guardian_address = models.TextField(blank=True, null=True)
    emergency_contact = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.father_name} / {self.mother_name}"
