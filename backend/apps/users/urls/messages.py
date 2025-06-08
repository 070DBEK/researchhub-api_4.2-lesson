from django.urls import path
from backend.apps.users.views import MessageListView, MessageCreateView, MessageMarkAsReadView


urlpatterns = [
    path('', MessageListView.as_view(), name='message_list'),
    path('create/', MessageCreateView.as_view(), name='message_create'),
    path('<int:id>/mark-as-read/', MessageMarkAsReadView.as_view(), name='message_mark_as_read'),
]