from django.shortcuts import render, redirect, get_object_or_404
from users.models import Client, Trainer
from updateApp.models import Update
from .models import Meal, Food
from .forms import MealForm
from django.forms import inlineformset_factory
import pdfkit
import matplotlib.pyplot as plt
import base64
from django.http import HttpResponse
from django.template import loader
from io import BytesIO

# Create your views here.
def index(request):
    trainer = get_object_or_404(Trainer, profile__user=request.user)
    clients = trainer.clients.all()
    

    clients_with_totals = []
    for client in clients:
        last_update = Update.objects.filter(client=client).last()
        weight = last_update.weight if last_update else None
        meals = Meal.objects.filter(client=client).prefetch_related('food')

        total_daily_calories = 0
        total_daily_protein = 0
        total_daily_fats = 0
        total_daily_carbs = 0        

        for meal in meals:
            meal_total_calories = sum(food.calories for food in meal.food.all())
            meal_total_protein = sum(food.protein for food in meal.food.all())
            meal_total_fats = sum(food.fats for food in meal.food.all())
            meal_total_carbs = sum(food.carbs for food in meal.food.all())

            total_daily_calories += meal_total_calories
            total_daily_protein += meal_total_protein
            total_daily_fats += meal_total_fats
            total_daily_carbs += meal_total_carbs

        clients_with_totals.append({
            'client':client,
            'weight':weight,
            'total_calories':total_daily_calories,
            'total_protein':total_daily_protein,
            'total_fats':total_daily_fats,
            'total_carbs':total_daily_carbs,
        })

    return render(request, 'nutritionApp/index.html', {'clients_with_totals':clients_with_totals})

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

    if totalP > 0:
        proteinP = ((total_daily_protein*4) / totalP) * 100
        fatP = ((total_daily_fats*9) / totalP) * 100
        carbP = ((total_daily_carbs*4) / totalP) * 100
    else:
        proteinP = fatP = carbP = 0
    

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

def mealPlan(request, client_username):
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
    
    total_calories_from_macros = (total_daily_protein*4)+(total_daily_fats*9)+(total_daily_carbs*4)

    if total_calories_from_macros > 0:
        protein_percentage = (total_daily_protein*4) / total_calories_from_macros
        fats_percentage = (total_daily_fats*9) / total_calories_from_macros
        carbs_percentage = (total_daily_carbs*4) / total_calories_from_macros
    else:
        protein_percentage = fats_percentage = carbs_percentage = 0

    # Doughnut chart 
    labels = ['Protein', 'Fats', 'Carb']
    sizes = [protein_percentage, fats_percentage, carbs_percentage]
    colors = ['#ff9999', '#66b3ff', '#99ff99']

    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors, pctdistance=0.85)
    centre_circle = plt.Circle((0,0), 0.70, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    buf = BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    chart_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    template = loader.get_template('nutritionApp/meal_plan.html')
    html = template.render({'client':client, 'meals':meals_with_totals,
                            'total_daily_calories':total_daily_calories,
                            'total_daily_protein':total_daily_protein,
                            'total_daily_fats':total_daily_fats,
                            'total_daily_carbs':total_daily_carbs,
                            'chart_base64':chart_base64,
                            })
    options ={
        'page-size':'Letter',
        'encoding':'UTF-8',
    }
    pdf = pdfkit.from_string(html,False,options)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename = "Meal_Plan.pdf"'

    return response