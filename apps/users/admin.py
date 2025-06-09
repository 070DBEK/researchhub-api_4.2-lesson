from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, EmailVerificationToken, PasswordResetToken


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'first_name', 'last_name', 'institution', 'role', 'is_verified', 'is_active']
    list_filter = ['role', 'is_verified', 'is_active', 'position']
    search_fields = ['email', 'first_name', 'last_name', 'institution']
    ordering = ['email']

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': (
            'institution', 'department', 'position', 'orcid_id', 'is_verified', 'role', 'citation_count', 'h_index')
        }),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('email', 'first_name', 'last_name', 'institution', 'department', 'position', 'orcid_id')
        }),
    )


@admin.register(EmailVerificationToken)
class EmailVerificationTokenAdmin(admin.ModelAdmin):
    list_display = ['user', 'token', 'created_at', 'expires_at', 'is_used']
    list_filter = ['is_used', 'created_at']
    search_fields = ['user__email', 'token']


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ['user', 'token', 'created_at', 'expires_at', 'is_used']
    list_filter = ['is_used', 'created_at']
    search_fields = ['user__email', 'token']
