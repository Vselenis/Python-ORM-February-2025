# Generated by Django 5.0.4 on 2025-04-17 06:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2025, 4, 17, 6, 10, 2, 142233, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='last_edited_on',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
