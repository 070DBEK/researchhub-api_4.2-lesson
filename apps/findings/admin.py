from django.contrib import admin
from .models import Finding


@admin.register(Finding)
class FindingAdmin(admin.ModelAdmin):
    list_display = ['title', 'experiment', 'significance', 'visibility', 'views_count', 'is_active']
    list_filter = ['significance', 'visibility', 'is_active', 'created_at']
    search_fields = ['title', 'description', 'created_by__email']
    readonly_fields = ['views_count', 'citations_count', 'created_at', 'updated_at']
    filter_horizontal = ['tags']
