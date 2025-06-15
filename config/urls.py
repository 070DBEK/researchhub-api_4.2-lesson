"""
URL configuration for ResearchHub project.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    path('admins/', admin.site.urls),

    path('api/v1/auth/', include('apps.users.urls')),

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

    path('api/v1/', include('apps.likes.urls')),

    path('api/v1/comments/', include('apps.comments.urls')),

    path('api/v1/attachments/', include('apps.attachments.urls')),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
