# Generated by Django 5.1.1 on 2024-09-24 20:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0003_trainer_client'),
    ]

    operations = [
        migrations.CreateModel(
            name='Meals',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meal_names', models.CharField(max_length=150)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meals', to='users.client')),
                ('trainer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.trainer')),
            ],
        ),
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('calories', models.IntegerField()),
                ('protein', models.IntegerField()),
                ('fats', models.IntegerField()),
                ('carbs', models.IntegerField()),
                ('servings', models.IntegerField()),
                ('meal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='food', to='nutritionApp.meals')),
            ],
        ),
    ]
