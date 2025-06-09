from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Finding(models.Model):
    SIGNIFICANCE_CHOICES = [
        ('breakthrough', 'Breakthrough'),
        ('significant', 'Significant'),
        ('moderate', 'Moderate'),
        ('minor', 'Minor'),
        ('negative', 'Negative'),
    ]

    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
        ('restricted', 'Restricted'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    data_summary = models.TextField()
    conclusion = models.TextField()
    significance = models.CharField(max_length=20, choices=SIGNIFICANCE_CHOICES)
    experiment = models.ForeignKey('experiments.Experiment', on_delete=models.CASCADE, related_name='findings')
    visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES)
    views_count = models.PositiveIntegerField(default=0)
    citations_count = models.PositiveIntegerField(default=0)
    tags = models.ManyToManyField('tags.Tag', blank=True, related_name='findings')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_findings')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_findings')

    class Meta:
        db_table = 'findings'
        ordering = ['-created_at']

    @property
    def project(self):
        return self.experiment.project

    @property
    def attachments_count(self):
        return self.attachments.filter(is_active=True).count()

    @property
    def comments_count(self):
        return self.comments.filter(is_active=True).count()

    def __str__(self):
        return self.title
