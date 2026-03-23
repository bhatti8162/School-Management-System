from .base import BaseSerializer
from ..models import Fee, Student
from rest_framework import serializers

class FeeSerializer(BaseSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    amount = serializers.ReadOnlyField()     
    status = serializers.ReadOnlyField()
    due_amount = serializers.ReadOnlyField()

    class Meta:
        model = Fee
        fields = ["student", "month", "amount", "paid_amount", "status", "due_amount"]