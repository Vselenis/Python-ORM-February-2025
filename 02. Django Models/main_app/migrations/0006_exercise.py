# Generated by Django 5.0.4 on 2025-04-12 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('difficulty_level', models.CharField(max_length=20)),
                ('duration_minutes', models.PositiveIntegerField()),
                ('equipment', models.CharField(max_length=90)),
                ('video_url', models.URLField(blank=True, null=True)),
                ('calories_burned', models.PositiveIntegerField(default=1)),
                ('is_favorite', models.BooleanField(default=False)),
            ],
        ),
    ]
