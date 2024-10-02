from django.shortcuts import render, redirect, get_object_or_404
from users.models import Client, Trainer
from .models import Meal, Food
from .forms import MealForm
from django.forms import inlineformset_factory

# Create your views here.
def index(request):
    trainer = get_object_or_404(Trainer, profile__user=request.user)
    clients = trainer.clients.all()
    return render(request, 'nutritionApp/index.html', {'clients':clients})

def nutritionPage(request, client_username):
    client = get_object_or_404(Client, profile__user__username=client_username)
    meals = Meal.objects.filter(client=client).prefetch_related('food')

    total_daily_calories = 0
    total_daily_protein = 0
    total_daily_fats = 0
    total_daily_carbs = 0

    meals_with_totals = []
    for meal in meals:
        meal_total_calories = sum(food.calories for food in meal.food.all())
        meal_total_protein = sum(food.protein for food in meal.food.all())
        meal_total_fats = sum(food.fats for food in meal.food.all())
        meal_total_carbs = sum(food.carbs for food in meal.food.all())

        total_daily_calories += meal_total_calories
        total_daily_protein += meal_total_protein
        total_daily_fats += meal_total_fats
        total_daily_carbs += meal_total_carbs

        meals_with_totals.append({
            'meal': meal,
            'total_calories': meal_total_calories,
            'total_protein': meal_total_protein,
            'total_fats': meal_total_fats,
            'total_carbs': meal_total_carbs
        })


    totalP = (total_daily_protein*4) + (total_daily_fats * 9) + (total_daily_carbs * 4)
    proteinP = ((total_daily_protein*4) / totalP) * 100
    fatP = ((total_daily_fats*9) / totalP) * 100
    carbP = ((total_daily_carbs*4) / totalP) * 100

    return render(request, 'nutritionApp/nutritionPage.html', {'client':client, 'meals':meals_with_totals,
                                                               'total_daily_calories':total_daily_calories,
                                                               'total_daily_protein': total_daily_protein,
                                                               'total_daily_fats': total_daily_fats,
                                                               'total_daily_carbs': total_daily_carbs,
                                                               'proteinP': proteinP, 'fatP': fatP, 
                                                               'carbP': carbP,
                                                               })



def addMeal(request, client_username):
    client = get_object_or_404(Client, profile__user__username=client_username)

    FoodFormSetDynamic = inlineformset_factory(
        Meal, Food, fields=('name', 'calories', 'protein', 'fats', 'carbs', 'servingSize'), extra=1, can_delete=True
    )


    if request.method == "POST":
        meal_form = MealForm(request.POST)
        food_formset = FoodFormSetDynamic(request.POST)

        if meal_form.is_valid() and food_formset.is_valid():
            meal = meal_form.save(commit=False)
            meal.client = client
            meal.trainer = get_object_or_404(Trainer, profile__user=request.user)
            meal.save()

            foods = food_formset.save(commit=False)
            for food in foods:
                food.meal = meal
                food.save()
            
            return redirect('nutritionPage', client_username=client_username)
    else:
        meal_form = MealForm()
        food_formset = FoodFormSetDynamic()

    return render(request, 'nutritionApp/addMeal.html', {'client':client, 'meal_form':meal_form, 'food_formset':food_formset})

def deleteMeal(request, client_username, meal_id):
    meal = get_object_or_404(Meal, id=meal_id)
    meal.delete()
    return redirect('nutritionPage', client_username=client_username)

def editMeal(request, client_username, meal_id):
    meal = get_object_or_404(Meal, id=meal_id)
    client = get_object_or_404(Client, profile__user__username=client_username)

    FoodFormSetDynamic = inlineformset_factory(
        Meal, Food, fields=('name', 'calories', 'protein', 'fats', 'carbs', 'servingSize'), extra=0, can_delete=True
    )

    if request.method=="POST":
        meal_form = MealForm(request.POST, instance=meal)
        food_formset = FoodFormSetDynamic(request.POST, instance=meal)

        if meal_form.is_valid() and food_formset.is_valid():
            meal_form.save()
            food_formset.save()
            return redirect('nutritionPage', client_username=client_username)
        else:
            print("Meal form errors:", meal_form.errors)
            print("Food form errors:", food_formset.errors)
    else:
        meal_form = MealForm(instance=meal)
        food_formset = FoodFormSetDynamic(instance=meal)


    return render(request, 'nutritionApp/editMeal.html', {'client':client, 'meal_form':meal_form,
                                                           'food_formset':food_formset, })