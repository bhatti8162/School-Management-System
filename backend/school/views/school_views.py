from .base import *
from ..models.school import School
from ..serializers import SchoolSerializer

class SchoolViewSet(ModelViewSet):
    serializer_class = SchoolSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrAssignedSchoolUser]

    def get_queryset(self):
        user = self.request.user
        profile = user.profile

        if profile.role == "superadmin":
            return School.objects.all()

        if profile.role == "school" and profile.school:
            return School.objects.filter(id=profile.school.id)

        return School.objects.none()

    @action(detail=False, methods=['get'])
    def me(self, request):
        profile = request.user.profile

        if profile.role == "superadmin":
            queryset = School.objects.all()
            serializer = self.get_serializer(queryset, many=True)
        else:
            if not profile.school:
                return Response({"detail": "No school assigned"}, status=404)
            serializer = self.get_serializer(profile.school)

        return Response(serializer.data)