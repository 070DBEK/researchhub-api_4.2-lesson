from django.urls import path
from backend.apps.users.views import CurrentUserView, UserDetailView


urlpatterns = [
    path('me/', CurrentUserView.as_view(), name='current_user'),
    path('<int:pk>/', UserDetailView.as_view(), name='user_detail'),
]