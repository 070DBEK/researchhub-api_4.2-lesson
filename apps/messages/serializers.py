from rest_framework import serializers
from .models import Message
from apps.users.serializers import UserSerializer


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    recipient = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = [
            'id', 'content', 'sender', 'recipient', 'is_read',
            'read_at', 'created_at'
        ]
        read_only_fields = ['id', 'sender', 'recipient', 'is_read', 'read_at', 'created_at']


class MessageCreateSerializer(serializers.ModelSerializer):
    recipient_id = serializers.IntegerField()

    class Meta:
        model = Message
        fields = ['content', 'recipient_id']

    def validate_content(self, value):
        if len(value.strip()) == 0:
            raise serializers.ValidationError("Content cannot be empty")
        return value
