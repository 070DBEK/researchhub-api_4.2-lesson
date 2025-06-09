from django.urls import path
from . import views

urlpatterns = [
    path('<int:user_id>/', views.ProfileDetailView.as_view(), name='profile-detail'),
    path('me/', views.CurrentProfileView.as_view(), name='current-profile'),
    path('<int:user_id>/follow/', views.follow_user, name='follow-user'),
    path('<int:user_id>/unfollow/', views.unfollow_user, name='unfollow-user'),
    path('<int:user_id>/followers/', views.UserFollowersView.as_view(), name='user-followers'),
    path('<int:user_id>/following/', views.UserFollowingView.as_view(), name='user-following'),
]
