from rest_framework import serializers
from .models import Publication
from apps.users.serializers import UserSerializer
from apps.projects.serializers import ProjectSerializer


class PublicationSerializer(serializers.ModelSerializer):
    authors = UserSerializer(many=True, read_only=True)
    project = ProjectSerializer(read_only=True)
    findings = serializers.SerializerMethodField()
    citation = serializers.ReadOnlyField()
    tags = serializers.SerializerMethodField()
    created_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)

    class Meta:
        model = Publication
        fields = [
            'id', 'title', 'abstract', 'authors', 'journal', 'conference',
            'publication_date', 'doi', 'url', 'citation', 'status',
            'project', 'findings', 'citations_count', 'views_count',
            'downloads_count', 'tags', 'is_active', 'created_at',
            'updated_at', 'created_by', 'updated_by'
        ]
        read_only_fields = [
            'id', 'citation', 'citations_count', 'views_count',
            'downloads_count', 'is_active', 'created_at', 'updated_at',
            'created_by', 'updated_by'
        ]

    def get_findings(self, obj):
        from apps.findings.serializers import FindingSerializer
        return FindingSerializer(obj.findings.all(), many=True).data

    def get_tags(self, obj):
        return [tag.name for tag in obj.tags.all()]


class PublicationCreateSerializer(serializers.ModelSerializer):
    author_ids = serializers.ListField(child=serializers.IntegerField())
    project_id = serializers.IntegerField()
    finding_ids = serializers.ListField(child=serializers.IntegerField(), required=False)
    tags = serializers.ListField(child=serializers.CharField(), required=False)

    class Meta:
        model = Publication
        fields = [
            'title', 'abstract', 'author_ids', 'journal', 'conference',
            'publication_date', 'doi', 'url', 'status', 'project_id',
            'finding_ids', 'tags'
        ]

    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters long")
        return value

    def validate_abstract(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("Abstract must be at least 10 characters long")
        return value


class PublicationUpdateSerializer(serializers.ModelSerializer):
    author_ids = serializers.ListField(child=serializers.IntegerField(), required=False)
    finding_ids = serializers.ListField(child=serializers.IntegerField(), required=False)
    tags = serializers.ListField(child=serializers.CharField(), required=False)

    class Meta:
        model = Publication
        fields = [
            'title', 'abstract', 'author_ids', 'journal', 'conference',
            'publication_date', 'doi', 'url', 'status', 'finding_ids',
            'tags', 'is_active'
        ]
