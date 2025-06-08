from django.db import models
from django.conf import settings


class ResearchGroup(models.Model):
    """Research group model."""

    name = models.CharField(max_length=100)
    description = models.TextField()
    institution = models.CharField(max_length=255)
    department = models.CharField(max_length=255, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to='research_groups/logos/', blank=True, null=True)
    leader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='led_research_groups',
        null=True
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='created_research_groups',
        null=True
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='updated_research_groups',
        null=True
    )

    def __str__(self):
        return self.name

    @property
    def members_count(self):
        return self.members.filter(is_active=True).count()

    @property
    def projects_count(self):
        return self.projects.filter(is_active=True).count()

    @property
    def publications_count(self):
        return sum(
            project.publications.filter(is_active=True).count() for project in self.projects.filter(is_active=True))


class ResearchGroupMember(models.Model):
    """Research group member model."""

    ROLE_CHOICES = [
        ('leader', 'Leader'),
        ('co_leader', 'Co-Leader'),
        ('senior_researcher', 'Senior Researcher'),
        ('researcher', 'Researcher'),
        ('student', 'Student'),
        ('collaborator', 'Collaborator'),
        ('alumni', 'Alumni'),
    ]

    group = models.ForeignKey(ResearchGroup, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='research_group_memberships')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    joined_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('group', 'user')

    def __str__(self):
        return f"{self.user.email} - {self.role} in {self.group.name}"

    def save(self, *args, **kwargs):
        # If this member is a leader, update the group's leader field
        if self.role == 'leader':
            self.group.leader = self.user
            self.group.save()

        super().save(*args, **kwargs)