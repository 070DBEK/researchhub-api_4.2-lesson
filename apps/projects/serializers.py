from rest_framework import serializers
from .models import Project, ProjectMember
from apps.users.serializers import UserSerializer
from apps.research_groups.serializers import ResearchGroupSerializer


class ProjectSerializer(serializers.ModelSerializer):
    principal_investigator = UserSerializer(read_only=True)
    research_group = ResearchGroupSerializer(read_only=True)
    members_count = serializers.ReadOnlyField()
    experiments_count = serializers.ReadOnlyField()
    findings_count = serializers.ReadOnlyField()
    publications_count = serializers.ReadOnlyField()
    tags = serializers.StringRelatedField(many=True, read_only=True)
    created_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'description', 'short_description', 'start_date',
            'end_date', 'status', 'visibility', 'funding_source', 'funding_amount',
            'funding_currency', 'research_group', 'principal_investigator',
            'members_count', 'experiments_count', 'findings_count',
            'publications_count', 'tags', 'is_active', 'created_at',
            'updated_at', 'created_by', 'updated_by'
        ]
        read_only_fields = [
            'id', 'principal_investigator', 'is_active', 'created_at',
            'updated_at', 'created_by', 'updated_by'
        ]


class ProjectCreateSerializer(serializers.ModelSerializer):
    research_group_id = serializers.IntegerField(required=False, allow_null=True)
    tags = serializers.ListField(child=serializers.CharField(), required=False)

    class Meta:
        model = Project
        fields = [
            'title', 'description', 'short_description', 'start_date',
            'end_date', 'status', 'visibility', 'funding_source',
            'funding_amount', 'funding_currency', 'research_group_id', 'tags'
        ]

    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters long")
        return value

    def validate_description(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("Description must be at least 10 characters long")
        return value


class ProjectUpdateSerializer(serializers.ModelSerializer):
    research_group_id = serializers.IntegerField(required=False, allow_null=True)
    tags = serializers.ListField(child=serializers.CharField(), required=False)

    class Meta:
        model = Project
        fields = [
            'title', 'description', 'short_description', 'start_date',
            'end_date', 'status', 'visibility', 'funding_source',
            'funding_amount', 'funding_currency', 'research_group_id',
            'tags', 'is_active'
        ]


class ProjectMemberSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = ProjectMember
        fields = [
            'id', 'project', 'user', 'role', 'joined_at',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'joined_at', 'created_at', 'updated_at']


class ProjectMemberCreateSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()

    class Meta:
        model = ProjectMember
        fields = ['user_id', 'role']


class ProjectMemberUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectMember
        fields = ['role', 'is_active']
