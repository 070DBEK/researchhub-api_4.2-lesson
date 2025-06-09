from rest_framework import serializers
from .models import UserActivity
from apps.users.serializers import UserSerializer


class UserActivitySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    target_type = serializers.ReadOnlyField()
    target_id = serializers.ReadOnlyField()

    class Meta:
        model = UserActivity
        fields = [
            'id', 'user', 'action', 'target_type', 'target_id',
            'details', 'ip_address', 'user_agent', 'created_at'
        ]
        read_only_fields = [
            'id', 'user', 'action', 'target_type', 'target_id',
            'details', 'ip_address', 'user_agent', 'created_at'
        ]


class AnalyticsSummarySerializer(serializers.Serializer):
    total_users = serializers.IntegerField()
    active_users = serializers.IntegerField()
    total_projects = serializers.IntegerField()
    active_projects = serializers.IntegerField()
    total_findings = serializers.IntegerField()
    total_publications = serializers.IntegerField()
    total_views = serializers.IntegerField()
    total_downloads = serializers.IntegerField()
    user_growth = serializers.DictField()
    project_growth = serializers.DictField()
    top_viewed_findings = serializers.ListField()
    top_cited_publications = serializers.ListField()
