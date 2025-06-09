from rest_framework import serializers
from .models import Finding
from apps.users.serializers import UserSerializer
from apps.experiments.serializers import ExperimentSerializer


class FindingSerializer(serializers.ModelSerializer):
    experiment = ExperimentSerializer(read_only=True)
    project = serializers.SerializerMethodField()
    attachments_count = serializers.ReadOnlyField()
    comments_count = serializers.ReadOnlyField()
    tags = serializers.StringRelatedField(many=True, read_only=True)
    created_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)

    class Meta:
        model = Finding
        fields = [
            'id', 'title', 'description', 'data_summary', 'conclusion',
            'significance', 'experiment', 'project', 'visibility',
            'attachments_count', 'comments_count', 'views_count',
            'citations_count', 'tags', 'is_active', 'created_at',
            'updated_at', 'created_by', 'updated_by'
        ]
        read_only_fields = [
            'id', 'experiment', 'views_count', 'citations_count',
            'is_active', 'created_at', 'updated_at', 'created_by', 'updated_by'
        ]

    def get_project(self, obj):
        from apps.projects.serializers import ProjectSerializer
        return ProjectSerializer(obj.project).data


class FindingCreateSerializer(serializers.ModelSerializer):
    experiment_id = serializers.IntegerField()
    tags = serializers.ListField(child=serializers.CharField(), required=False)

    class Meta:
        model = Finding
        fields = [
            'title', 'description', 'data_summary', 'conclusion',
            'significance', 'experiment_id', 'visibility', 'tags'
        ]

    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters long")
        return value


class FindingUpdateSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(child=serializers.CharField(), required=False)

    class Meta:
        model = Finding
        fields = [
            'title', 'description', 'data_summary', 'conclusion',
            'significance', 'visibility', 'tags', 'is_active'
        ]
