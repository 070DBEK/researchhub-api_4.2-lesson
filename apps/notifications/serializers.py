from rest_framework import serializers
from .models import Notification
from apps.users.serializers import UserSerializer


class NotificationSerializer(serializers.ModelSerializer):
    recipient = UserSerializer(read_only=True)
    actor = UserSerializer(read_only=True)
    target_type = serializers.ReadOnlyField()
    target_id = serializers.ReadOnlyField()

    class Meta:
        model = Notification
        fields = [
            'id', 'recipient', 'actor', 'verb', 'target_type',
            'target_id', 'message', 'is_read', 'read_at', 'created_at'
        ]
        read_only_fields = [
            'id', 'recipient', 'actor', 'verb', 'target_type',
            'target_id', 'message', 'is_read', 'read_at', 'created_at'
        ]
