from django.core.validators import MinValueValidator, MaxLengthValidator
from django.db import models

from main_app.validators import validate_manu_categories


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
    name = models.CharField(
        max_length=100
    )
    description = models.TextField(
        validators=[validate_manu_categories]
    )
    restaurants = models.ForeignKey(Restaurant, on_delete=models.CASCADE)


class RestaurantReview(models.Model):
    reviewer_name = models.CharField(max_length=100)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    review_content = models.TextField()
    rating = models.PositiveIntegerField(validators=[MaxLengthValidator(5)])

    class Meta:
        abstract = True
        ordering = ['-rating']
        verbose_name = 'Restaurant Review'
        verbose_name_plural = 'Restaurant Reviews'
        unique_together = ['reviewer_name', 'restaurant']


class RegularRestaurantReview(RestaurantReview):
    pass

class FoodCriticRestaurantReview(RestaurantReview):
    food_critic_cuisine_area = models.CharField
