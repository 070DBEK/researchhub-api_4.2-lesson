from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db import models
from .models import Profile, Follow, Message, Notification
from .serializers import (
    UserCreateSerializer, UserLoginSerializer, UserSerializer,
    ProfileSerializer, ProfileUpdateSerializer,
    MessageSerializer, MessageCreateSerializer, NotificationSerializer,
    EmailVerificationSerializer, PasswordResetSerializer, PasswordResetConfirmSerializer
)

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """Register a new user."""
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Return user data without tokens for registration
        user_serializer = UserSerializer(user)
        return Response(user_serializer.data, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    """Login user and return JWT tokens."""
    serializer_class = UserLoginSerializer


class LogoutView(APIView):
    """Logout user by blacklisting refresh token."""
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response(
                    {"detail": "Refresh token is required."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"detail": "Successfully logged out."},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"detail": "Invalid token."},
                status=status.HTTP_400_BAD_REQUEST
            )


class CurrentUserView(generics.RetrieveAPIView):
    """Get current user profile."""
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class UserDetailView(generics.RetrieveAPIView):
    """Get user by ID."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)


class ProfileDetailView(generics.RetrieveAPIView):
    """Get user profile by user ID."""
    serializer_class = ProfileSerializer
    permission_classes = (permissions.AllowAny,)
    lookup_url_kwarg = 'user_id'

    def get_object(self):
        user_id = self.kwargs.get(self.lookup_url_kwarg)
        return get_object_or_404(Profile, user_id=user_id)


class CurrentProfileView(generics.RetrieveUpdateAPIView):
    """Get and update current user's profile."""
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ProfileUpdateSerializer
        return ProfileSerializer


class FollowUserView(APIView):
    """Follow a user."""
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, user_id):
        if int(user_id) == request.user.id:
            return Response(
                {"detail": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user_to_follow = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        follow, created = Follow.objects.get_or_create(
            follower=request.user,
            followed=user_to_follow
        )

        if created:
            # Create notification
            Notification.objects.create(
                recipient=user_to_follow,
                actor=request.user,
                verb='followed',
                target_type='profile',
                target_id=user_to_follow.id,
                message=f"{request.user.full_name} started following you."
            )

        profile = get_object_or_404(Profile, user=user_to_follow)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UnfollowUserView(APIView):
    """Unfollow a user."""
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, user_id):
        if int(user_id) == request.user.id:
            return Response(
                {"detail": "You cannot unfollow yourself."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user_to_unfollow = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        follow = Follow.objects.filter(
            follower=request.user,
            followed=user_to_unfollow
        ).first()

        if follow:
            follow.delete()

        profile = get_object_or_404(Profile, user=user_to_unfollow)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserFollowersListView(generics.ListAPIView):
    """Get user's followers."""
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        # Verify user exists
        get_object_or_404(User, id=user_id)
        return User.objects.filter(following__followed_id=user_id)


class UserFollowingListView(generics.ListAPIView):
    """Get users followed by user."""
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        # Verify user exists
        get_object_or_404(User, id=user_id)
        return User.objects.filter(followers__follower_id=user_id)


class MessageListView(generics.ListAPIView):
    """List messages for current user."""
    serializer_class = MessageSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        user_id = self.request.query_params.get('user_id')
        is_read = self.request.query_params.get('is_read')

        # Base queryset - messages where user is sender or recipient
        queryset = Message.objects.filter(
            models.Q(sender=user) | models.Q(recipient=user)
        )

        # Filter by conversation with specific user
        if user_id:
            try:
                other_user = User.objects.get(id=user_id)
                queryset = queryset.filter(
                    (models.Q(sender=user) & models.Q(recipient=other_user)) |
                    (models.Q(sender=other_user) & models.Q(recipient=user))
                )
            except User.DoesNotExist:
                queryset = queryset.none()

        # Filter by read status (only for received messages)
        if is_read is not None:
            is_read_bool = is_read.lower() == 'true'
            queryset = queryset.filter(recipient=user, is_read=is_read_bool)

        return queryset.order_by('-created_at')


class MessageCreateView(generics.CreateAPIView):
    """Send a message."""
    serializer_class = MessageCreateSerializer
    permission_classes = (permissions.IsAuthenticated,)


class MessageMarkAsReadView(APIView):
    """Mark message as read."""
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, id):
        try:
            message = Message.objects.get(id=id, recipient=request.user)
        except Message.DoesNotExist:
            return Response(
                {"detail": "Message not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        if not message.is_read:
            message.is_read = True
            message.read_at = timezone.now()
            message.save()

        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_200_OK)


class NotificationListView(generics.ListAPIView):
    """List notifications for current user."""
    serializer_class = NotificationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        is_read = self.request.query_params.get('is_read')
        verb = self.request.query_params.get('verb')

        queryset = Notification.objects.filter(recipient=user)

        if is_read is not None:
            is_read_bool = is_read.lower() == 'true'
            queryset = queryset.filter(is_read=is_read_bool)

        if verb:
            queryset = queryset.filter(verb=verb)

        return queryset.order_by('-created_at')


class NotificationMarkAsReadView(APIView):
    """Mark notification as read."""
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, id):
        try:
            notification = Notification.objects.get(id=id, recipient=request.user)
        except Notification.DoesNotExist:
            return Response(
                {"detail": "Notification not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        if not notification.is_read:
            notification.is_read = True
            notification.read_at = timezone.now()
            notification.save()

        serializer = NotificationSerializer(notification)
        return Response(serializer.data, status=status.HTTP_200_OK)


class NotificationMarkAllAsReadView(APIView):
    """Mark all notifications as read."""
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        updated_count = Notification.objects.filter(
            recipient=request.user,
            is_read=False
        ).update(
            is_read=True,
            read_at=timezone.now()
        )

        return Response(
            {"detail": f"Marked {updated_count} notifications as read."},
            status=status.HTTP_200_OK
        )


class EmailVerificationView(APIView):
    """Verify user email."""
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = EmailVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # In a real implementation, you would:
        # 1. Decode and verify the token
        # 2. Find the user associated with the token
        # 3. Mark the user as verified
        # 4. Handle expired tokens

        return Response(
            {"detail": "Email verified successfully."},
            status=status.HTTP_200_OK
        )


class PasswordResetView(APIView):
    """Request password reset."""
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # In a real implementation, you would:
        # 1. Generate a secure token
        # 2. Send password reset email
        # 3. Store token with expiration

        return Response(
            {"detail": "Password reset email sent."},
            status=status.HTTP_200_OK
        )


class PasswordResetConfirmView(APIView):
    """Confirm password reset."""
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # In a real implementation, you would:
        # 1. Verify the token
        # 2. Find the user associated with the token
        # 3. Update the user's password
        # 4. Invalidate the token

        return Response(
            {"detail": "Password reset successful."},
            status=status.HTTP_200_OK
        )