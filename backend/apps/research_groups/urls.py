from django.urls import path
from .views import (
    ResearchGroupListCreateView, ResearchGroupDetailView,
    ResearchGroupMemberListCreateView, ResearchGroupMemberDetailView
)

urlpatterns = [
    path('', ResearchGroupListCreateView.as_view(), name='research_group_list_create'),
    path('<int:pk>/', ResearchGroupDetailView.as_view(), name='research_group_detail'),
    path('<int:group_id>/members/', ResearchGroupMemberListCreateView.as_view(), name='research_group_member_list_create'),
    path('<int:group_id>/members/<int:member_id>/', ResearchGroupMemberDetailView.as_view(), name='research_group_member_detail'),
]