from django.shortcuts import render, redirect, get_object_or_404
from .models import Workout, Exercise, Schedule
from users.models import Client, Trainer
from .forms import WorkoutForm, ExerciseFormSet, ScheduleForm
from django.forms import inlineformset_factory

# Create your views here.
def index(request):
    trainer = get_object_or_404(Trainer, profile__user=request.user)
    clients = trainer.clients.all()
    return render(request, 'workoutApp/index.html', {'clients':clients,})

def workoutPage(request, client_username):
    client = get_object_or_404(Client, profile__user__username=client_username)
    workouts = Workout.objects.filter(client=client).prefetch_related('exercises')
    schedule = Schedule.objects.filter(client=client)
    return render(request, 'workoutApp/workoutPage.html', {'client':client, 'workouts':workouts, 'schedule':schedule })

def addWorkout(request, client_username):
    client = get_object_or_404(Client, profile__user__username=client_username)

    ExerciseFormSetDynamic = inlineformset_factory(
        Workout, Exercise, fields=('name', 'sets', 'reps', 'weight'), extra=1, can_delete=True
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
            
            return redirect('workoutPage', client_username=client_username)
    else:
        workout_form = WorkoutForm()
        exercise_formset = ExerciseFormSetDynamic()

    return render(request, 'workoutApp/addWorkout.html', {'client':client, 'workout_form':workout_form, 'exercise_formset':exercise_formset})

def deleteWorkout(request, client_username, workout_id):
    workout = get_object_or_404(Workout, id=workout_id)

    workout.delete()
    return redirect("workoutPage", client_username=client_username)

def editWorkout(request, client_username, workout_id):
    workout = get_object_or_404(Workout, id=workout_id)
    client = get_object_or_404(Client, profile__user__username=client_username)

    ExerciseFormSetDynamic = inlineformset_factory(
        Workout, Exercise, fields=('name', 'sets', 'reps', 'weight'), extra=0, can_delete=True
    )

    if request.method=="POST":
        workout_form = WorkoutForm(request.POST, instance=workout)
        exercise_formset = ExerciseFormSetDynamic(request.POST, instance=workout)

        if workout_form.is_valid() and exercise_formset.is_valid():
            workout_form.save()
            exercise_formset.save()
            return redirect('workoutPage', client_username=client_username)
        else:
            print("Workout form errors:", workout_form.errors)
            print("Exercise form errors:", exercise_formset.errors)
    else:
        workout_form = WorkoutForm(instance=workout)
        exercise_formset = ExerciseFormSetDynamic(instance=workout)


    return render(request, 'workoutApp/editWorkout.html', {'client':client, 'workout_form':workout_form,
                                                           'exercise_formset':exercise_formset, })

def editSchedule(request, client_username):
    client = get_object_or_404(Client, profile__user__username=client_username)
    workouts = Workout.objects.filter(client=client)
    schedule, created = Schedule.objects.get_or_create(client=client)

    if request.method == "POST":
        form = ScheduleForm(request.POST, workouts=workouts, instance=schedule)
        if form.is_valid():
            form.save()
            return redirect('workoutPage', client_username=client_username)
    else:
        form = ScheduleForm(instance=schedule, workouts=workouts)

    return render(request, "workoutApp/editSchedule.html", {'client':client, 'form':form})