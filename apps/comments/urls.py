from django.urls import path
from . import views


urlpatterns = [
    path('<int:pk>/', views.CommentDetailView.as_view(), name='comment-detail'),
]
