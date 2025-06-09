from django.urls import path
from . import views


urlpatterns = [
    # Finding likes
    path('findings/<int:pk>/like/', views.like_finding, name='like-finding'),
    path('findings/<int:pk>/unlike/', views.unlike_finding, name='unlike-finding'),

    # Publication likes
    path('publications/<int:pk>/like/', views.like_publication, name='like-publication'),
    path('publications/<int:pk>/unlike/', views.unlike_publication, name='unlike-publication'),

    # Comment likes
    path('comments/<int:pk>/like/', views.like_comment, name='like-comment'),
    path('comments/<int:pk>/unlike/', views.unlike_comment, name='unlike-comment'),
]
