from django import forms
from django.contrib.auth.models import User
from .models import Profile, Trainer, Client


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('user',)

class ClientEditTrainerForm(forms.ModelForm):
    trainer = forms.ModelChoiceField(
        queryset=Trainer.objects.all(),
        required=False,
        #labels="Select Trainer"
    )

    class Meta:
        model = Client 
        fields = ('trainer',)


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):

    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    is_trainer = forms.BooleanField(label='Registering as a trainer?', required=False)

    class Meta:
        model = User
        fields = {'username', 'email', 'first_name', 'last_name'}

    def check_password(self):
        if self.cleaned_data['password'] != self.cleaned_data['password2']:
            raise forms.ValidationError('Passwords do not match')
        return self.cleaned_data['password2']