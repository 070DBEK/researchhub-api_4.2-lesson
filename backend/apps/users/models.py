from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Custom User model with email as the unique identifier."""

    POSITION_CHOICES = [
        ('professor', 'Professor'),
        ('associate_professor', 'Associate Professor'),
        ('assistant_professor', 'Assistant Professor'),
        ('postdoc', 'Postdoc'),
        ('phd_student', 'PhD Student'),
        ('masters_student', 'Masters Student'),
        ('researcher', 'Researcher'),
        ('lab_technician', 'Lab Technician'),
        ('other', 'Other'),
    ]

    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('moderator', 'Moderator'),
        ('researcher', 'Researcher'),
    ]

    username = None
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    institution = models.CharField(max_length=255, blank=True, null=True)
    department = models.CharField(max_length=255, blank=True, null=True)
    position = models.CharField(max_length=50, choices=POSITION_CHOICES, blank=True, null=True)
    orcid_id = models.CharField(max_length=19, blank=True, null=True, help_text="Format: 0000-0000-0000-0000")
    is_verified = models.BooleanField(default=False)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='researcher')
    citation_count = models.IntegerField(default=0)
    h_index = models.IntegerField(default=0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def profile_url(self):
        return f"/api/v1/profiles/{self.id}/"

    def __str__(self):
        return self.email


class Profile(models.Model):
    """Extended profile information for users."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    research_interests = models.JSONField(default=list, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    google_scholar = models.URLField(blank=True, null=True)
    researchgate = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile for {self.user.email}"

    @property
    def followers_count(self):
        return self.user.followers.count()

    @property
    def following_count(self):
        return self.user.following.count()

    @property
    def projects_count(self):
        return self.user.project_members.filter(is_active=True).count()

    @property
    def publications_count(self):
        return self.user.publication_authors.filter(is_active=True).count()


class Follow(models.Model):
    """Model to track user following relationships."""

    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followed')
        constraints = [
            models.CheckConstraint(
                check=~models.Q(follower=models.F('followed')),
                name='cannot_follow_self'
            )
        ]

    def __str__(self):
        return f"{self.follower.email} follows {self.followed.email}"


class Message(models.Model):
    """Direct messages between users."""

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.CheckConstraint(
                check=~models.Q(sender=models.F('recipient')),
                name='cannot_message_self'
            )
        ]

    def __str__(self):
        return f"Message from {self.sender.email} to {self.recipient.email}"


class Notification(models.Model):
    """User notifications for various events."""

    VERB_CHOICES = [
        ('followed', 'Followed'),
        ('liked', 'Liked'),
        ('commented', 'Commented'),
        ('mentioned', 'Mentioned'),
        ('invited', 'Invited'),
        ('joined', 'Joined'),
        ('published', 'Published'),
        ('updated', 'Updated'),
    ]

    TARGET_TYPE_CHOICES = [
        ('profile', 'Profile'),
        ('finding', 'Finding'),
        ('publication', 'Publication'),
        ('comment', 'Comment'),
        ('project', 'Project'),
        ('experiment', 'Experiment'),
        ('research_group', 'Research Group'),
    ]

    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    actor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='actions', null=True, blank=True)
    verb = models.CharField(max_length=20, choices=VERB_CHOICES)
    target_type = models.CharField(max_length=20, choices=TARGET_TYPE_CHOICES)
    target_id = models.PositiveIntegerField()
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'is_read']),
            models.Index(fields=['target_type', 'target_id']),
        ]

    def __str__(self):
        return f"Notification for {self.recipient.email}: {self.message}"