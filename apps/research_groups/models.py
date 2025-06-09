from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ResearchGroup(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    institution = models.CharField(max_length=255)
    department = models.CharField(max_length=255, blank=True)
    website = models.URLField(blank=True, null=True)
    logo = models.URLField(blank=True, null=True)
    leader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='led_groups')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_groups')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_groups')

    class Meta:
        db_table = 'research_groups'

    @property
    def members_count(self):
        return self.members.filter(is_active=True).count()

    @property
    def projects_count(self):
        return self.projects.filter(is_active=True).count()

    @property
    def publications_count(self):
        return sum(project.publications.filter(is_active=True).count() for project in self.projects.all())

    def __str__(self):
        return self.name


class ResearchGroupMember(models.Model):
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='group_memberships')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    joined_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'research_group_members'
        unique_together = ['group', 'user']

    def __str__(self):
        return f"{self.user.full_name} - {self.group.name} ({self.role})"
