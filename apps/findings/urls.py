from django.urls import path
from . import views


urlpatterns = [
    path('', views.FindingListCreateView.as_view(), name='finding-list-create'),
    path('<int:pk>/', views.FindingDetailView.as_view(), name='finding-detail'),
]
