from rest_framework import serializers
from .models import Comment
from apps.users.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    parent = serializers.SerializerMethodField()
    finding = serializers.SerializerMethodField()
    publication = serializers.SerializerMethodField()
    replies_count = serializers.ReadOnlyField()
    likes_count = serializers.ReadOnlyField()

    class Meta:
        model = Comment
        fields = [
            'id', 'content', 'parent', 'finding', 'publication',
            'author', 'replies_count', 'likes_count', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'author', 'replies_count', 'likes_count',
            'is_active', 'created_at', 'updated_at'
        ]

    def get_parent(self, obj):
        if obj.parent:
            return CommentSerializer(obj.parent).data
        return None

    def get_finding(self, obj):
        if obj.finding:
            from apps.findings.serializers import FindingSerializer
            return FindingSerializer(obj.finding).data
        return None

    def get_publication(self, obj):
        if obj.publication:
            from apps.publications.serializers import PublicationSerializer
            return PublicationSerializer(obj.publication).data
        return None


class CommentCreateSerializer(serializers.ModelSerializer):
    parent_id = serializers.IntegerField(required=False, allow_null=True)
    finding_id = serializers.IntegerField(required=False, allow_null=True)
    publication_id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = Comment
        fields = ['content', 'parent_id', 'finding_id', 'publication_id']

    def validate(self, attrs):
        finding_id = attrs.get('finding_id')
        publication_id = attrs.get('publication_id')

        if not finding_id and not publication_id:
            raise serializers.ValidationError("Either finding_id or publication_id must be provided")

        if finding_id and publication_id:
            raise serializers.ValidationError("Cannot comment on both finding and publication")

        return attrs


class CommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content', 'is_active']
