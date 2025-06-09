from django.contrib import admin
from .models import Like


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'target_type', 'target_title', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__email']

    def target_type(self, obj):
        if obj.finding:
            return 'Finding'
        elif obj.publication:
            return 'Publication'
        elif obj.comment:
            return 'Comment'
        return 'Unknown'

    def target_title(self, obj):
        if obj.finding:
            return obj.finding.title
        elif obj.publication:
            return obj.publication.title
        elif obj.comment:
            return obj.comment.content[:50]
        return 'Unknown'
