"""
Custom permissions for the ResearchHub API.
"""
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the object.
        return obj.created_by == request.user


class IsProjectMemberOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow project members to edit project-related objects.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Check if user is a project member
        if hasattr(obj, 'project'):
            return obj.project.members.filter(user=request.user, is_active=True).exists()

        return False


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors to edit their content.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the author
        if hasattr(obj, 'author'):
            return obj.author == request.user
        elif hasattr(obj, 'authors'):
            return obj.authors.filter(id=request.user.id).exists()

        return False


class IsGroupLeaderOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow group leaders to edit group-related objects.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Check if user is group leader
        if hasattr(obj, 'research_group'):
            return obj.research_group.leader == request.user
        elif hasattr(obj, 'group'):
            return obj.group.leader == request.user

        return False
