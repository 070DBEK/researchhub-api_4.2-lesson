from django.urls import path
from . import views


urlpatterns = [
    path('', views.MessageListCreateView.as_view(), name='message-list-create'),
    path('<int:pk>/mark-as-read/', views.mark_message_as_read, name='mark-message-as-read'),
]
