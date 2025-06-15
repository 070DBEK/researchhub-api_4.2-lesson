from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Project, ProjectMember
from .serializers import (
    ProjectSerializer, ProjectCreateSerializer, ProjectUpdateSerializer,
    ProjectMemberSerializer, ProjectMemberCreateSerializer, ProjectMemberUpdateSerializer
)
from apps.research_groups.models import ResearchGroup
from apps.tags.models import Tag

User = get_user_model()


class ProjectListCreateView(generics.ListCreateAPIView):
    """List all projects or create a new one"""
    queryset = Project.objects.filter(is_active=True)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'visibility', 'research_group', 'principal_investigator']
    search_fields = ['title', 'description', 'short_description']
    ordering_fields = ['title', 'start_date', 'created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProjectCreateSerializer
        return ProjectSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Handle research group
        research_group = None
        research_group_id = serializer.validated_data.pop('research_group_id', None)
        if research_group_id:
            research_group = get_object_or_404(ResearchGroup, id=research_group_id)

        # Handle tags
        tag_names = serializer.validated_data.pop('tags', [])

        # Create project
        project = serializer.save(
            principal_investigator=request.user,
            research_group=research_group,
            created_by=request.user,
            updated_by=request.user
        )

        # Add tags
        if tag_names:
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                project.tags.add(tag)

        # Add creator as principal investigator member
        ProjectMember.objects.create(
            project=project,
            user=request.user,
            role='principal_investigator'
        )

        # Return response with ProjectSerializer
        response_serializer = ProjectSerializer(project)
        headers = self.get_success_headers(response_serializer.data)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a project"""
    queryset = Project.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ProjectUpdateSerializer
        return ProjectSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_update(self, serializer):
        project = self.get_object()

        # Check permissions
        if (project.principal_investigator != self.request.user and
                not self.request.user.is_staff and
                not project.members.filter(user=self.request.user,
                                           role__in=['principal_investigator', 'co_investigator']).exists()):
            raise PermissionError("Only project PI, co-PI or admin can update project")

        # Handle research group
        research_group = project.research_group
        research_group_id = serializer.validated_data.pop('research_group_id', None)
        if research_group_id is not None:
            research_group = get_object_or_404(ResearchGroup, id=research_group_id) if research_group_id else None

        # Handle tags
        tag_names = serializer.validated_data.pop('tags', None)

        project = serializer.save(
            research_group=research_group,
            updated_by=self.request.user
        )

        # Update tags
        if tag_names is not None:
            project.tags.clear()
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                project.tags.add(tag)

    def perform_destroy(self, instance):
        # Check permissions
        if instance.principal_investigator != self.request.user and not self.request.user.is_staff:
            raise PermissionError("Only project PI or admin can delete project")

        instance.is_active = False
        instance.save()


class ProjectMemberListCreateView(generics.ListCreateAPIView):
    """List members of a project or add a new member"""
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['role']
    ordering_fields = ['joined_at', 'role']
    ordering = ['-joined_at']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProjectMemberCreateSerializer
        return ProjectMemberSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        return ProjectMember.objects.filter(
            project_id=project_id,
            is_active=True
        )

    def perform_create(self, serializer):
        project_id = self.kwargs['project_id']
        project = get_object_or_404(Project, id=project_id, is_active=True)

        if (project.principal_investigator != self.request.user and
                not self.request.user.is_staff and
                not project.members.filter(user=self.request.user,
                                           role__in=['principal_investigator', 'co_investigator']).exists()):
            raise PermissionError("Only project PI, co-PI or admin can add members")

        user_id = serializer.validated_data['user_id']
        user = get_object_or_404(User, id=user_id)

        serializer.save(project=project, user=user)


class ProjectMemberDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or remove a project member"""
    serializer_class = ProjectMemberSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        project_id = self.kwargs['project_id']
        member_id = self.kwargs['member_id']
        return get_object_or_404(
            ProjectMember,
            id=member_id,
            project_id=project_id,
            is_active=True
        )

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ProjectMemberUpdateSerializer
        return ProjectMemberSerializer

    def perform_update(self, serializer):
        member = self.get_object()
        project = member.project

        if (project.principal_investigator != self.request.user and
                not self.request.user.is_staff):
            raise PermissionError("Only project PI or admin can update members")
        serializer.save()

    def perform_destroy(self, instance):
        project = instance.project

        if (project.principal_investigator != self.request.user and
                not self.request.user.is_staff):
            raise PermissionError("Only project PI or admin can remove members")
        instance.is_active = False
        instance.save()
