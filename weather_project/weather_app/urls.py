from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('history/', views.history, name='history'),
    path('api/search_stats/', views.search_stats, name='search_stats'),
]