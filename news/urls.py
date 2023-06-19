from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.index, name='index'),
    path('featured/<str:slug>', views.featured_news_detail, name='featured_news_detail')
]

