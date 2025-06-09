from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Experiment
from .serializers import ExperimentSerializer, ExperimentCreateSerializer, ExperimentUpdateSerializer
from apps.projects.models import Project
from apps.tags.models import Tag

User = get_user_model()


class ExperimentListCreateView(generics.ListCreateAPIView):
    """List all experiments or create a new one"""
    queryset = Experiment.objects.filter(is_active=True)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'project', 'lead_researcher']
    search_fields = ['title', 'description', 'hypothesis']
    ordering_fields = ['title', 'start_date', 'created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ExperimentCreateSerializer
        return ExperimentSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]

    def perform_create(self, serializer):
        project_id = serializer.validated_data.pop('project_id')
        project = get_object_or_404(Project, id=project_id, is_active=True)

        # Check if user is project member
        if not project.members.filter(user=self.request.user, is_active=True).exists():
            raise PermissionError("Only project members can create experiments")

        collaborator_ids = serializer.validated_data.pop('collaborator_ids', [])
        tag_names = serializer.validated_data.pop('tags', [])

        experiment = serializer.save(
            project=project,
            lead_researcher=self.request.user,
            created_by=self.request.user,
            updated_by=self.request.user
        )

        # Add collaborators
        for collaborator_id in collaborator_ids:
            collaborator = get_object_or_404(User, id=collaborator_id)
            experiment.collaborators.add(collaborator)

        # Add tags
        for tag_name in tag_names:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            experiment.tags.add(tag)


class ExperimentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete an experiment"""
    queryset = Experiment.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ExperimentUpdateSerializer
        return ExperimentSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_update(self, serializer):
        experiment = self.get_object()

        # Check permissions
        if (experiment.lead_researcher != self.request.user and
                not self.request.user.is_staff):
            raise PermissionError("Only experiment lead researcher or admin can update experiment")

        collaborator_ids = serializer.validated_data.pop('collaborator_ids', None)
        tag_names = serializer.validated_data.pop('tags', None)

        experiment = serializer.save(updated_by=self.request.user)

        # Update collaborators
        if collaborator_ids is not None:
            experiment.collaborators.clear()
            for collaborator_id in collaborator_ids:
                collaborator = get_object_or_404(User, id=collaborator_id)
                experiment.collaborators.add(collaborator)

        # Update tags
        if tag_names is not None:
            experiment.tags.clear()
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                experiment.tags.add(tag)

    def perform_destroy(self, instance):
        # Check permissions
        if (instance.lead_researcher != self.request.user and
                not self.request.user.is_staff):
            raise PermissionError("Only experiment lead researcher or admin can delete experiment")

        instance.is_active = False
        instance.save()
