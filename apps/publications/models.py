from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Publication(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('in_review', 'In Review'),
        ('accepted', 'Accepted'),
        ('published', 'Published'),
        ('rejected', 'Rejected'),
    ]

    title = models.CharField(max_length=300)
    abstract = models.TextField()
    authors = models.ManyToManyField(User, related_name='authored_publications')
    journal = models.CharField(max_length=255, blank=True, null=True)
    conference = models.CharField(max_length=255, blank=True, null=True)
    publication_date = models.DateField(blank=True, null=True)
    doi = models.CharField(max_length=255, blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='publications')
    findings = models.ManyToManyField('findings.Finding', blank=True, related_name='publications')
    citations_count = models.PositiveIntegerField(default=0)
    views_count = models.PositiveIntegerField(default=0)
    downloads_count = models.PositiveIntegerField(default=0)
    tags = models.ManyToManyField('tags.Tag', blank=True, related_name='publications')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_publications')
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='updated_publications')

    class Meta:
        db_table = 'publications'
        ordering = ['-created_at']

    @property
    def citation(self):
        authors_str = ", ".join([author.full_name for author in self.authors.all()[:3]])
        if self.authors.count() > 3:
            authors_str += " et al."

        year = self.publication_date.year if self.publication_date else "n.d."
        venue = self.journal or self.conference or "Unpublished"

        return f"{authors_str} ({year}). {self.title}. {venue}."

    def __str__(self):
        return self.title
