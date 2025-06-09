from django.urls import path
from . import views


urlpatterns = [
    path('', views.PublicationListCreateView.as_view(), name='publication-list-create'),
    path('<int:pk>/', views.PublicationDetailView.as_view(), name='publication-detail'),
]
