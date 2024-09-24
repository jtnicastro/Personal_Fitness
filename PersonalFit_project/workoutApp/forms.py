from django import forms
from .models import Workout, Exercise, Schedule
from django.forms import inlineformset_factory

class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = {'workout_names'}

ExerciseFormSet = inlineformset_factory(
    Workout,
    Exercise,
    fields=('name', 'sets', 'reps', 'weight'),
    extra=1,
    can_delete=True
)

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
    
    def __init__(self, *args, **kwargs):
        workouts = kwargs.pop('workouts', [])
        super().__init__(*args, **kwargs)

        workout_choices = [(None, 'Rest')] + [(workout.id, workout.workout_names) for workout in workouts]

        self.fields['sunday'].choices = workout_choices
        self.fields['monday'].choices = workout_choices
        self.fields['tuesday'].choices = workout_choices
        self.fields['wednesday'].choices = workout_choices
        self.fields['thursday'].choices = workout_choices
        self.fields['friday'].choices = workout_choices
        self.fields['saturday'].choices = workout_choices
