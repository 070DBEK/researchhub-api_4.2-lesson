from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project_id = serializer.validated_data.pop('project_id')
        project = get_object_or_404(Project, id=project_id, is_active=True)
        if not project.members.filter(user=request.user, is_active=True).exists():
            return Response(
                {'detail': 'Only project members can create publications'},
                status=status.HTTP_403_FORBIDDEN
            )
        author_ids = serializer.validated_data.pop('author_ids')
        finding_ids = serializer.validated_data.pop('finding_ids', [])
        tag_names = serializer.validated_data.pop('tags', [])
        invalid_authors = []
        valid_authors = []
        for author_id in author_ids:
            try:
                author = User.objects.get(id=author_id)
                valid_authors.append(author)
            except User.DoesNotExist:
                invalid_authors.append(author_id)

        if invalid_authors:
            return Response(
                {'detail': f'Authors with IDs {invalid_authors} do not exist'},
                status=status.HTTP_400_BAD_REQUEST
            )
        invalid_findings = []
        valid_findings = []
        for finding_id in finding_ids:
            try:
                finding = Finding.objects.get(id=finding_id, is_active=True)
                valid_findings.append(finding)
            except Finding.DoesNotExist:
                invalid_findings.append(finding_id)

        if invalid_findings:
            return Response(
                {'detail': f'Findings with IDs {invalid_findings} do not exist'},
                status=status.HTTP_400_BAD_REQUEST
            )
        publication = serializer.save(
            project=project,
            created_by=request.user,
            updated_by=request.user
        )
        for author in valid_authors:
            publication.authors.add(author)

        for finding in valid_findings:
            publication.findings.add(finding)

        for tag_name in tag_names:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            publication.tags.add(tag)
        response_serializer = PublicationSerializer(publication)
        headers = self.get_success_headers(response_serializer.data)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED, headers=headers)


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
        instance.views_count += 1
        instance.save(update_fields=['views_count'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if (not instance.authors.filter(id=request.user.id).exists() and
                not request.user.is_staff):
            return Response(
                {'detail': 'Only publication authors or admin can update publication'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        author_ids = serializer.validated_data.pop('author_ids', None)
        finding_ids = serializer.validated_data.pop('finding_ids', None)
        tag_names = serializer.validated_data.pop('tags', None)

        if author_ids is not None:
            invalid_authors = []
            valid_authors = []
            for author_id in author_ids:
                try:
                    author = User.objects.get(id=author_id)
                    valid_authors.append(author)
                except User.DoesNotExist:
                    invalid_authors.append(author_id)

            if invalid_authors:
                return Response(
                    {'detail': f'Authors with IDs {invalid_authors} do not exist'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        if finding_ids is not None:
            invalid_findings = []
            valid_findings = []
            for finding_id in finding_ids:
                try:
                    finding = Finding.objects.get(id=finding_id, is_active=True)
                    valid_findings.append(finding)
                except Finding.DoesNotExist:
                    invalid_findings.append(finding_id)

            if invalid_findings:
                return Response(
                    {'detail': f'Findings with IDs {invalid_findings} do not exist'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        publication = serializer.save(updated_by=request.user)

        if author_ids is not None:
            publication.authors.clear()
            for author in valid_authors:
                publication.authors.add(author)

        if finding_ids is not None:
            publication.findings.clear()
            for finding in valid_findings:
                publication.findings.add(finding)

        if tag_names is not None:
            publication.tags.clear()
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                publication.tags.add(tag)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(PublicationSerializer(publication).data)

    def perform_destroy(self, instance):
        if (not instance.authors.filter(id=self.request.user.id).exists() and
                not self.request.user.is_staff):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Only publication authors or admin can delete publication")
        instance.is_active = False
        instance.save()
