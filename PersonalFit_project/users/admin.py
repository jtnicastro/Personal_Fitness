from django.contrib import admin
from .models import Profile, Client, Trainer
# Register your models here.
admin.site.register(Profile) 
admin.site.register(Trainer) 
admin.site.register(Client) 

