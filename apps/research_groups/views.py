from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import ResearchGroup, ResearchGroupMember
from .serializers import (
    ResearchGroupSerializer, ResearchGroupCreateSerializer,
    ResearchGroupUpdateSerializer, ResearchGroupMemberSerializer,
    ResearchGroupMemberCreateSerializer, ResearchGroupMemberUpdateSerializer
)

User = get_user_model()


class ResearchGroupListCreateView(generics.ListCreateAPIView):
    """List all research groups or create a new one"""
    queryset = ResearchGroup.objects.filter(is_active=True)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['institution', 'department']
    search_fields = ['name', 'description', 'institution']
    ordering_fields = ['name', 'created_at', 'members_count']
    ordering = ['name']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ResearchGroupCreateSerializer
        return ResearchGroupSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]

    def perform_create(self, serializer):
        group = serializer.save(
            leader=self.request.user,
            created_by=self.request.user,
            updated_by=self.request.user
        )
        # Add creator as leader member
        ResearchGroupMember.objects.create(
            group=group,
            user=self.request.user,
            role='leader'
        )


class ResearchGroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a research group"""
    queryset = ResearchGroup.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ResearchGroupUpdateSerializer
        return ResearchGroupSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_update(self, serializer):
        # Check if user is leader or admin
        group = self.get_object()
        if group.leader != self.request.user and not self.request.user.is_staff:
            raise PermissionError("Only group leader or admin can update group")
        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        # Check if user is leader or admin
        if instance.leader != self.request.user and not self.request.user.is_staff:
            raise PermissionError("Only group leader or admin can delete group")
        instance.is_active = False
        instance.save()


class ResearchGroupMemberListCreateView(generics.ListCreateAPIView):
    """List members of a research group or add a new member"""
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['role']
    ordering_fields = ['joined_at', 'role']
    ordering = ['-joined_at']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ResearchGroupMemberCreateSerializer
        return ResearchGroupMemberSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        group_id = self.kwargs['group_id']
        return ResearchGroupMember.objects.filter(
            group_id=group_id,
            is_active=True
        )

    def perform_create(self, serializer):
        group_id = self.kwargs['group_id']
        group = get_object_or_404(ResearchGroup, id=group_id, is_active=True)

        # Check if user is leader or admin
        if group.leader != self.request.user and not self.request.user.is_staff:
            raise PermissionError("Only group leader or admin can add members")

        user_id = serializer.validated_data['user_id']
        user = get_object_or_404(User, id=user_id)

        serializer.save(group=group, user=user)


class ResearchGroupMemberDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or remove a research group member"""
    serializer_class = ResearchGroupMemberSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        group_id = self.kwargs['group_id']
        member_id = self.kwargs['member_id']
        return get_object_or_404(
            ResearchGroupMember,
            id=member_id,
            group_id=group_id,
            is_active=True
        )

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ResearchGroupMemberUpdateSerializer
        return ResearchGroupMemberSerializer

    def perform_update(self, serializer):
        member = self.get_object()
        group = member.group

        # Check if user is leader or admin
        if group.leader != self.request.user and not self.request.user.is_staff:
            raise PermissionError("Only group leader or admin can update members")

        serializer.save()

    def perform_destroy(self, instance):
        group = instance.group

        # Check if user is leader or admin
        if group.leader != self.request.user and not self.request.user.is_staff:
            raise PermissionError("Only group leader or admin can remove members")

        instance.is_active = False
        instance.save()
