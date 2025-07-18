from django.urls import path
from . import views


urlpatterns = [
    path('<int:pk>/', views.AttachmentDetailView.as_view(), name='attachment-detail'),
    path('findings/<int:finding_id>/', views.AttachmentListCreateView.as_view(), name='finding-attachment-list-create'),
]
