from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

User = get_user_model()


class Notification(models.Model):
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

    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    actor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='sent_notifications')
    verb = models.CharField(max_length=20, choices=VERB_CHOICES)
    target_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    target_object_id = models.PositiveIntegerField()
    target = GenericForeignKey('target_content_type', 'target_object_id')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']

    @property
    def target_type(self):
        return self.target_content_type.model

    @property
    def target_id(self):
        return self.target_object_id

    def __str__(self):
        return f"Notification for {self.recipient.full_name}: {self.message}"
