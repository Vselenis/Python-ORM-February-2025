from django.db import models


class AwardedMixin(models.Model):
    is_awarded = models.BooleanField(
        default=False,
        help_text="Indicates whether this entity has received awards.",
    )

    class Meta:
        abstract = True


class UpdatedMixin(models.Model):
    last_updated = models.DateTimeField(
        auto_now=True,
        help_text="Automatically updated when the record is modified.",
    )

    class Meta:
        abstract = True
