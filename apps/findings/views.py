from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        experiment_id = serializer.validated_data.pop('experiment_id')
        experiment = get_object_or_404(Experiment, id=experiment_id, is_active=True)

        if not experiment.project.members.filter(user=request.user, is_active=True).exists():
            return Response(
                {'detail': 'Only project members can create findings'},
                status=status.HTTP_403_FORBIDDEN
            )
        tag_names = serializer.validated_data.pop('tags', [])
        finding = serializer.save(
            experiment=experiment,
            created_by=request.user,
            updated_by=request.user
        )

        for tag_name in tag_names:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            finding.tags.add(tag)
        response_serializer = FindingSerializer(finding)
        headers = self.get_success_headers(response_serializer.data)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED, headers=headers)


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
        instance.views_count += 1
        instance.save(update_fields=['views_count'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if (instance.created_by != request.user and
                not request.user.is_staff):
            return Response(
                {'detail': 'Only finding creator or admin can update finding'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        tag_names = serializer.validated_data.pop('tags', None)
        finding = serializer.save(updated_by=request.user)

        if tag_names is not None:
            finding.tags.clear()
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                finding.tags.add(tag)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(FindingSerializer(finding).data)

    def perform_destroy(self, instance):
        if (instance.created_by != self.request.user and
                not self.request.user.is_staff):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Only finding creator or admin can delete finding")
        instance.is_active = False
        instance.save()
