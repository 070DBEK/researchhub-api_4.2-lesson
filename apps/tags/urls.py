from django.urls import path
from . import views

urlpatterns = [
    path('', views.TagListView.as_view(), name='tag-list'),
    path('search/', views.search, name='search'),
]
