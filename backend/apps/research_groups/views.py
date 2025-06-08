from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import ResearchGroup, ResearchGroupMember
from .serializers import (
    ResearchGroupSerializer, ResearchGroupCreateSerializer, ResearchGroupUpdateSerializer,
    ResearchGroupMemberSerializer, ResearchGroupMemberCreateSerializer, ResearchGroupMemberUpdateSerializer
)
from .permissions import IsResearchGroupLeaderOrAdmin, IsResearchGroupMemberWithRole


class ResearchGroupListCreateView(generics.ListCreateAPIView):
    queryset = ResearchGroup.objects.all()

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ResearchGroupCreateSerializer
        return ResearchGroupSerializer

    def get_queryset(self):
        queryset = ResearchGroup.objects.all()

        # Apply filters
        search = self.request.query_params.get('search')
        institution = self.request.query_params.get('institution')
        department = self.request.query_params.get('department')
        ordering = self.request.query_params.get('ordering', 'name')

        if search:
            queryset = queryset.filter(name__icontains=search)

        if institution:
            queryset = queryset.filter(institution__icontains=institution)

        if department:
            queryset = queryset.filter(department__icontains=department)

        # Apply ordering
        if ordering and ordering in ['name', '-name', 'created_at', '-created_at',
                                     'members_count', '-members_count']:
            queryset = queryset.order_by(ordering)

        return queryset


class ResearchGroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ResearchGroup.objects.all()

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated(), IsResearchGroupLeaderOrAdmin()]
        return [permissions.AllowAny()]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ResearchGroupUpdateSerializer
        return ResearchGroupSerializer

    def perform_destroy(self, instance):
        # Soft delete
        instance.is_active = False
        instance.save()


class ResearchGroupMemberListCreateView(generics.ListCreateAPIView):
    serializer_class = ResearchGroupMemberSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsResearchGroupLeaderOrAdmin()]
        return [permissions.AllowAny()]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ResearchGroupMemberCreateSerializer
        return ResearchGroupMemberSerializer

    def get_queryset(self):
        group_id = self.kwargs.get('group_id')
        queryset = ResearchGroupMember.objects.filter(group_id=group_id)

        # Apply filters
        role = self.request.query_params.get('role')
        ordering = self.request.query_params.get('ordering', '-joined_at')

        if role:
            queryset = queryset.filter(role=role)

        # Apply ordering
        if ordering and ordering in ['joined_at', '-joined_at', 'role', '-role']:
            queryset = queryset.order_by(ordering)

        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['group'] = get_object_or_404(ResearchGroup, id=self.kwargs.get('group_id'))
        return context


class ResearchGroupMemberDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ResearchGroupMemberSerializer
    permission_classes = [permissions.IsAuthenticated, IsResearchGroupLeaderOrAdmin]

    def get_queryset(self):
        group_id = self.kwargs.get('group_id')
        return ResearchGroupMember.objects.filter(group_id=group_id)

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ResearchGroupMemberUpdateSerializer
        return ResearchGroupMemberSerializer

    def get_object(self):
        group_id = self.kwargs.get('group_id')
        member_id = self.kwargs.get('member_id')
        return get_object_or_404(ResearchGroupMember, group_id=group_id, id=member_id)