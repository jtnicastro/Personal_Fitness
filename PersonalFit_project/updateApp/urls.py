from django.urls import path
from .import views

urlpatterns = [
    path('', views.index, name='updateApp_index'),
    path('<str:client_username>/', views.updatePage, name='updatePage'),
    
]  