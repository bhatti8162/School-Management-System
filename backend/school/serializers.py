from rest_framework import serializers
from .models import Admin
from .models.parent_guardian import ParentGuardian
from .models.student import Student
from .models.admission import Admission
from .models.teacher import Teacher
from .models.result import Result
from .models.fee import Fee
from .models.attendance import Attendance


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


class AdminSerializer(BaseSerializer):
    class Meta:
        model = Admin
        fields = '__all__'


class ParentGuardianSerializer(BaseSerializer):
    class Meta:
        model = ParentGuardian
        fields = '__all__'


class StudentSerializer(BaseSerializer):
    parent_guardian = ParentGuardianSerializer(read_only=True)
    parent_guardian_id = serializers.PrimaryKeyRelatedField(
        queryset=ParentGuardian.objects.all(), source='parent_guardian', write_only=True, required=False
    )

    class Meta:
        model = Student
        fields = "__all__"


class AdmissionSerializer(BaseSerializer):
    student = StudentSerializer(read_only=True)
    student_id = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all(), source='student', write_only=True
    )

    class Meta:
        model = Admission
        fields = '__all__'


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