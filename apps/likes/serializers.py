from rest_framework import serializers
from .models import Like
from apps.users.serializers import UserSerializer


class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    finding = serializers.SerializerMethodField()
    publication = serializers.SerializerMethodField()
    comment = serializers.SerializerMethodField()

    class Meta:
        model = Like
        fields = ['id', 'user', 'finding', 'publication', 'comment', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

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

    def get_comment(self, obj):
        if obj.comment:
            from apps.comments.serializers import CommentSerializer
            return CommentSerializer(obj.comment).data
        return None
