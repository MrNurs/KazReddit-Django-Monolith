from django.urls import path

from . import views

app_name = 'core'
urlpatterns = [
    path('', views.SubredditView.as_view(), name='index'),
    path('<str:subreddit_name>/', views.PostView.as_view(), name='posts'),
    path('<str:subreddit_name>/post/<int:post_id>/', views.PostDetailView.as_view(), name='post'),
]