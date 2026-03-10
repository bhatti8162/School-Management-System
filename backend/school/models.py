from django.db import models

class Admin(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Student(models.Model):
    CLASS_CHOICES = [
        ("Nursery", "Nursery"),
        ("KG", "KG"),
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5"),
        ("6", "6"),
        ("7", "7"),
        ("8", "8"),
        ("9", "9"),
        ("10", "10"),
        ("11", "11"),
        ("12", "12"),
    ]

    name = models.CharField(max_length=100)
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)
    class_name = models.CharField(max_length=100, choices=CLASS_CHOICES, default="0")

    def __str__(self):
        return self.name


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=20)


class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(default="2026-03-10")
    test_name = models.CharField(max_length=100, default="Test")
    subject = models.CharField(max_length=100)
    marks = models.IntegerField()

class Fee(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.IntegerField()
    month = models.CharField(max_length=20)