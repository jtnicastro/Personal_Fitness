# Generated by Django 5.1.1 on 2024-09-23 23:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workoutApp', '0003_alter_schedule_is_restday'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='schedule',
            name='day',
        ),
        migrations.RemoveField(
            model_name='schedule',
            name='is_restDay',
        ),
        migrations.RemoveField(
            model_name='schedule',
            name='workout',
        ),
        migrations.AddField(
            model_name='schedule',
            name='friday',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='friday_workout', to='workoutApp.workout'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='monday',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='monday_workout', to='workoutApp.workout'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='saturday',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='saturday_workout', to='workoutApp.workout'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='sunday',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sunday_workout', to='workoutApp.workout'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='thursday',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='thursday_workout', to='workoutApp.workout'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='tuesday',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tuesday_workout', to='workoutApp.workout'),
        ),
        migrations.AddField(
            model_name='schedule',
            name='wednesday',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='wednesday_workout', to='workoutApp.workout'),
        ),
    ]
