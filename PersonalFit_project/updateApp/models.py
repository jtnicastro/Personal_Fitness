from django.db import models
from users.models import Client, Trainer


# Create your models here.
class Update(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="updates")
    trainer = models.ForeignKey(Trainer, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now=True)
    height = models.IntegerField()
    weight = models.FloatField()
    file = models.FileField(upload_to='uploads')
    notes = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.client} - {self.date}"