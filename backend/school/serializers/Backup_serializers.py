from rest_framework import serializers
from ..models import (
    School,
    ParentGuardian,
    Student,
    Teacher,
    Result,
    Fee,
    Attendance,
)


class BaseSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data = self._replace_empty_with_na(data)
        return data

    def _replace_empty_with_na(self, data):
        if isinstance(data, dict):
            for key, value in data.items():
                if value is None or value == '':
                    data[key] = 'N/A'
                elif isinstance(value, dict):
                    data[key] = self._replace_empty_with_na(value)
                elif isinstance(value, list):
                    data[key] = [self._replace_empty_with_na(item) if isinstance(item, dict) else item for item in value]
        return data


class SchoolSerializer(BaseSerializer):
    class Meta:
        model = School
        fields = '__all__'


class ParentGuardianSerializer(BaseSerializer):
    school_id = serializers.CharField(source="school.school_id", read_only=True) 

    class Meta:
        model = ParentGuardian
        fields = '__all__'


class StudentSerializer(BaseSerializer):
    family_id = serializers.CharField(source="parent_guardian.family_id",read_only=True)
    school_id = serializers.CharField(source="parent_guardian.school.school_id", read_only=True) 
    school_name = serializers.CharField(source="parent_guardian.school.name", read_only=True) 

    class Meta:
        model = Student
        # fields = "__all__"
        exclude = ['id', 'parent_guardian', 'school'] 


class TeacherSerializer(BaseSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'


class AttendanceSerializer(BaseSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'


class ResultSerializer(BaseSerializer):
    # Let DRF select student by ID
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

class FeeSerializer(BaseSerializer):
    # Let DRF select student by ID
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    
    # Read-only fields
    amount = serializers.ReadOnlyField()      # pulls from student.monthly_fee
    status = serializers.ReadOnlyField()
    due_amount = serializers.ReadOnlyField()

    class Meta:
        model = Fee
        fields = ["student", "month", "amount", "paid_amount", "status", "due_amount"]