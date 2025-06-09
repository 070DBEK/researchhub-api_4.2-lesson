from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .models import Profile, Follow
from .serializers import ProfileSerializer, ProfileUpdateSerializer
from apps.users.serializers import UserSerializer

User = get_user_model()


class ProfileDetailView(generics.RetrieveAPIView):
    """Get user profile by user ID"""
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        user_id = self.kwargs['user_id']
        user = get_object_or_404(User, id=user_id)
        profile, created = Profile.objects.get_or_create(user=user)
        return profile


class CurrentProfileView(generics.RetrieveUpdateAPIView):
    """Get and update current user's profile"""
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return ProfileUpdateSerializer
        return ProfileSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request, user_id):
    """Follow a user"""
    if request.user.id == user_id:
        return Response(
            {'detail': 'Cannot follow yourself'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user_to_follow = get_object_or_404(User, id=user_id)
    follow, created = Follow.objects.get_or_create(
        follower=request.user,
        following=user_to_follow
    )

    if not created:
        return Response(
            {'detail': 'Already following this user'},
            status=status.HTTP_400_BAD_REQUEST
        )

    profile, _ = Profile.objects.get_or_create(user=user_to_follow)
    return Response(ProfileSerializer(profile).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfollow_user(request, user_id):
    """Unfollow a user"""
    if request.user.id == user_id:
        return Response(
            {'detail': 'Cannot unfollow yourself'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user_to_unfollow = get_object_or_404(User, id=user_id)
    try:
        follow = Follow.objects.get(
            follower=request.user,
            following=user_to_unfollow
        )
        follow.delete()

        profile, _ = Profile.objects.get_or_create(user=user_to_unfollow)
        return Response(ProfileSerializer(profile).data)
    except Follow.DoesNotExist:
        return Response(
            {'detail': 'Not following this user'},
            status=status.HTTP_400_BAD_REQUEST
        )


class UserFollowersView(generics.ListAPIView):
    """Get user's followers"""
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = get_object_or_404(User, id=user_id)
        return User.objects.filter(following__following=user)


class UserFollowingView(generics.ListAPIView):
    """Get users followed by user"""
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = get_object_or_404(User, id=user_id)
        return User.objects.filter(followers__follower=user)
