from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Experiment(models.Model):
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('inconclusive', 'Inconclusive'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    hypothesis = models.TextField()
    methodology = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='experiments')
    lead_researcher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='led_experiments')
    collaborators = models.ManyToManyField(User, blank=True, related_name='collaborated_experiments')
    tags = models.ManyToManyField('tags.Tag', blank=True, related_name='experiments')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_experiments')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_experiments')

    class Meta:
        db_table = 'experiments'
        ordering = ['-created_at']

    @property
    def findings_count(self):
        return self.findings.filter(is_active=True).count()

    def __str__(self):
        return self.title
