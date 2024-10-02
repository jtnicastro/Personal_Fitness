from django.shortcuts import render, redirect, get_object_or_404
from users.models import Client, Trainer

# Create your views here.
def index(request):
    trainer = get_object_or_404(Trainer, profile__user=request.user)
    clients = trainer.clients.all()
    return render(request, 'updateApp/index.html', {'clients':clients,})