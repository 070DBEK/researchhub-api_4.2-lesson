from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="ResearchHub API",
        default_version='v1',
        description="API for a collaborative scientific research management platform",
        terms_of_service="https://www.researchhub.com/terms/",
        contact=openapi.Contact(email="contact@researchhub.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # API documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # API endpoints
    path('api/v1/', include([
        path('auth/', include('apps.users.urls.auth')),
        path('users/', include('apps.users.urls.users')),
        path('profiles/', include('apps.users.urls.profiles')),
        path('research-groups/', include('apps.research_groups.urls')),
        path('projects/', include('apps.projects.urls')),
        path('experiments/', include('apps.experiments.urls')),
        path('findings/', include('apps.findings.urls')),
        path('publications/', include('apps.publications.urls')),
        path('attachments/', include('apps.findings.urls_attachments')),
        path('comments/', include('apps.findings.urls_comments')),
        path('messages/', include('apps.users.urls.messages')),
        path('notifications/', include('apps.users.urls.notifications')),
        path('analytics/', include('apps.analytics.urls')),
        path('search/', include('apps.analytics.urls_search')),
        path('tags/', include('apps.analytics.urls_tags')),
        path('admin/', include('apps.analytics.urls_admin')),
    ])),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # Debug toolbar
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]