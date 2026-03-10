from rest_framework import serializers
from .models import Admin, Student, Attendance, Result, Fee


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    admin = serializers.CharField()  # accept name in POST

    class Meta:
        model = Student
        fields = "__all__"

    def create(self, validated_data):
        admin_name = validated_data.pop("admin")

        try:
            admin = Admin.objects.get(name__iexact=admin_name)
        except Admin.DoesNotExist:
            raise serializers.ValidationError("Admin not found")

        validated_data["admin"] = admin
        return Student.objects.create(**validated_data)
    def update(self, instance, validated_data):
        # Handle admin field if present
        admin_name = validated_data.pop("admin", None)
        if admin_name:
            try:
                admin = Admin.objects.get(name__iexact=admin_name)
            except Admin.DoesNotExist:
                raise serializers.ValidationError("Admin not found")
            instance.admin = admin

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class AttendanceSerializer(serializers.ModelSerializer):
    student = serializers.CharField()  # Accept student name in POST

    class Meta:
        model = Attendance
        fields = '__all__'

    def create(self, validated_data):
        # Pop the student name from validated data
        student_name = validated_data.pop("student")

        try:
            # Find the student by name (case-insensitive)
            student = Student.objects.get(name__iexact=student_name)
        except Student.DoesNotExist:
            raise serializers.ValidationError("Student not found")

        # Assign the actual student object
        validated_data["student"] = student

        # Create and return the Attendance record
        return Attendance.objects.create(**validated_data)
        

class ResultSerializer(serializers.ModelSerializer):
    student = serializers.CharField()

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

class FeeSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField()
    class Meta:
        model = Fee
        fields = '__all__'

