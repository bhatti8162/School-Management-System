from django.db import models
from .student import Student

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
        return getattr(self.student, 'monthly_fee', 0)

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
