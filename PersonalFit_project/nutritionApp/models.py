from django.db import models
from users.models import Client, Trainer


# Create your models here.
class Meal(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="meals")
    trainer = models.ForeignKey(Trainer, on_delete=models.SET_NULL, null=True)
    meal_names = models.CharField(max_length=150)

    def __str__(self):
        return self.meal_names


class Food(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name='food')
    name = models.CharField(max_length=100)
    calories = models.DecimalField(max_digits=6, decimal_places=1)
    protein = models.DecimalField(max_digits=5, decimal_places=1)
    fats = models.DecimalField(max_digits=5, decimal_places=1)
    carbs = models.DecimalField(max_digits=5, decimal_places=1)
    servingSize = models.CharField(max_length=50)

    def __str__(self):
        return self.name 