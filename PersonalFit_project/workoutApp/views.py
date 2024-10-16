from django.shortcuts import render, redirect, get_object_or_404
from django.forms import inlineformset_factory
from django.template import loader
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.conf import settings

from .models import Workout, Exercise, Schedule
from users.models import Client, Trainer
from nutritionApp.models import Meal, Food
from updateApp.models import Update
from .forms import WorkoutForm, ExerciseFormSet, ScheduleForm

import pdfkit
import requests
import difflib



# Create your views here.
def index(request):
    trainer = get_object_or_404(Trainer, profile__user=request.user)
    clients = trainer.clients.all()

    clients_with_totals = []
    for client in clients:
        last_update = Update.objects.filter(client=client).last()
        weight = last_update.weight if last_update else None
        meals = Meal.objects.filter(client=client).prefetch_related("food")
        total_daily_calories = 0

        for meal in meals:
            total_daily_calories += sum(food.calories for food in meal.food.all())

        try:
            schedule = Schedule.objects.get(client=client)
            workouts_per_week = sum(
                1
                for day in [
                    schedule.sunday,
                    schedule.monday,
                    schedule.tuesday,
                    schedule.wednesday,
                    schedule.thursday,
                    schedule.friday,
                    schedule.saturday,
                ]
                if day is not None
            )
        except Schedule.DoesNotExist:
            workouts_per_week = 0

        clients_with_totals.append(
            {
                "client": client,
                "weight": weight,
                "total_daily_calories": total_daily_calories,
                "workouts_per_week": workouts_per_week,
            }
        )

    return render(
        request,
        "workoutApp/index.html",
        {
            "clients_with_totals": clients_with_totals,
        },
    )


def workoutPage(request, client_username):
    client = get_object_or_404(Client, profile__user__username=client_username)
    workouts = Workout.objects.filter(client=client).prefetch_related("exercises")
    schedule = Schedule.objects.filter(client=client)
    return render(
        request,
        "workoutApp/workoutPage.html",
        {"client": client, "workouts": workouts, "schedule": schedule},
    )


def addWorkout(request, client_username):
    client = get_object_or_404(Client, profile__user__username=client_username)

    ExerciseFormSetDynamic = inlineformset_factory(
        Workout,
        Exercise,
        fields=("name", "sets", "reps", "weight"),
        extra=1,
        can_delete=True,
    )

    if request.method == "POST":
        workout_form = WorkoutForm(request.POST)
        exercise_formset = ExerciseFormSetDynamic(request.POST)

        if workout_form.is_valid() and exercise_formset.is_valid():
            workout = workout_form.save(commit=False)
            workout.client = client
            workout.trainer = get_object_or_404(Trainer, profile__user=request.user)
            workout.save()

            exercises = exercise_formset.save(commit=False)
            for exercise in exercises:
                exercise.workout = workout
                exercise.save()

            return redirect("workoutPage", client_username=client_username)
    else:
        workout_form = WorkoutForm()
        exercise_formset = ExerciseFormSetDynamic()

    return render(
        request,
        "workoutApp/addWorkout.html",
        {
            "client": client,
            "workout_form": workout_form,
            "exercise_formset": exercise_formset,
        },
    )


def deleteWorkout(request, client_username, workout_id):
    workout = get_object_or_404(Workout, id=workout_id)

    workout.delete()
    return redirect("workoutPage", client_username=client_username)


