from django.contrib import admin
from .models import Project, ProjectMember

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'principal_investigator', 'status', 'visibility', 'start_date', 'is_active']
    list_filter = ['status', 'visibility', 'is_active', 'start_date']
    search_fields = ['title', 'description', 'principal_investigator__email']
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['tags']

@admin.register(ProjectMember)
class ProjectMemberAdmin(admin.ModelAdmin):
    list_display = ['user', 'project', 'role', 'is_active', 'joined_at']
    list_filter = ['role', 'is_active', 'joined_at']
    search_fields = ['user__email', 'project__title']
