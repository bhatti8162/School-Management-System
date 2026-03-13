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

    gr_number = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    father_chic = models.CharField(max_length=13)
    family_name = models.CharField(max_length=100)
    contact = models.CharField(max_length=11)
    b_form = models.CharField(max_length=100)
    age = models.CharField(max_length=100)
    monthly_fee = models.DecimalField(max_digits=10, decimal_places=2)
    class_name = models.CharField(max_length=100, choices=CLASS_CHOICES, default="0")
    admin = models.ForeignKey(Admin, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=20)


class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(default="2000-03-10")
    test_name = models.CharField(max_length=100, default="Test")
    subject = models.CharField(max_length=100)
    marks = models.IntegerField()

class Fee(models.Model):
    MONTH_FEE_CHOICES = [
    ("January", "January"),
    ("February", "February"),
    ("March", "March"),
    ("April", "April"),
    ("May", "May"),
    ("June", "June"),
    ("July", "July"),
    ("August", "August"),
    ("September", "September"),
    ("October", "October"),
    ("November", "November"),
    ("December", "December"),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="fees")
    month = models.CharField(max_length=100, choices=MONTH_FEE_CHOICES, default="January")
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    @property
    def amount(self):
        # Pull the student's fixed monthly fee
        return self.student.monthly_fee

    @property
    def status(self):
        if self.paid_amount >= self.amount:
            return "Full Paid"
        elif self.paid_amount > 0:
            return "Partial Paid"
        else:
            return "Not Paid"

    @property
    def due_amount(self):
        return self.amount - self.paid_amount