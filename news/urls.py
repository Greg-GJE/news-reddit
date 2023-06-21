from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.index, name='index'),
    path('featured/<str:slug>', views.featured_news_detail,
         name='featured_news_detail'),
    path('search', views.search, name='search'),
    path('community', views.community_news, name='community'),
    path('comment', views.add_comment, name='add_comment'),
    path('create', views.create_community_news, name='create'),
    path('community/<str:slug>', views.community_detail, name='community_detail'),
    path('community/search/', views.community_search, name='community_search')
]
