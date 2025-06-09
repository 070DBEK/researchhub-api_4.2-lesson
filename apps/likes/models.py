from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    finding = models.ForeignKey('findings.Finding', on_delete=models.CASCADE, null=True, blank=True,
                                related_name='likes')
    publication = models.ForeignKey('publications.Publication', on_delete=models.CASCADE, null=True, blank=True,
                                    related_name='likes')
    comment = models.ForeignKey('comments.Comment', on_delete=models.CASCADE, null=True, blank=True,
                                related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'likes'
        unique_together = [
            ['user', 'finding'],
            ['user', 'publication'],
            ['user', 'comment']
        ]

    def __str__(self):
        target = self.finding or self.publication or self.comment
        return f"{self.user.full_name} likes {target}"
