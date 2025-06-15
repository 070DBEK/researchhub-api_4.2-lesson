from django.urls import path
from . import views


urlpatterns = [
    # Individual comment operations
    path('<int:pk>/', views.CommentDetailView.as_view(), name='comment-detail'),

    # Finding comments
    path('findings/<int:finding_id>/', views.FindingCommentListCreateView.as_view(),
         name='finding-comment-list-create'),

    # Publication comments
    path('publications/<int:publication_id>/', views.PublicationCommentListCreateView.as_view(),
         name='publication-comment-list-create'),
]
