from django.urls import path
from . import views


urlpatterns = [
    path('', views.ResearchGroupListCreateView.as_view(), name='research-group-list-create'),
    path('<int:pk>/', views.ResearchGroupDetailView.as_view(), name='research-group-detail'),
    path('<int:group_id>/members/', views.ResearchGroupMemberListCreateView.as_view(), name='research-group-member-list-create'),
    path('<int:group_id>/members/<int:member_id>/', views.ResearchGroupMemberDetailView.as_view(), name='research-group-member-detail'),
]