def editWorkout(request, client_username, workout_id):
    workout = get_object_or_404(Workout, id=workout_id)
    client = get_object_or_404(Client, profile__user__username=client_username)

    ExerciseFormSetDynamic = inlineformset_factory(
        Workout,
        Exercise,
        fields=("name", "sets", "reps", "weight"),
        extra=0,
        can_delete=True,
    )

    if request.method == "POST":
        workout_form = WorkoutForm(request.POST, instance=workout)
        exercise_formset = ExerciseFormSetDynamic(request.POST, instance=workout)

        if workout_form.is_valid() and exercise_formset.is_valid():
            workout_form.save()
            exercise_formset.save()
            return redirect("workoutPage", client_username=client_username)
        else:
            print("Workout form errors:", workout_form.errors)
            print("Exercise form errors:", exercise_formset.errors)
    else:
        workout_form = WorkoutForm(instance=workout)
        exercise_formset = ExerciseFormSetDynamic(instance=workout)

    return render(
        request,
        "workoutApp/editWorkout.html",
        {
            "client": client,
            "workout_form": workout_form,
            "exercise_formset": exercise_formset,
        },
    )


def editSchedule(request, client_username):
    client = get_object_or_404(Client, profile__user__username=client_username)
    workouts = Workout.objects.filter(client=client)
    schedule, created = Schedule.objects.get_or_create(client=client)

    if request.method == "POST":
        form = ScheduleForm(request.POST, workouts=workouts, instance=schedule)
        if form.is_valid():
            form.save()
            return redirect("workoutPage", client_username=client_username)
    else:
        form = ScheduleForm(instance=schedule, workouts=workouts)

    return render(
        request, "workoutApp/editSchedule.html", {"client": client, "form": form}
    )


def workoutPlan(request, client_username):
    client = get_object_or_404(Client, profile__user__username=client_username)
    workouts = Workout.objects.filter(client=client).prefetch_related("exercises")
    schedule = Schedule.objects.filter(client=client)

    template = loader.get_template("workoutApp/workoutPlan.html")
    html = template.render(
        {
            "client": client,
            "workouts": workouts,
            "schedule": schedule,
        }
    )

    options = {
        "page-size": "Letter",
        "encoding": "UTF-8",
    }
    pdf = pdfkit.from_string(html, False, options)
    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename = "Workout_Plan.pdf"'

    return response


def exerciseList(request):
    bodyparts = ["Back", "Chest", "Shoulders", "Arms", "Legs"]
    return render(request, "workoutApp/exerciseList.html", {"bodyparts": bodyparts})


def exerciseList_bodypart(request, bodypart):
    api_bodypart_mapping = {
        "Back": "back",
        "Chest": "chest",
        "Shoulders": "shoulders",
        "Arms": "upper arms",
        "Legs": "upper legs",
    }

    api_bodypart = api_bodypart_mapping.get(bodypart, bodypart.lower())

    url = f"https://exercisedb.p.rapidapi.com/exercises/bodyPart/{api_bodypart}"
    api_key = settings.API_KEY
    querystring = {"limit": "0", "offset": "0"}
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "exercisedb.p.rapidapi.com",
    }
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        exercises = response.json()
    else:
        exercises = []

    exercise_search = request.GET.get("exercise_search", "").lower()

    if exercise_search:
        filtered_exercises = []
        for exercise in exercises:
            name_match = difflib.SequenceMatcher(
                None, exercise_search, exercise["name"].lower()
            ).ratio()
            target_match = difflib.SequenceMatcher(
                None, exercise_search, exercise["target"].lower()
            ).ratio()

            if (
                name_match > 0.99
                or target_match > 0.99
                or exercise_search in exercise["name"].lower()
                or exercise_search in exercise["target"].lower()
            ):
                filtered_exercises.append(exercise)

        exercises = filtered_exercises

    paginator = Paginator(exercises, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "workoutApp/exerciseList_bodypart.html",
        {
            "page_obj": page_obj,
            "bodypart": bodypart,
            "exercise_search": exercise_search,
        },
    )


def exerciseDetails(request, id):
    url = f"https://exercisedb.p.rapidapi.com/exercises/exercise/{id}"
    api_key = settings.API_KEY
    querystring = {"limit": "0", "offset": "0"}
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "exercisedb.p.rapidapi.com",
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        exercise = response.json()
    else:
        exercise = None

    return render(request, "workoutApp/exerciseDetails.html", {"exercise": exercise})
