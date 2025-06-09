from rest_framework import serializers
from .models import ResearchGroup, ResearchGroupMember
from apps.users.serializers import UserSerializer


class ResearchGroupSerializer(serializers.ModelSerializer):
    leader = UserSerializer(read_only=True)
    members_count = serializers.ReadOnlyField()
    projects_count = serializers.ReadOnlyField()
    publications_count = serializers.ReadOnlyField()
    created_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)

    class Meta:
        model = ResearchGroup
        fields = [
            'id', 'name', 'description', 'institution', 'department',
            'website', 'logo', 'leader', 'members_count', 'projects_count',
            'publications_count', 'is_active', 'created_at', 'updated_at',
            'created_by', 'updated_by'
        ]
        read_only_fields = [
            'id', 'leader', 'is_active', 'created_at', 'updated_at',
            'created_by', 'updated_by'
        ]


class ResearchGroupCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResearchGroup
        fields = ['name', 'description', 'institution', 'department', 'website', 'logo']

    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Name must be at least 3 characters long")
        return value

    def validate_description(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("Description must be at least 10 characters long")
        return value


class ResearchGroupUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResearchGroup
        fields = ['name', 'description', 'institution', 'department', 'website', 'logo']


class ResearchGroupMemberSerializer(serializers.ModelSerializer):
    group = ResearchGroupSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = ResearchGroupMember
        fields = [
            'id', 'group', 'user', 'role', 'joined_at',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'joined_at', 'created_at', 'updated_at']


class ResearchGroupMemberCreateSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()

    class Meta:
        model = ResearchGroupMember
        fields = ['user_id', 'role']


class ResearchGroupMemberUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResearchGroupMember
        fields = ['role', 'is_active']
