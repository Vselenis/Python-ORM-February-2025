from django.db import models

from decimal import Decimal

from django.db import models
from django.core.validators import (
    MinLengthValidator,
    MinValueValidator,
    MaxValueValidator,
)

from .base import PersonBase
from .mixins import AwardedMixin, UpdatedMixin
from django.db.models import Count


class DirectorManager(models.Manager):
    def get_directors_by_movies_count(self):
        return (
            self.annotate(movie_count=Count("movies"))
            .order_by("-movie_count", "full_name")
        )

class Director(PersonBase):
    years_of_experience = models.SmallIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
    )
    objects = DirectorManager()

    def __str__(self):
        return self.full_name

    class Meta:
        ordering = ("full_name",)

class Actor(PersonBase, AwardedMixin, UpdatedMixin):
    class Meta:
        ordering = ("full_name",)


class Movie(AwardedMixin, UpdatedMixin):

    class Genre(models.TextChoices):
        ACTION = "Action", "Action"
        COMEDY = "Comedy", "Comedy"
        DRAMA = "Drama", "Drama"
        OTHER = "Other", "Other"

    title = models.CharField(
        max_length=150,
        validators=[MinLengthValidator(5)],
    )

    release_date = models.DateField(
    )

    storyline = models.TextField(
        null=True,
        blank=True,
    )

    genre = models.CharField(
        max_length=6,
        choices=Genre.choices,
        default=Genre.OTHER,
    )

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        default=Decimal("0.0"),
        validators=[MinValueValidator(Decimal("0.0")), MaxValueValidator(Decimal("10.0"))],
    )

    is_classic = models.BooleanField(
        default=False,
    )

    director = models.ForeignKey(
        "Director",
        on_delete=models.CASCADE,
        related_name="movies",
    )

    starring_actor = models.ForeignKey(
        "Actor",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="starred_movies",
    )

    actors = models.ManyToManyField(
        "Actor",
        related_name="movies",
        blank=True,
    )

    class Meta:
        ordering = ("title",)

    def __str__(self) -> str:
        return self.title

