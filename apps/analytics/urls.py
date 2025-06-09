from django.urls import path
from . import views


urlpatterns = [
    path('summary/', views.analytics_summary, name='analytics-summary'),
    path('user-activities/', views.UserActivityListView.as_view(), name='user-activity-list'),
]
