from django.db import models
from users.models import Client, Trainer

# Create your models here.

class Workout(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="workouts")
    trainer = models.ForeignKey(Trainer, on_delete=models.SET_NULL, null=True)
    workout_names = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.workout_names}"

class Exercise(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name='exercises')
    name = models.CharField(max_length=100)
    sets = models.IntegerField()
    reps = models.IntegerField()
    weight = models.IntegerField()

    def __str__(self):
        return f"{self.name} - {self.sets} sets x {self.reps} reps @ {self.weight} lbs."

class Schedule(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='workout_schedule')
    sunday = models.ForeignKey(Workout, on_delete=models.SET_NULL, null=True, related_name='sunday_workout', blank=True)
    monday = models.ForeignKey(Workout, on_delete=models.SET_NULL, null=True, related_name='monday_workout', blank=True)
    tuesday = models.ForeignKey(Workout, on_delete=models.SET_NULL, null=True, related_name='tuesday_workout', blank=True)
    wednesday = models.ForeignKey(Workout, on_delete=models.SET_NULL, null=True, related_name='wednesday_workout', blank=True)
    thursday = models.ForeignKey(Workout, on_delete=models.SET_NULL, null=True, related_name='thursday_workout', blank=True)
    friday = models.ForeignKey(Workout, on_delete=models.SET_NULL, null=True, related_name='friday_workout', blank=True)
    saturday = models.ForeignKey(Workout, on_delete=models.SET_NULL, null=True, related_name='saturday_workout', blank=True)