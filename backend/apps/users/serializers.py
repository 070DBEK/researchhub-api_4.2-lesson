from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils import timezone
from .models import Profile, Follow, Message, Notification
import re

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password_confirm', 'first_name', 'last_name',
                  'institution', 'department', 'position', 'orcid_id')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate_orcid_id(self, value):
        if value:
            pattern = r'^[0-9]{4}-[0-9]{4}-[0-9]{4}-[0-9]{3}[0-9X]$'
            if not re.match(pattern, value):
                raise serializers.ValidationError("ORCID ID must be in format: 0000-0000-0000-0000")
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)

        # Create profile for user
        Profile.objects.create(user=user)

        return user


class UserLoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email
        token['role'] = user.role
        token['full_name'] = user.full_name

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # Add user data to response
        data['user'] = UserSerializer(self.user).data

        return data


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)
    profile_url = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'full_name', 'institution',
                  'department', 'position', 'orcid_id', 'is_active', 'is_staff',
                  'is_verified', 'date_joined', 'role', 'citation_count', 'h_index',
                  'profile_url')
        read_only_fields = ('id', 'email', 'is_active', 'is_staff', 'is_verified',
                            'date_joined', 'role', 'citation_count', 'h_index')


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    followers_count = serializers.IntegerField(read_only=True)
    following_count = serializers.IntegerField(read_only=True)
    projects_count = serializers.IntegerField(read_only=True)
    publications_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Profile
        fields = ('id', 'user', 'bio', 'research_interests', 'avatar', 'website',
                  'google_scholar', 'researchgate', 'linkedin', 'twitter',
                  'followers_count', 'following_count', 'projects_count',
                  'publications_count', 'created_at', 'updated_at')
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('bio', 'research_interests', 'avatar', 'website', 'google_scholar',
                  'researchgate', 'linkedin', 'twitter')


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    recipient = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ('id', 'sender', 'recipient', 'content', 'is_read', 'read_at', 'created_at')
        read_only_fields = ('id', 'sender', 'is_read', 'read_at', 'created_at')


class MessageCreateSerializer(serializers.ModelSerializer):
    recipient_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Message
        fields = ('content', 'recipient_id')

    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message content cannot be empty.")
        return value.strip()

    def validate_recipient_id(self, value):
        try:
            recipient = User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Recipient not found.")

        # Check if trying to send message to self
        if self.context['request'].user.id == value:
            raise serializers.ValidationError("Cannot send message to yourself.")

        return value

    def create(self, validated_data):
        recipient_id = validated_data.pop('recipient_id')
        sender = self.context['request'].user

        message = Message.objects.create(
            sender=sender,
            recipient_id=recipient_id,
            **validated_data
        )

        # Create notification for recipient
        Notification.objects.create(
            recipient_id=recipient_id,
            actor=sender,
            verb='mentioned',
            target_type='profile',
            target_id=sender.id,
            message=f"{sender.full_name} sent you a message."
        )

        return message


class NotificationSerializer(serializers.ModelSerializer):
    recipient = UserSerializer(read_only=True)
    actor = UserSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = ('id', 'recipient', 'actor', 'verb', 'target_type', 'target_id',
                  'message', 'is_read', 'read_at', 'created_at')
        read_only_fields = ('id', 'recipient', 'actor', 'verb', 'target_type',
                            'target_id', 'message', 'is_read', 'read_at', 'created_at')


class EmailVerificationSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=255)


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            User.objects.get(email=value)
        except User.DoesNotExist:
            # Don't reveal if email exists or not for security
            pass
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=255)
    password = serializers.CharField(validators=[validate_password])
    password_confirm = serializers.CharField()

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs


class TokenRefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class TokenResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = UserSerializer()