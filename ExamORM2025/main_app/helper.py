from django.db import models
from django.core.validators import MinLengthValidator

from django.db.models import Count

class UpdatedAtMixin(models.Model):
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Name100Mixin(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(1)]
    )

    class Meta:
        abstract = True

class UpdatedAtReadOnlyAdminMixin:
    readonly_fields = ('updated_at',)



class MuseumQuerySet(models.QuerySet):
    def get_museums_by_exhibitions_count(self):
        return (
            self.annotate(exhibitions_count=Count('exhibition'))
            .order_by('-exhibitions_count', 'name')
        )


class MuseumManager(models.Manager):
    def get_queryset(self):
        return MuseumQuerySet(self.model, using=self._db)

    def get_museums_by_exhibitions_count(self):
        return self.get_queryset().get_museums_by_exhibitions_count()