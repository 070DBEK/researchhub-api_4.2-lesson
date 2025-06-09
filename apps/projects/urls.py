from django.urls import path
from . import views


urlpatterns = [
    path('', views.ProjectListCreateView.as_view(), name='project-list-create'),
    path('<int:pk>/', views.ProjectDetailView.as_view(), name='project-detail'),
    path('<int:project_id>/members/', views.ProjectMemberListCreateView.as_view(), name='project-member-list-create'),
    path('<int:project_id>/members/<int:member_id>/', views.ProjectMemberDetailView.as_view(), name='project-member-detail'),
]
