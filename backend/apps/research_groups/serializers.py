from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ResearchGroup, ResearchGroupMember
from apps.users.serializers import UserSerializer

User = get_user_model()


class ResearchGroupSerializer(serializers.ModelSerializer):
    leader = UserSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)
    members_count = serializers.IntegerField(read_only=True)
    projects_count = serializers.IntegerField(read_only=True)
    publications_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = ResearchGroup
        fields = ('id', 'name', 'description', 'institution', 'department', 'website',
                  'logo', 'leader', 'members_count', 'projects_count', 'publications_count',
                  'is_active', 'created_at', 'updated_at', 'created_by', 'updated_by')
        read_only_fields = ('id', 'leader', 'is_active', 'created_at', 'updated_at',
                            'created_by', 'updated_by')


class ResearchGroupCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResearchGroup
        fields = ('name', 'description', 'institution', 'department', 'website', 'logo')

    def create(self, validated_data):
        user = self.context['request'].user

        research_group = ResearchGroup.objects.create(
            created_by=user,
            updated_by=user,
            **validated_data
        )

        # Add the creator as the leader
        ResearchGroupMember.objects.create(
            group=research_group,
            user=user,
            role='leader'
        )

        return research_group


class ResearchGroupUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResearchGroup
        fields = ('name', 'description', 'institution', 'department', 'website', 'logo')

    def update(self, instance, validated_data):
        user = self.context['request'].user
        validated_data['updated_by'] = user

        return super().update(instance, validated_data)


class ResearchGroupMemberSerializer(serializers.ModelSerializer):
    group = ResearchGroupSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = ResearchGroupMember
        fields = ('id', 'group', 'user', 'role', 'joined_at', 'is_active',
                  'created_at', 'updated_at')
        read_only_fields = ('id', 'group', 'user', 'joined_at', 'created_at', 'updated_at')


class ResearchGroupMemberCreateSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()

    class Meta:
        model = ResearchGroupMember
        fields = ('user_id', 'role')

    def validate(self, attrs):
        user_id = attrs['user_id']
        group = self.context['group']

        # Check if user exists
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError({"user_id": "User not found."})

        # Check if user is already a member
        if ResearchGroupMember.objects.filter(group=group, user_id=user_id).exists():
            raise serializers.ValidationError({"user_id": "User is already a member of this group."})

        return attrs

    def create(self, validated_data):
        user_id = validated_data.pop('user_id')
        group = self.context['group']

        member = ResearchGroupMember.objects.create(
            group=group,
            user_id=user_id,
            **validated_data
        )

        return member


class ResearchGroupMemberUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResearchGroupMember
        fields = ('role', 'is_active')