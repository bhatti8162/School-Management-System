from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsSuperAdminOrAssignedSchoolUser(BasePermission):
    """
    All-in-one permission:
    1. Superadmins have full access to all objects.
    2. School users can access only objects linked to their assigned school(s).
       Optionally, school users can be restricted to read-only.
    Works for list, retrieve, create, update, delete, and custom actions.
    """

    # Optional: restrict school users to read-only
    SCHOOL_USERS_READ_ONLY = False

    def has_permission(self, request, view):
        # Must be authenticated and have a profile
        if not request.user.is_authenticated or not hasattr(request.user, "profile"):
            return False

        profile = request.user.profile

        # Superadmin bypass: full access
        if profile.role == "superadmin":
            return True

        # School users: check read-only if enforced
        if profile.role == "school":
            if not profile.school:
                return False  # no school assigned
            if self.SCHOOL_USERS_READ_ONLY:
                return request.method in SAFE_METHODS
            return True

        # Deny all other roles
        return False

    def has_object_permission(self, request, view, obj):
        profile = request.user.profile

        # Superadmin bypass: full access
        if profile.role == "superadmin":
            return True

        # School user: access only objects linked to their assigned school
        if profile.role == "school":
            user_school = profile.school
            if not user_school:
                return False

            # Object has 'school' ForeignKey
            if hasattr(obj, "school") and obj.school == user_school:
                return True

            # Object has 'school_id' field
            if hasattr(obj, "school_id") and obj.school_id == user_school.id:
                return True

        return False