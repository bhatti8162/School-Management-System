from .base import BaseSerializer
from ..models import Result, Student
from rest_framework import serializers

class ResultSerializer(BaseSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())

    class Meta:
        model = Result
        fields = "__all__"

    def create(self, validated_data):
        student_name = validated_data.pop("student")
        try:
            student = Student.objects.get(name__iexact=student_name)
        except Student.DoesNotExist:
            raise serializers.ValidationError("Student not found")
        validated_data["student"] = student
        return Result.objects.create(**validated_data)