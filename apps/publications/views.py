from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Publication
from .serializers import PublicationSerializer, PublicationCreateSerializer, PublicationUpdateSerializer
from apps.projects.models import Project
from apps.findings.models import Finding
from apps.tags.models import Tag

User = get_user_model()


class PublicationListCreateView(generics.ListCreateAPIView):
    """List all publications or create a new one"""
    queryset = Publication.objects.filter(is_active=True)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'project', 'authors']
    search_fields = ['title', 'abstract', 'journal', 'conference']
    ordering_fields = ['title', 'publication_date', 'created_at', 'citations_count']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PublicationCreateSerializer
        return PublicationSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]

    def perform_create(self, serializer):
        project_id = serializer.validated_data.pop('project_id')
        project = get_object_or_404(Project, id=project_id, is_active=True)

        # Check if user is project member
        if not project.members.filter(user=self.request.user, is_active=True).exists():
            raise PermissionError("Only project members can create publications")

        author_ids = serializer.validated_data.pop('author_ids')
        finding_ids = serializer.validated_data.pop('finding_ids', [])
        tag_names = serializer.validated_data.pop('tags', [])

        publication = serializer.save(
            project=project,
            created_by=self.request.user,
            updated_by=self.request.user
        )

        # Add authors
        for author_id in author_ids:
            author = get_object_or_404(User, id=author_id)
            publication.authors.add(author)

        # Add findings
        for finding_id in finding_ids:
            finding = get_object_or_404(Finding, id=finding_id, is_active=True)
            publication.findings.add(finding)

        # Add tags
        for tag_name in tag_names:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            publication.tags.add(tag)


class PublicationDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a publication"""
    queryset = Publication.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return PublicationUpdateSerializer
        return PublicationSerializer

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
        publication = self.get_object()

        # Check permissions - only authors or admin can update
        if (not publication.authors.filter(id=self.request.user.id).exists() and
                not self.request.user.is_staff):
            raise PermissionError("Only publication authors or admin can update publication")

        author_ids = serializer.validated_data.pop('author_ids', None)
        finding_ids = serializer.validated_data.pop('finding_ids', None)
        tag_names = serializer.validated_data.pop('tags', None)

        publication = serializer.save(updated_by=self.request.user)

        # Update authors
        if author_ids is not None:
            publication.authors.clear()
            for author_id in author_ids:
                author = get_object_or_404(User, id=author_id)
                publication.authors.add(author)

        # Update findings
        if finding_ids is not None:
            publication.findings.clear()
            for finding_id in finding_ids:
                finding = get_object_or_404(Finding, id=finding_id, is_active=True)
                publication.findings.add(finding)

        # Update tags
        if tag_names is not None:
            publication.tags.clear()
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                publication.tags.add(tag)

    def perform_destroy(self, instance):
        # Check permissions - only authors or admin can delete
        if (not instance.authors.filter(id=self.request.user.id).exists() and
                not self.request.user.is_staff):
            raise PermissionError("Only publication authors or admin can delete publication")

        instance.is_active = False
        instance.save()
