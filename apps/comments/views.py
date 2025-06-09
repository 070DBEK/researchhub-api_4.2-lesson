from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .models import Comment
from .serializers import CommentSerializer, CommentCreateSerializer, CommentUpdateSerializer
from apps.findings.models import Finding
from apps.publications.models import Publication

User = get_user_model()


class FindingCommentListCreateView(generics.ListCreateAPIView):
    """List comments for a finding or create a new comment"""
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at', 'likes_count']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CommentCreateSerializer
        return CommentSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        finding_id = self.kwargs['finding_id']
        return Comment.objects.filter(
            finding_id=finding_id,
            is_active=True,
            parent__isnull=True  # Only top-level comments
        )

    def perform_create(self, serializer):
        finding_id = self.kwargs['finding_id']
        finding = get_object_or_404(Finding, id=finding_id, is_active=True)

        parent_id = serializer.validated_data.pop('parent_id', None)
        parent = None
        if parent_id:
            parent = get_object_or_404(Comment, id=parent_id, is_active=True)

        serializer.save(
            finding=finding,
            parent=parent,
            author=self.request.user
        )


class PublicationCommentListCreateView(generics.ListCreateAPIView):
    """List comments for a publication or create a new comment"""
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at', 'likes_count']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CommentCreateSerializer
        return CommentSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_queryset(self):
        publication_id = self.kwargs['publication_id']
        return Comment.objects.filter(
            publication_id=publication_id,
            is_active=True,
            parent__isnull=True  # Only top-level comments
        )

    def perform_create(self, serializer):
        publication_id = self.kwargs['publication_id']
        publication = get_object_or_404(Publication, id=publication_id, is_active=True)

        parent_id = serializer.validated_data.pop('parent_id', None)
        parent = None
        if parent_id:
            parent = get_object_or_404(Comment, id=parent_id, is_active=True)

        serializer.save(
            publication=publication,
            parent=parent,
            author=self.request.user
        )


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a comment"""
    queryset = Comment.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return CommentUpdateSerializer
        return CommentSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_update(self, serializer):
        comment = self.get_object()

        # Check permissions
        if (comment.author != self.request.user and
                not self.request.user.is_staff):
            raise PermissionError("Only comment author or admin can update comment")

        serializer.save()

    def perform_destroy(self, instance):
        # Check permissions
        if (instance.author != self.request.user and
                not self.request.user.is_staff):
            raise PermissionError("Only comment author or admin can delete comment")

        instance.is_active = False
        instance.save()
