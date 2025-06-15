from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta, datetime
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .models import UserActivity
from .serializers import UserActivitySerializer, AnalyticsSummarySerializer
from apps.projects.models import Project
from apps.findings.models import Finding
from apps.publications.models import Publication


User = get_user_model()


@api_view(['GET'])
@permission_classes([IsAdminUser])
def analytics_summary(request):
    """Get analytics summary"""
    period = request.query_params.get('period', 'month')
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')
    now = timezone.now()

    if start_date and end_date:
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
    elif period == 'day':
        start = now - timedelta(days=1)
        end = now
    elif period == 'week':
        start = now - timedelta(weeks=1)
        end = now
    elif period == 'month':
        start = now - timedelta(days=30)
        end = now
    elif period == 'year':
        start = now - timedelta(days=365)
        end = now
    else:  # all
        start = None
        end = None

    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    total_projects = Project.objects.count()
    active_projects = Project.objects.filter(is_active=True).count()
    total_findings = Finding.objects.filter(is_active=True).count()
    total_publications = Publication.objects.filter(is_active=True).count()

    activities_query = UserActivity.objects.all()
    if start and end:
        activities_query = activities_query.filter(created_at__range=[start, end])

    total_views = activities_query.filter(action='view').count()
    total_downloads = activities_query.filter(action='download').count()

    user_growth = {
        'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'data': [10, 20, 30, 40, 50, 60]
    }

    project_growth = {
        'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'data': [5, 10, 15, 20, 25, 30]
    }

    top_viewed_findings = Finding.objects.filter(is_active=True).order_by('-views_count')[:5]
    top_viewed_findings_data = [
        {
            'id': finding.id,
            'title': finding.title,
            'views': finding.views_count
        }
        for finding in top_viewed_findings
    ]

    top_cited_publications = Publication.objects.filter(is_active=True).order_by('-citations_count')[:5]
    top_cited_publications_data = [
        {
            'id': pub.id,
            'title': pub.title,
            'citations': pub.citations_count
        }
        for pub in top_cited_publications
    ]

    data = {
        'total_users': total_users,
        'active_users': active_users,
        'total_projects': total_projects,
        'active_projects': active_projects,
        'total_findings': total_findings,
        'total_publications': total_publications,
        'total_views': total_views,
        'total_downloads': total_downloads,
        'user_growth': user_growth,
        'project_growth': project_growth,
        'top_viewed_findings': top_viewed_findings_data,
        'top_cited_publications': top_cited_publications_data,
    }

    serializer = AnalyticsSummarySerializer(data)
    return Response(serializer.data)


class UserActivityListView(generics.ListAPIView):
    """List user activities"""
    serializer_class = UserActivitySerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['user', 'action', 'target_content_type']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = UserActivity.objects.all()

        # Filter by date range
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if start_date and end_date:
            queryset = queryset.filter(
                created_at__range=[start_date, end_date]
            )

        return queryset
