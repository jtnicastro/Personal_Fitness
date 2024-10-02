from django.urls import path
from .import views

urlpatterns = [
    path('', views.index, name='nutritionApp_index'),
    path('<str:client_username>/', views.nutritionPage, name='nutritionPage'),
    path('<str:client_username>/addMeal', views.addMeal, name='addMeal'),
    path('<str:client_username>/deleteMeal/<int:meal_id>/', views.deleteMeal, name='deleteMeal'),
    path('<str:client_username>/editMeal/<int:meal_id>/', views.editMeal, name='editMeal'),

]  