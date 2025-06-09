from django.contrib import admin
from .models import ResearchGroup, ResearchGroupMember


@admin.register(ResearchGroup)
class ResearchGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'institution', 'leader', 'members_count', 'is_active', 'created_at']
    list_filter = ['institution', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'institution']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ResearchGroupMember)
class ResearchGroupMemberAdmin(admin.ModelAdmin):
    list_display = ['user', 'group', 'role', 'is_active', 'joined_at']
    list_filter = ['role', 'is_active', 'joined_at']
    search_fields = ['user__email', 'group__name']
