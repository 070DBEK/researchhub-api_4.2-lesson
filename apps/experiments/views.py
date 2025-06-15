from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project_id = serializer.validated_data.pop('project_id')
        project = get_object_or_404(Project, id=project_id, is_active=True)

        if not project.members.filter(user=request.user, is_active=True).exists():
            return Response(
                {'detail': 'Only project members can create experiments'},
                status=status.HTTP_403_FORBIDDEN
            )
        collaborator_ids = serializer.validated_data.pop('collaborator_ids', [])
        tag_names = serializer.validated_data.pop('tags', [])
        invalid_collaborators = []
        valid_collaborators = []
        for collaborator_id in collaborator_ids:
            try:
                collaborator = User.objects.get(id=collaborator_id)
                valid_collaborators.append(collaborator)
            except User.DoesNotExist:
                invalid_collaborators.append(collaborator_id)

        if invalid_collaborators:
            return Response(
                {'detail': f'Users with IDs {invalid_collaborators} do not exist'},
                status=status.HTTP_400_BAD_REQUEST
            )
        experiment = serializer.save(
            project=project,
            lead_researcher=request.user,
            created_by=request.user,
            updated_by=request.user
        )

        for collaborator in valid_collaborators:
            experiment.collaborators.add(collaborator)

        for tag_name in tag_names:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            experiment.tags.add(tag)
        response_serializer = ExperimentSerializer(experiment)
        headers = self.get_success_headers(response_serializer.data)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED, headers=headers)


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

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if (instance.lead_researcher != request.user and
                not request.user.is_staff):
            return Response(
                {'detail': 'Only experiment lead researcher or admin can update experiment'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        collaborator_ids = serializer.validated_data.pop('collaborator_ids', None)
        tag_names = serializer.validated_data.pop('tags', None)

        if collaborator_ids is not None:
            invalid_collaborators = []
            valid_collaborators = []
            for collaborator_id in collaborator_ids:
                try:
                    collaborator = User.objects.get(id=collaborator_id)
                    valid_collaborators.append(collaborator)
                except User.DoesNotExist:
                    invalid_collaborators.append(collaborator_id)

            if invalid_collaborators:
                return Response(
                    {'detail': f'Users with IDs {invalid_collaborators} do not exist'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        experiment = serializer.save(updated_by=request.user)

        if collaborator_ids is not None:
            experiment.collaborators.clear()
            for collaborator in valid_collaborators:
                experiment.collaborators.add(collaborator)

        if tag_names is not None:
            experiment.tags.clear()
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                experiment.tags.add(tag)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(ExperimentSerializer(experiment).data)

    def perform_destroy(self, instance):
        if (instance.lead_researcher != self.request.user and
                not self.request.user.is_staff):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Only experiment lead researcher or admin can delete experiment")
        instance.is_active = False
        instance.save()
