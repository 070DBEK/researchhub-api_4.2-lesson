"""
URL configuration for ResearchHub project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentication
    path('api/v1/auth/', include('apps.users.urls')),

    # Core APIs
    path('api/v1/users/', include('apps.users.urls')),
    path('api/v1/profiles/', include('apps.profiles.urls')),
    path('api/v1/research-groups/', include('apps.research_groups.urls')),
    path('api/v1/projects/', include('apps.projects.urls')),
    path('api/v1/experiments/', include('apps.experiments.urls')),
    path('api/v1/findings/', include('apps.findings.urls')),
    path('api/v1/publications/', include('apps.publications.urls')),
    path('api/v1/messages/', include('apps.messages.urls')),
    path('api/v1/notifications/', include('apps.notifications.urls')),
    path('api/v1/analytics/', include('apps.analytics.urls')),
    path('api/v1/tags/', include('apps.tags.urls')),

    # Likes
    path('api/v1/', include('apps.likes.urls')),

    # Comments
    path('api/v1/comments/', include('apps.comments.urls')),

    # Attachments
    path('api/v1/attachments/', include('apps.attachments.urls')),

    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
