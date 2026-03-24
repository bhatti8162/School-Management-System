from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsSuperAdminOrAssignedSchoolUser(BasePermission):
    """
    Permission:
    1. Superadmins have full access.
    2. School users can access only objects linked to their assigned school.
       Optionally, school users can be restricted to read-only.
    """

    SCHOOL_USERS_READ_ONLY = False  # Set True to make school users read-only

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated or not hasattr(user, "profile"):
            return False

        profile = user.profile

        # Superadmin has full access
        if profile.role == "superadmin":
            return True

        # School user
        if profile.role == "school":
            if not profile.school:
                return False
            if self.SCHOOL_USERS_READ_ONLY:
                return request.method in SAFE_METHODS
            return True

        return False

    def has_object_permission(self, request, view, obj):
        user = request.user
        profile = user.profile

        # Superadmin: full access
        if profile.role == "superadmin":
            return True

        # School user: only for their school
        if profile.role == "school" and profile.school:
            user_school = profile.school

            # Check FK fields
            if getattr(obj, "school", None) == user_school:
                return True
            if getattr(obj, "school_id", None) == user_school:
                return True
            if getattr(obj, "family_id", None) and getattr(obj.family_id, "school", None) == user_school:
                return True  # for ParentGuardian linked via student

        return False