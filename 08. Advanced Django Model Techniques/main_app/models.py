from django.core.validators import MinValueValidator, MaxLengthValidator
from django.db import models

class Restaurant(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[
            MinValueValidator(2, message='Name must be at least 2 characters long.'),
            MaxLengthValidator(100, message='Name cannot exceed 100 characters.')
        ]
    )

    location = models.CharField(
        max_length=200,
        validators=[
            MinValueValidator(2, message='Name must be at least 2 characters long.'),
            MaxLengthValidator(200, message='Name cannot exceed 200 characters.')
        ]
    )

    description = models.TextField(
        null=True,
        blank=True
    )

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[
            MinValueValidator(0, message="Rating must be at least 0.00."),
            MaxLengthValidator(5, message="Rating cannot exceed 5.00."),
        ]
    )


class Menu(models.Model):
    