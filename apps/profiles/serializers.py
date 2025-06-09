from rest_framework import serializers
from .models import Profile, Follow
from apps.users.serializers import UserSerializer


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()
    projects_count = serializers.ReadOnlyField()
    publications_count = serializers.ReadOnlyField()

    class Meta:
        model = Profile
        fields = [
            'id', 'user', 'bio', 'research_interests', 'avatar',
            'website', 'google_scholar', 'researchgate', 'linkedin',
            'twitter', 'followers_count', 'following_count',
            'projects_count', 'publications_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'bio', 'research_interests', 'avatar', 'website',
            'google_scholar', 'researchgate', 'linkedin', 'twitter'
        ]
