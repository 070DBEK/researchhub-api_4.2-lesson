from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'actor', 'verb', 'target_type', 'is_read', 'created_at']
    list_filter = ['verb', 'is_read', 'created_at']
    search_fields = ['recipient__email', 'actor__email', 'message']
    readonly_fields = ['created_at']
