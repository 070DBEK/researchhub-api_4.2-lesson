from django.urls import path
from . import views


urlpatterns = [
    path('', views.ExperimentListCreateView.as_view(), name='experiment-list-create'),
    path('<int:pk>/', views.ExperimentDetailView.as_view(), name='experiment-detail'),
]
