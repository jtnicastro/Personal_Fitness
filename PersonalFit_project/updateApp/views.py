from django.shortcuts import render, redirect, get_object_or_404
from users.models import Client, Trainer
from .models import Update
from .forms import UpdateForm
import datetime
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    trainer = get_object_or_404(Trainer, profile__user=request.user)
    clients = trainer.clients.all()
    updates = Update.objects.filter(trainer=trainer).order_by('-date')

    client_name = request.GET.get('client_name')

    if client_name != '' and client_name is not None:
        updates = updates.filter(client__profile__user__username__icontains=client_name)

    paginator = Paginator(updates, 5)
    page = request.GET.get('page')
    updates = paginator.get_page(page)

    return render(request, 'updateApp/index.html', {'clients':clients, 'updates':updates})

def updatePage(request, client_username):
    client = get_object_or_404(Client, profile__user__username=client_username) 

    if request.method =='POST':
        update_form = UpdateForm(request.POST, request.FILES)
        if update_form.is_valid():
            new_update = update_form.save(commit=False)
            new_update.client = client
            new_update.trainer = get_object_or_404(Trainer, profile__user=request.user)
            new_update.save()
            return redirect('updatePage', client_username=client_username)
                           
    update_form = UpdateForm()
    updates = Update.objects.filter(client=client)
    date = datetime.date.today()

    return render(request, 'updateApp/updatePage.html', {'client':client, 'updates':updates, 'update_form':update_form, 'date':date})