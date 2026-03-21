from django.db import models
from django.contrib.auth.models import User
from django.db import models

class School(models.Model):
    school_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    school_phone = models.CharField(max_length=20, blank=True, null=True)


    def __str__(self):
        return f" {self.school_id} / {self.name}"
    
