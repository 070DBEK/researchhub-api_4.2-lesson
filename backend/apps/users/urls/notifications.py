from django.urls import path
from apps.users.views import (
    NotificationListView, NotificationMarkAsReadView, NotificationMarkAllAsReadView
)

urlpatterns = [
    path('', NotificationListView.as_view(), name='notification_list'),
    path('<int:id>/mark-as-read/', NotificationMarkAsReadView.as_view(), name='notification_mark_as_read'),
    path('mark-all-as-read/', NotificationMarkAllAsReadView.as_view(), name='notification_mark_all_as_read'),
]