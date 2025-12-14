from django.db import models

from django.core.validators import MaxValueValidator,MinValueValidator
from .helper import UpdatedAtMixin, Name100Mixin,MuseumManager


class Museum(Name100Mixin, UpdatedAtMixin):
    location = models.CharField(max_length=150)

    annual_visitors = models.PositiveIntegerField(
        default=1,
        validators = [
            MinValueValidator(1),
            MaxValueValidator(10000000)
        ]
    )

    website = models.URLField(
        max_length=200,
        null=True,
        blank=True
    )

    objects = MuseumManager()


class Curator(Name100Mixin, UpdatedAtMixin):
    specialization = models.CharField(max_length=50)
    experience_years = models.PositiveSmallIntegerField(default=0)


class Exhibition(Name100Mixin, UpdatedAtMixin):
    THEME_CHOICES = [
        ("History", "History"),
        ("Science", "Science"),
        ("Art", "Art"),
        ("Other", "Other"),
    ]

    theme = models.CharField(
        max_length=7,
        choices=THEME_CHOICES,
        default="Art"
    )

    opening_date = models.DateField()
    is_free_entry = models.BooleanField(default=False)

    details = models.TextField(
        null=True,
        blank=True
    )

    museum = models.ForeignKey(
        Museum,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    curators = models.ManyToManyField('Curator')

