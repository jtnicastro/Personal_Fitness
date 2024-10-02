from django import forms
from .models import Meal, Food
from django.forms import inlineformset_factory

class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = {'meal_names'}

FoodFormSet = inlineformset_factory(
    Meal,
    Food,
    fields=('name', 'calories', 'protein', 'fats', 'carbs', 'servingSize'),
    extra=1,
    can_delete=True
)
