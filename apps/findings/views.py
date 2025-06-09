from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Finding
from .serializers import FindingSerializer, FindingCreateSerializer, FindingUpdateSerializer
from apps.experiments.models import Experiment
from apps.tags.models import Tag

User = get_user_model()


class FindingListCreateView(generics.ListCreateAPIView):
    """List all findings or create a new one"""
    queryset = Finding.objects.filter(is_active=True)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['significance', 'experiment', 'visibility']
    search_fields = ['title', 'description', 'conclusion']
    ordering_fields = ['title', 'created_at', 'views_count', 'citations_count']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return FindingCreateSerializer
        return FindingSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]

    def perform_create(self, serializer):
        experiment_id = serializer.validated_data.pop('experiment_id')
        experiment = get_object_or_404(Experiment, id=experiment_id, is_active=True)

        # Check if user is project member
        if not experiment.project.members.filter(user=self.request.user, is_active=True).exists():
            raise PermissionError("Only project members can create findings")

        tag_names = serializer.validated_data.pop('tags', [])

        finding = serializer.save(
            experiment=experiment,
            created_by=self.request.user,
            updated_by=self.request.user
        )

        # Add tags
        for tag_name in tag_names:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            finding.tags.add(tag)


class FindingDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a finding"""
    queryset = Finding.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return FindingUpdateSerializer
        return FindingSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Increment view count
        instance.views_count += 1
        instance.save(update_fields=['views_count'])
        return super().retrieve(request, *args, **kwargs)

    def perform_update(self, serializer):
        finding = self.get_object()

        # Check permissions
        if (finding.created_by != self.request.user and
                not self.request.user.is_staff):
            raise PermissionError("Only finding creator or admin can update finding")

        tag_names = serializer.validated_data.pop('tags', None)

        finding = serializer.save(updated_by=self.request.user)

        # Update tags
        if tag_names is not None:
            finding.tags.clear()
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                finding.tags.add(tag)

    def perform_destroy(self, instance):
        # Check permissions
        if (instance.created_by != self.request.user and
                not self.request.user.is_staff):
            raise PermissionError("Only finding creator or admin can delete finding")

        instance.is_active = False
        instance.save()
