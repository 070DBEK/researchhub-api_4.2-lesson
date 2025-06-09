from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Comment(models.Model):
    content = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    finding = models.ForeignKey('findings.Finding', on_delete=models.CASCADE, null=True, blank=True,
                                related_name='comments')
    publication = models.ForeignKey('publications.Publication', on_delete=models.CASCADE, null=True, blank=True,
                                    related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'comments'
        ordering = ['-created_at']

    @property
    def replies_count(self):
        return self.replies.filter(is_active=True).count()

    @property
    def likes_count(self):
        return self.likes.count()

    def __str__(self):
        return f"Comment by {self.author.full_name}"
