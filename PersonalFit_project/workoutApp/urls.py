from django.urls import path
from .import views

urlpatterns = [
    path('', views.index, name='workoutApp_index'),
    path('exerciseList/', views.exerciseList, name='exerciseList'),
    path('exerciseList/<str:bodypart>/', views.exerciseList_bodypart, name='exerciseList_bodypart'),
    path('exerciseList/details/<str:id>/', views.exerciseDetails, name='exerciseDetails'),
    path('<str:client_username>/', views.workoutPage, name='workoutPage'),
    path('<str:client_username>/addWorkout', views.addWorkout, name='addWorkout'),
    path('<str:client_username>/deleteWorkout/<int:workout_id>/', views.deleteWorkout, name='deleteWorkout'),
    path('<str:client_username>/editWorkout/<int:workout_id>/', views.editWorkout, name='editWorkout'),
    path('<str:client_username>/editSchedule', views.editSchedule, name='editSchedule'),
    path('<str:client_username>/planPDF', views.workoutPlan, name='workoutPlan'),
    

]  