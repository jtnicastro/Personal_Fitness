from django.db import models
from django.conf import settings

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_trainer = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username 
    

class Trainer(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.profile.user.username 
    
class Client(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    trainer = models.ForeignKey(Trainer, null=True, blank=True, on_delete=models.SET_NULL, related_name='clients')

    def __str__(self):
        return self.profile.user.username 