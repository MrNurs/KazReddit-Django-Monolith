from django.urls import path
from django.contrib.auth.views import LoginView
from . import views
from .views import logout_view

app_name = 'core'
urlpatterns = [
    path('', views.SubredditView.as_view(), name='index'),
    path('login/', LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('<str:subreddit_name>/', views.PostView.as_view(), name='posts'),
    path('<str:subreddit_name>/post/<int:post_id>/', views.PostDetailView.as_view(), name='post'),

]