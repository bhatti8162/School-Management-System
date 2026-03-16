from django.db import models
from .student import Student

class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(default="2000-03-10")
    test_name = models.CharField(max_length=100, default="Test")
    subject = models.CharField(max_length=100)
    marks = models.IntegerField()
