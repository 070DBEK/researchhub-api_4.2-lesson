from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Attachment(models.Model):
    FILE_TYPE_CHOICES = [
        ('document', 'Document'),
        ('image', 'Image'),
        ('dataset', 'Dataset'),
        ('code', 'Code'),
        ('video', 'Video'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    file_type = models.CharField(max_length=20, choices=FILE_TYPE_CHOICES)
    file_url = models.URLField()
    file_size = models.PositiveIntegerField(help_text="File size in bytes")
    content_type = models.CharField(max_length=100)
    finding = models.ForeignKey('findings.Finding', on_delete=models.CASCADE, related_name='attachments')
    experiment = models.ForeignKey('experiments.Experiment', on_delete=models.CASCADE, null=True, blank=True,
                                   related_name='attachments')
    downloads_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_attachments')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_attachments')

    class Meta:
        db_table = 'attachments'
        ordering = ['-created_at']

    @property
    def project(self):
        return self.finding.experiment.project

    def __str__(self):
        return self.title
