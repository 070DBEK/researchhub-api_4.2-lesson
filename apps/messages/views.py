from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from django.db import models
from . import models, serializers
from .models import Message
from .serializers import MessageSerializer, MessageCreateSerializer

User = get_user_model()


class MessageListCreateView(generics.ListCreateAPIView):
    """List messages for current user or send a new message"""
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['is_read']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return MessageCreateSerializer
        return MessageSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Message.objects.filter(
            models.Q(sender=user) | models.Q(recipient=user)
        )

        # Filter by conversation with specific user
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = queryset.filter(
                models.Q(sender_id=user_id, recipient=user) |
                models.Q(sender=user, recipient_id=user_id)
            )

        return queryset

    def perform_create(self, serializer):
        recipient_id = serializer.validated_data['recipient_id']
        recipient = get_object_or_404(User, id=recipient_id)

        if recipient == self.request.user:
            raise serializers.ValidationError("Cannot send message to yourself")

        serializer.save(
            sender=self.request.user,
            recipient=recipient
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_message_as_read(request, pk):
    """Mark message as read"""
    message = get_object_or_404(Message, id=pk)

    # Check if user is the recipient
    if message.recipient != request.user:
        return Response(
            {'detail': 'Forbidden - not the recipient'},
            status=status.HTTP_403_FORBIDDEN
        )

    if not message.is_read:
        message.is_read = True
        message.read_at = timezone.now()
        message.save()

    return Response(MessageSerializer(message).data)
