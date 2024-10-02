from django.urls import path
from .import views

urlpatterns = [
    path('', views.index, name='workoutApp_index'),
    path('<str:client_username>/', views.workoutPage, name='workoutPage'),
    path('<str:client_username>/addWorkout', views.addWorkout, name='addWorkout'),
    path('<str:client_username>/deleteWorkout/<int:workout_id>/', views.deleteWorkout, name='deleteWorkout'),
    path('<str:client_username>/editWorkout/<int:workout_id>/', views.editWorkout, name='editWorkout'),
    path('<str:client_username>/editSchedule', views.editSchedule, name='editSchedule'),


]  