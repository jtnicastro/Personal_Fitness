from django import forms
from .models import Update

class UpdateForm(forms.ModelForm):
    class Meta:
        model = Update
        fields = ['height', 'weight', 'file', 'notes']