from .base import *
from ..models.parent_guardian import ParentGuardian
from ..serializers import ParentGuardianSerializer

class ParentGuardianViewSet(ModelViewSet):
    serializer_class = ParentGuardianSerializer
    permission_classes = [IsAuthenticated, IsSuperAdminOrAssignedSchoolUser]
    lookup_field = "family_id"

    def get_queryset(self):
        user_school = self.request.user.profile.school
        return ParentGuardian.objects.filter(school=user_school)