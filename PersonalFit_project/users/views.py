from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required
from .models import Profile, Trainer, Client
from nutritionApp.models import Meal
from workoutApp.models import Schedule
from updateApp.models import Update
from .forms import UserEditForm, ProfileEditForm, ClientEditTrainerForm
from chatapp.models import ChatRoom, ChatMessage 
from django.utils.text import slugify 

def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate( 
                request, username=data['username'], password=data['password'])
            if user is not None:
                login(request, user)
                return redirect('users:index')
            else:
                return HttpResponse("Invalid credentials")

    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form':form})

def user_logout(request):
    if request.method == "POST":
        logout(request)
        return redirect('users:login')

    return render(request, 'users/logout.html')

@login_required
def index(request):
    profile = Profile.objects.get(user=request.user)
    is_trainer = profile.is_trainer
    chatrooms = ChatRoom.objects.all()

    if profile.is_trainer:
        trainer = Trainer.objects.get(profile=profile)
        clients = Client.objects.filter(trainer=trainer)
        client_chatrooms = []
        meals_with_totals = []
        schedule = []
        updates = []

        total_daily_calories = total_daily_protein = total_daily_fats = total_daily_carbs = 0
        proteinP = fatP = carbP = 0

        for client in clients:
            chatroom = ChatRoom.objects.filter(name=client.profile.user.username).first()

            if chatroom:
                unread_count = ChatMessage.objects.filter(room=chatroom, is_read=False).count()
                last_message = ChatMessage.objects.filter(room=chatroom).order_by('-date').first()
                client_chatrooms.append({
                    'chatroom': chatroom,
                    'unread_count': unread_count,
                    'last_message': last_message.date if last_message else None
                })

    else:
        clients = None
        client_chatrooms = []
        client = get_object_or_404(Client, profile__user__username=profile.user.username)
        meals = Meal.objects.filter(client=client).prefetch_related('food')
        schedule = Schedule.objects.filter(client=client)
        updates = Update.objects.filter(client=client)

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

    return render(request, 'users/index.html', {'is_trainer':is_trainer, 'client_chatrooms': client_chatrooms,
                                                'chatrooms':chatrooms, 'clients':clients, 'profile':profile,
                                                'meals':meals_with_totals, 'total_daily_calories':total_daily_calories,
                                                'total_daily_protein': total_daily_protein, 'total_daily_fats': total_daily_fats,
                                                'total_daily_carbs': total_daily_carbs, 'proteinP': proteinP,
                                                'fatP': fatP, 'carbP': carbP, 'schedule': schedule, 'updates': updates,
                                                 })


def register(request):
    if request.method =="POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            profile = Profile.objects.create(user=new_user, is_trainer=user_form.cleaned_data['is_trainer'])
            
            if profile.is_trainer: 
                Trainer.objects.create(profile=profile)
            else:
                Client.objects.create(profile=profile)

                chatroom_name = new_user.username
                chatroom_slug = slugify(chatroom_name)
                ChatRoom.objects.create(name=chatroom_name, slug=chatroom_slug)
            return render(request, 'users/register_done.html')
    
    else:
        user_form = UserRegistrationForm()
    return render(request, 'users/register.html', {'user_form': user_form})

@login_required
def edit(request):
    profile = request.user.profile

    if not profile.is_trainer:
        client = profile.client
        if request.method == "POST":
            user_form = UserEditForm(instance=request.user, data=request.POST)
            profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST)
            client_form = ClientEditTrainerForm(instance=client, data=request.POST)

            if user_form.is_valid() and client_form.is_valid():
                user_form.save()
                profile_form.save()
                client_form.save()
                return HttpResponse('Profile and Trainer updated sucessfully')
        else:
            user_form = UserEditForm(instance=request.user)
            profile_form = ProfileEditForm(instance=request.user.profile)
            client_form = ClientEditTrainerForm(instance=client)
            
        return render(request, 'users/edit.html',
                               {'user_form': user_form, 
                                'profile_form': profile_form,
                                'client_form':client_form})

    else:
        if request.method=="POST":
            user_form = UserEditForm(instance=request.user, data=request.POST)
            profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                return HttpResponse('Profile updated successfully')
        else:
            user_form = UserEditForm(instance=request.user)
            profile_form = ProfileEditForm(instance=request.user.profile)
        return render(request, 'users/edit.html', {'user_form': user_form, 'profile_form': profile_form})

    
    
    