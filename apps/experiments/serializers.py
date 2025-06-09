from rest_framework import serializers
from .models import Experiment
from apps.users.serializers import UserSerializer
from apps.projects.serializers import ProjectSerializer


class ExperimentSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)
    lead_researcher = UserSerializer(read_only=True)
    collaborators = UserSerializer(many=True, read_only=True)
    findings_count = serializers.ReadOnlyField()
    tags = serializers.StringRelatedField(many=True, read_only=True)
    created_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)

    class Meta:
        model = Experiment
        fields = [
            'id', 'title', 'description', 'hypothesis', 'methodology',
            'start_date', 'end_date', 'status', 'project', 'lead_researcher',
            'collaborators', 'findings_count', 'tags', 'is_active',
            'created_at', 'updated_at', 'created_by', 'updated_by'
        ]
        read_only_fields = [
            'id', 'project', 'lead_researcher', 'is_active',
            'created_at', 'updated_at', 'created_by', 'updated_by'
        ]


class ExperimentCreateSerializer(serializers.ModelSerializer):
    project_id = serializers.IntegerField()
    collaborator_ids = serializers.ListField(child=serializers.IntegerField(), required=False)
    tags = serializers.ListField(child=serializers.CharField(), required=False)

    class Meta:
        model = Experiment
        fields = [
            'title', 'description', 'hypothesis', 'methodology',
            'start_date', 'end_date', 'status', 'project_id',
            'collaborator_ids', 'tags'
        ]

    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters long")
        return value


class ExperimentUpdateSerializer(serializers.ModelSerializer):
    collaborator_ids = serializers.ListField(child=serializers.IntegerField(), required=False)
    tags = serializers.ListField(child=serializers.CharField(), required=False)

    class Meta:
        model = Experiment
        fields = [
            'title', 'description', 'hypothesis', 'methodology',
            'start_date', 'end_date', 'status', 'collaborator_ids',
            'tags', 'is_active'
        ]
