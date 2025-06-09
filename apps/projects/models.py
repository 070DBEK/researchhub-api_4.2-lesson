from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Project(models.Model):
    STATUS_CHOICES = [
        ('planning', 'Planning'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
        ('cancelled', 'Cancelled'),
    ]

    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
        ('restricted', 'Restricted'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    short_description = models.CharField(max_length=500)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES)
    funding_source = models.CharField(max_length=255, blank=True, null=True)
    funding_amount = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    funding_currency = models.CharField(max_length=3, blank=True, null=True)
    research_group = models.ForeignKey(
        'research_groups.ResearchGroup',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='projects'
    )
    principal_investigator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='led_projects'
    )
    tags = models.ManyToManyField('tags.Tag', blank=True, related_name='projects')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_projects')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_projects')

    class Meta:
        db_table = 'projects'
        ordering = ['-created_at']

    @property
    def members_count(self):
        return self.members.filter(is_active=True).count()

    @property
    def experiments_count(self):
        return self.experiments.filter(is_active=True).count()

    @property
    def findings_count(self):
        return sum(exp.findings.filter(is_active=True).count() for exp in self.experiments.all())

    @property
    def publications_count(self):
        return self.publications.filter(is_active=True).count()

    def __str__(self):
        return self.title


class ProjectMember(models.Model):
    ROLE_CHOICES = [
        ('principal_investigator', 'Principal Investigator'),
        ('co_investigator', 'Co-Investigator'),
        ('researcher', 'Researcher'),
        ('student', 'Student'),
        ('advisor', 'Advisor'),
        ('collaborator', 'Collaborator'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_memberships')
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)
    joined_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'project_members'
        unique_together = ['project', 'user']

    def __str__(self):
        return f"{self.user.full_name} - {self.project.title} ({self.role})"
