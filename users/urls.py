from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('', views.index, name='index'),
    path('profile', views.fetch_user_details, name='user_profile'),
    path('profile/<str:username>', views.fetch_user_details, name='profile'),
    path('login', views.login_user, name='login'),
    path('register', views.register_user, name='register'),
    path('logout', views.logout_user, name='logout'),
    path('delete', views.delete_news, name='delete')
]
