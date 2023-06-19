from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.index, name='index'),
    path('featured/<str:slug>', views.featured_news_detail, name='featured_news_detail'),
    path('search', views.search, name='search'),
    path('community', views.community_news, name='community')
]

