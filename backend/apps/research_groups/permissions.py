from rest_framework import permissions


class IsResearchGroupLeaderOrAdmin(permissions.BasePermission):
    """
    Permission to check if user is the leader of the research group or an admin.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Allow if user is admin
        if request.user.is_staff or request.user.role == 'admin':
            return True

        # Get the research group object
        if hasattr(obj, 'group'):
            # If obj is a ResearchGroupMember
            group = obj.group
        else:
            # If obj is a ResearchGroup
            group = obj

        # Check if user is the leader
        return group.leader == request.user


class IsResearchGroupMemberWithRole(permissions.BasePermission):
    """
    Permission to check if user is a member of the research group with a specific role.
    """

    def __init__(self, allowed_roles=None):
        self.allowed_roles = allowed_roles or ['leader', 'co_leader']

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Allow if user is admin
        if request.user.is_staff or request.user.role == 'admin':
            return True

        # Get the research group object
        if hasattr(obj, 'group'):
            # If obj is a ResearchGroupMember or similar
            group = obj.group
        else:
            # If obj is a ResearchGroup
            group = obj

        # Check if user is a member with allowed role
        return group.members.filter(
            user=request.user,
            role__in=self.allowed_roles,
            is_active=True
        ).exists()