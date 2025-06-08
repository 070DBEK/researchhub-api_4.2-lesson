from django.urls import path
from backend.apps.users.views import (
    ProfileDetailView, CurrentProfileView,
    FollowUserView, UnfollowUserView,
    UserFollowersListView, UserFollowingListView
)

urlpatterns = [
    path('me/', CurrentProfileView.as_view(), name='current_profile'),
    path('<int:user_id>/', ProfileDetailView.as_view(), name='profile_detail'),
    path('<int:user_id>/follow/', FollowUserView.as_view(), name='follow_user'),
    path('<int:user_id>/unfollow/', UnfollowUserView.as_view(), name='unfollow_user'),
    path('<int:user_id>/followers/', UserFollowersListView.as_view(), name='user_followers'),
    path('<int:user_id>/following/', UserFollowingListView.as_view(), name='user_following'),
]