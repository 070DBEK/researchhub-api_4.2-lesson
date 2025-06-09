from django.urls import path
from . import views


urlpatterns = [
    path('', views.NotificationListView.as_view(), name='notification-list'),
    path('<int:pk>/mark-as-read/', views.mark_notification_as_read, name='mark-notification-as-read'),
    path('mark-all-as-read/', views.mark_all_notifications_as_read, name='mark-all-notifications-as-read'),
]
