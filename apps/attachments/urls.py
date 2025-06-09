from django.urls import path
from . import views


urlpatterns = [
    path('<int:pk>/', views.AttachmentDetailView.as_view(), name='attachment-detail'),
]
