from rest_framework import serializers
from .models import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'category', 'usage_count', 'created_at']
        read_only_fields = ['id', 'slug', 'usage_count', 'created_at']


class SearchResultSerializer(serializers.Serializer):
    users = serializers.ListField()
    research_groups = serializers.ListField()
    projects = serializers.ListField()
    experiments = serializers.ListField()
    findings = serializers.ListField()
    publications = serializers.ListField()
