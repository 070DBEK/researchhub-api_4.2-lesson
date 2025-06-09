from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.core.files.storage import default_storage
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from .models import Attachment
from .serializers import AttachmentSerializer, AttachmentCreateSerializer, AttachmentUpdateSerializer
from apps.findings.models import Finding
from apps.experiments.models import Experiment

User = get_user_model()


class AttachmentListCreateView(generics.ListCreateAPIView):
    """List attachments for a finding or upload a new one"""
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['file_type']
    ordering_fields = ['title', 'created_at', 'file_size', 'downloads_count']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AttachmentCreateSerializer
        return AttachmentSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        finding_id = self.kwargs['finding_id']
        return Attachment.objects.filter(
            finding_id=finding_id,
            is_active=True
        )

    def perform_create(self, serializer):
        finding_id = self.kwargs['finding_id']
        finding = get_object_or_404(Finding, id=finding_id, is_active=True)

        # Check if user is project member
        if not finding.experiment.project.members.filter(user=self.request.user, is_active=True).exists():
            raise PermissionError("Only project members can upload attachments")

        file = serializer.validated_data.pop('file')
        experiment_id = serializer.validated_data.pop('experiment_id', None)
        experiment = None

        if experiment_id:
            experiment = get_object_or_404(Experiment, id=experiment_id, is_active=True)

        # Save file (in production, use cloud storage like AWS S3)
        file_path = default_storage.save(f'attachments/{file.name}', file)
        file_url = default_storage.url(file_path)

        attachment = serializer.save(
            finding=finding,
            experiment=experiment,
            file_url=file_url,
            file_size=file.size,
            content_type=file.content_type,
            created_by=self.request.user,
            updated_by=self.request.user
        )


class AttachmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete an attachment"""
    queryset = Attachment.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return AttachmentUpdateSerializer
        return AttachmentSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Increment download count
        instance.downloads_count += 1
        instance.save(update_fields=['downloads_count'])
        return super().retrieve(request, *args, **kwargs)

    def perform_update(self, serializer):
        attachment = self.get_object()

        # Check permissions
        if (attachment.created_by != self.request.user and
                not self.request.user.is_staff):
            raise PermissionError("Only attachment uploader or admin can update attachment")

        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        # Check permissions
        if (instance.created_by != self.request.user and
                not self.request.user.is_staff):
            raise PermissionError("Only attachment uploader or admin can delete attachment")

        instance.is_active = False
        instance.save()
