from rest_framework import serializers
from .models import Attachment
from apps.users.serializers import UserSerializer


class AttachmentSerializer(serializers.ModelSerializer):
    finding = serializers.SerializerMethodField()
    experiment = serializers.SerializerMethodField()
    project = serializers.SerializerMethodField()
    created_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)

    class Meta:
        model = Attachment
        fields = [
            'id', 'title', 'description', 'file_type', 'file_url',
            'file_size', 'content_type', 'finding', 'experiment',
            'project', 'downloads_count', 'is_active', 'created_at',
            'updated_at', 'created_by', 'updated_by'
        ]
        read_only_fields = [
            'id', 'file_size', 'content_type', 'downloads_count',
            'is_active', 'created_at', 'updated_at', 'created_by', 'updated_by'
        ]

    def get_finding(self, obj):
        from apps.findings.serializers import FindingSerializer
        return FindingSerializer(obj.finding).data

    def get_experiment(self, obj):
        if obj.experiment:
            from apps.experiments.serializers import ExperimentSerializer
            return ExperimentSerializer(obj.experiment).data
        return None

    def get_project(self, obj):
        from apps.projects.serializers import ProjectSerializer
        return ProjectSerializer(obj.project).data


class AttachmentCreateSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True)
    finding_id = serializers.IntegerField()
    experiment_id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = Attachment
        fields = ['title', 'description', 'file_type', 'file', 'finding_id', 'experiment_id']

    def validate_title(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters long")
        return value


class AttachmentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ['title', 'description', 'file_type', 'is_active']
