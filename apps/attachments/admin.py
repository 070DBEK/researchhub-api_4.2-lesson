from django.contrib import admin
from .models import Attachment


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'finding', 'file_type', 'file_size', 'downloads_count', 'is_active']
    list_filter = ['file_type', 'is_active', 'created_at']
    search_fields = ['title', 'description', 'finding__title']
    readonly_fields = ['file_size', 'content_type', 'downloads_count', 'created_at', 'updated_at']
