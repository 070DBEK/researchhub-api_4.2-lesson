from django.contrib import admin
from .models import Publication


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'publication_date', 'citations_count', 'is_active']
    list_filter = ['status', 'is_active', 'publication_date']
    search_fields = ['title', 'abstract', 'journal', 'conference']
    readonly_fields = ['citation', 'citations_count', 'views_count', 'downloads_count', 'created_at', 'updated_at']
    filter_horizontal = ['authors', 'findings', 'tags']
