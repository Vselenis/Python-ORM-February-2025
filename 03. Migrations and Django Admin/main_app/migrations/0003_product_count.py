# Generated by Django 5.0.4 on 2025-04-17 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_product_created_on_product_last_edited_on'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
