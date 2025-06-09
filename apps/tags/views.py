from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Tag
from .serializers import TagSerializer, SearchResultSerializer
from apps.users.serializers import UserSerializer
from apps.research_groups.models import ResearchGroup
from apps.research_groups.serializers import ResearchGroupSerializer
from apps.projects.models import Project
from apps.projects.serializers import ProjectSerializer
from apps.experiments.models import Experiment
from apps.experiments.serializers import ExperimentSerializer
from apps.findings.models import Finding
from apps.findings.serializers import FindingSerializer
from apps.publications.models import Publication
from apps.publications.serializers import PublicationSerializer

User = get_user_model()


class TagListView(generics.ListAPIView):
    """List all tags"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['name']
    ordering_fields = ['name', 'usage_count']
    ordering = ['-usage_count']


@api_view(['GET'])
@permission_classes([AllowAny])
def search(request):
    """Search across all resources"""
    query = request.query_params.get('q', '')
    search_type = request.query_params.get('type', 'all')

    if not query:
        return Response({'detail': 'Query parameter q is required'}, status=400)

    results = {
        'users': [],
        'research_groups': [],
        'projects': [],
        'experiments': [],
        'findings': [],
        'publications': []
    }

    if search_type in ['user', 'all']:
        users = User.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query) |
            Q(institution__icontains=query)
        )[:10]
        results['users'] = UserSerializer(users, many=True).data

    if search_type in ['research_group', 'all']:
        groups = ResearchGroup.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(institution__icontains=query),
            is_active=True
        )[:10]
        results['research_groups'] = ResearchGroupSerializer(groups, many=True).data

    if search_type in ['project', 'all']:
        projects = Project.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(short_description__icontains=query),
            is_active=True
        )[:10]
        results['projects'] = ProjectSerializer(projects, many=True).data

    if search_type in ['experiment', 'all']:
        experiments = Experiment.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(hypothesis__icontains=query),
            is_active=True
        )[:10]
        results['experiments'] = ExperimentSerializer(experiments, many=True).data

    if search_type in ['finding', 'all']:
        findings = Finding.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(conclusion__icontains=query),
            is_active=True
        )[:10]
        results['findings'] = FindingSerializer(findings, many=True).data

    if search_type in ['publication', 'all']:
        publications = Publication.objects.filter(
            Q(title__icontains=query) |
            Q(abstract__icontains=query) |
            Q(journal__icontains=query) |
            Q(conference__icontains=query),
            is_active=True
        )[:10]
        results['publications'] = PublicationSerializer(publications, many=True).data

    serializer = SearchResultSerializer(results)
    return Response(serializer.data)
