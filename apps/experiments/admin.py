from django.contrib import admin
from .models import Experiment

@admin.register(Experiment)
class ExperimentAdmin(admin.ModelAdmin):
    list_display = ['title', 'project', 'lead_researcher', 'status', 'start_date', 'is_active']
    list_filter = ['status', 'is_active', 'start_date']
    search_fields = ['title', 'description', 'lead_researcher__email']
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['collaborators', 'tags']
